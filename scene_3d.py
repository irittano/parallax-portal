'''
Funciones relacionadas a OpenGL para el dibujado de una escena 3D

Coordenadas:
- X positivo hacia la derecha
- Y positivo hacia arriba
- Z positivo hacia afuera de la pantalla (la persona está en Z positivo y los
  objetos en Z negativo)
- Distancias en centimetros

Notas sobre OpenGL:

- Un VAO contiene varios VBOs
- Un VBO es un buffer con información sobre vertices
- Un shader es código que corre en GPU y toma uno o varios VBOs
- Un programa es un conjunto de shaders que creo que se usan juntos

Por cada objeto o grupo de objetos debería tener un VAO, un programa y varios
shaders
'''

import video
from config import prm

from OpenGL import GL
from OpenGL.GL import shaders as GLShaders
from OpenGL.arrays import vbo as GLVbo
from OpenGL import GLU
from OpenGL import GLUT
import glm

import pygame
import PIL.Image
import numpy as np

MIN_Z = -60 # cm
NEAR_Z = 1 # cm
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (1, 1, 1)
COLOR_RED = (1, 0, 0)
COLOR_GREEN = (0, 1, 0)
COLOR_BLUE = (0, 0, 1)

# Ubicaciones de variables en el shader, puede ser cualquier numero creo
LOCATIONS = {
    'MVP': 0,
    'texture': 1,
    'vertexPos': 2,
    'vertexUV': 3,
}

def get_cam_from_mouse(screen_s):
    '''
    Obtener coordenadas de la camara desde la posicion del mouse

    Dar como argumento tuple de ancho y alto de pantalla en pixeles

    Posicion Z de la camara fija en 30
    '''
    mouse = pygame.mouse.get_pos()
    pos = np.divide(
            np.subtract(
                np.divide(screen_s, 2),
                mouse
            ),
            6
        )

    return (pos[0], -pos[1], 30)

def set_camera(cam, screen, screen_s):
    '''
    Configura la camara en la posicion dada

    Devuelve la matriz de proyección y de vista
    '''

    projection = glm.mat4(1)
    view = glm.mat4(1)

    if prm["scene_3d_perspective"]:
        projection = glm.perspective(glm.radians(60),
                screen_s[0] / screen_s[1], 1, 250)
        view = glm.lookAt(cam, (0, 0, 0), (0, 1, 0))

    else:
        # SKEWED FRUSTRUM / OFF-AXIS PROJECTION
        # Basada en la implementación de
        # https://github.com/agirault/screenReality
        # basada en el paper:
        # Name:   Generalized Perspective Projection
        # Author: Robert Kooima
        # Date:   August 2008, revised June 2009

        # space corners coordinates
        pa = np.array((-screen[0], -screen[1], 0))
        pb = np.array(( screen[0], -screen[1], 0))
        pc = np.array((-screen[0],  screen[1], 0))
        pe = cam
        # Compute an orthonormal basis for the screen.
        vr = pb - pa
        vr /= np.linalg.norm(vr)
        vu = pc - pa
        vu /= np.linalg.norm(vu)
        vn = np.cross(vr, vu)
        vn /= np.linalg.norm(vn)
        # Compute the screen corner vectors.
        va = pa - pe
        vb = pb - pe
        vc = pc - pe
        # Find the distance from the eye to screen plane.
        d = -np.dot(va, vn)
        # Find the extent of the perpendicular projection.
        l = np.dot(va, vr) * NEAR_Z / d;
        r = np.dot(vr, vb) * NEAR_Z / d;
        b = np.dot(vu, va) * NEAR_Z / d;
        t = np.dot(vu, vc) * NEAR_Z / d;
        # Load the perpendicular projection.
        projection = glm.frustum(l, r, b, t, NEAR_Z, -MIN_Z + d);
        # Rotate the projection to be non-perpendicular.
        projection = projection * glm.mat4(
            vr[0], vu[0], vn[0],     0,
            vr[1], vu[1], vn[1],     0,
            vr[1], vu[2], vn[2],     0,
                0,     0,     0,     1,
            )
        # Move the apex of the frustum to the origin.
        projection = glm.translate(projection,
            glm.vec3(-pe[0], -pe[1], -pe[2]))

    return projection, view

def load_texture(path):
    '''
    Cargar textura RGBA desde PNG
    '''
    image = PIL.Image.open(path).transpose(PIL.Image.FLIP_TOP_BOTTOM)
    data = np.fromstring(image.tobytes(), dtype=np.uint8)
    width, height = image.size
    image.close()

    # Generar 1 textura
    texture_id = GL.glGenTextures(1)

    # Usar la textura creada
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)

    # Pasar datos
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data);
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    # Configurar escalado
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)

    return texture_id

class HouseVAO:

    def __init__(self, screen_s_cm):
        '''
        Crear VAO para la casa

        Incluye todos los vértices con sus datos (VBO), su textura, etc.
        '''

        # Crear VAO y bindear

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        # Cargar vertices en VBOs

        self.vbo = GLVbo.VBO(
            np.array([
                # X, Y, Z, W,   U,  V

                # Izquierda
                [-1, 1,-1, 1,   0,    1],
                [-1,-1, 1, 1, 1/3, 0.64],
                [-1,-1,-1, 1,   0, 0.64],
                [-1, 1,-1, 1,   0,    1],
                [-1, 1, 1, 1, 1/3,    1],
                [-1,-1, 1, 1, 1/3, 0.64],
                # Atras
                [-1, 1,-1, 1, 1/3,    1],
                [-1,-1,-1, 1, 1/3, 0.64],
                [ 1,-1,-1, 1, 2/3, 0.64],
                [-1, 1,-1, 1, 1/3,    1],
                [ 1,-1,-1, 1, 2/3, 0.64],
                [ 1, 1,-1, 1, 2/3,    1],
                # Derecha
                [ 1, 1,-1, 1, 2/3,    1],
                [ 1,-1,-1, 1, 2/3, 0.64],
                [ 1,-1, 1, 1,   1, 0.64],
                [ 1, 1,-1, 1, 2/3,    1],
                [ 1,-1, 1, 1,   1, 0.64],
                [ 1, 1, 1, 1,   1,    1],
                # Techo
                [-1, 1, 1, 1,   0, 0.64],
                [-1, 1,-1, 1,   0,    0],
                [ 1, 1,-1, 1, 1/3,    0],
                [-1, 1, 1, 1,   0, 0.64],
                [ 1, 1,-1, 1, 1/3,    0],
                [ 1, 1, 1, 1, 1/3, 0.64],
                # Piso
                [-1,-1, 1, 1, 1/3, 0.64],
                [ 1,-1,-1, 1, 2/3,    0],
                [-1,-1,-1, 1, 1/3,    0],
                [-1,-1, 1, 1, 1/3, 0.64],
                [ 1,-1, 1, 1, 2/3, 0.64],
                [ 1,-1,-1, 1, 2/3,    0],
            ], dtype=np.float32)
        )

        # Números varios

        # Salto en bytes entre valor y valor
        # Son 6 números (X, Y, Z, W, U, V) de 4 bits cada uno
        self.vbo_stride = 6 * 4

        # Offset en donde se ubican valores de UV
        # Son 4 números (X, Y, Z, W) de 4 bits cada uno
        self.vbo_uv_offset = 4 * 4

        # Desbindear VAO

        GL.glBindVertexArray(0)

        # Obtener matriz de modelo

        self.model = glm.mat4(1)
        self.model = glm.scale(self.model,
                glm.vec3(screen_s_cm[0], screen_s_cm[1], screen_s_cm[0]))
        self.model = glm.translate(self.model, glm.vec3(0, 0, -1))

        # Cargar texturas

        self.texture = load_texture("./res/house/house.png")


    def draw(self, projection, view):
        '''
        Dibujar todo

        Toma las matrices de proyección y vista de la cámara. Previamente se
        deben activar los shaders a usar
        '''

        # Bindear VAO, supuestamente bindea todos los VBOs
        GL.glBindVertexArray(self.vao)

        # Obtener matriz de ModelViewProjection

        mvp = projection * view * self.model
        GL.glUniformMatrix4fv(LOCATIONS['MVP'], 1, GL.GL_FALSE,
            glm.value_ptr(mvp))

        # Usar textura como uniform, parece que no es necesario? TODO
        #  GL.glActiveTexture(GL.GL_TEXTURE0)
        #  GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        #  GL.glUniform1i(self.texture, 0)

        # Dibujar

        with self.vbo:
            GL.glEnableVertexAttribArray(LOCATIONS['vertexPos'])
            GL.glEnableVertexAttribArray(LOCATIONS['vertexUV'])
            GL.glVertexAttribPointer(LOCATIONS['vertexPos'], 4,
                    GL.GL_FLOAT, GL.GL_FALSE, self.vbo_stride, self.vbo)
            GL.glVertexAttribPointer(LOCATIONS['vertexUV'], 2, GL.GL_FLOAT,
                    GL.GL_FALSE, self.vbo_stride, self.vbo + 4 * 4)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6*5)

        GL.glDisableVertexAttribArray(LOCATIONS['vertexPos'])
        GL.glDisableVertexAttribArray(LOCATIONS['vertexUV'])

        # Desbindear VAO
        GL.glBindVertexArray(0)


class Scene3D:

    def __init__(self):
        self.video = video.Video()
        self.video.set_mode_3d()
        self.screen_s = self.video.screen_size
        self.screen_s_cm = np.array(self.screen_s) / prm["px_per_cm"] / 2

        # Para que las cosas se dibujen en orden correcto
        GL.glEnable(GL.GL_DEPTH_TEST);
        GL.glDepthFunc(GL.GL_LESS);

        # No dibujar triangulos cuya normal no mire hacia la camara
        GL.glEnable(GL.GL_CULL_FACE);

        # Para transparencias
        GL.glEnable(GL.GL_BLEND);
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        vertex_shader = '''
        #version 130

        in vec4 vertexPos;
        in vec2 vertexUV;

        out vec2 UV;

        // Model View Projection Matrix
        uniform mat4 MVP;

        void main()
        {
            gl_Position = MVP * vertexPos;
            UV = vertexUV;
        }
        '''

        fragment_shader = '''
        #version 130

        in vec2 UV;

        out vec4 color;

        uniform sampler2D texture_sampler;

        void main()
        {
           color = texture(texture_sampler, UV);
        }
        '''

        # Compilar shaders

        self.shaders = GLShaders.glCreateProgram()
        GLShaders.glAttachShader(self.shaders,
                GLShaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER))
        GLShaders.glAttachShader(self.shaders,
                GLShaders.compileShader(fragment_shader, GL.GL_FRAGMENT_SHADER))

        for name, location in LOCATIONS.items():
            GLShaders.glBindAttribLocation(self.shaders, location, name)

        GLShaders.glLinkProgram(self.shaders)

        # Cargar VAOs de objetos

        self.house_vao = HouseVAO(self.screen_s_cm)

        # Iniciar loop

        self.video.start_loop(
            lambda screen, delta_t, screen_w, screen_h:
                self.loop(screen, delta_t, np.array((screen_w, screen_h)))
        )

    def loop(self, screen, delta_t, screen_s):

        # Activar shaders
        GLShaders.glUseProgram(self.shaders)

        # Limpiar pantalla
        GL.glClearColor(0.4, 0.8, 1, 0.0);
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # Recalcular matrices de proyección y vista
        cam_pos = get_cam_from_mouse(screen_s)
        projection, view = set_camera(cam_pos, self.screen_s_cm, screen_s)

        # Dibujar
        self.house_vao.draw(projection, view)

        # Desactivar shaders
        GLShaders.glUseProgram(0)


def demo():
    print("Entrado a escena 3D")

    Scene3D()

