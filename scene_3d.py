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
import os
import random

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

    if prm['scene_3d_perspective']:
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

class ObjectVAO:

    def __init__(self, data):
        '''
        Crear VAO para un objeto

        Dar np.ndarray de datos float32 para poner en un único VBO. Con
        componentes (X, Y, Z, U, V)
        '''

        # Crear VAO y bindear

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        # Cargar vertices en VBOs

        self.vbo = GLVbo.VBO(data)

        # Números varios

        # Salto en bytes entre valor y valor
        # Son 6 números (X, Y, Z, W, U, V) de 4 bits cada uno
        self.vbo_stride = 6 * 4

        # Offset en donde se ubican valores de UV
        # Son 4 números (X, Y, Z, W) de 4 bits cada uno
        self.vbo_uv_offset = 4 * 4

        # Desbindear VAO

        GL.glBindVertexArray(0)

    def draw(self, projection, view, model, texture):
        '''
        Dibujar todo

        Toma las matrices de proyección y vista de la cámara y la textura.
        Previamente se deben activar los shaders a usar
        '''

        # Bindear VAO, supuestamente bindea todos los VBOs
        GL.glBindVertexArray(self.vao)

        # Obtener matriz de ModelViewProjection

        mvp = projection * view * model
        GL.glUniformMatrix4fv(LOCATIONS['MVP'], 1, GL.GL_FALSE,
            glm.value_ptr(mvp))

        # Usar textura como uniform, parece que no es necesario? TODO
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        #  GL.glUniform1i(texture, LOCATIONS['texture'])

        # Dibujar

        with self.vbo:
            GL.glEnableVertexAttribArray(LOCATIONS['vertexPos'])
            GL.glEnableVertexAttribArray(LOCATIONS['vertexUV'])
            GL.glVertexAttribPointer(
                LOCATIONS['vertexPos'],
                4,
                GL.GL_FLOAT, GL.GL_FALSE,
                self.vbo_stride,
                self.vbo
            )
            GL.glVertexAttribPointer(
                LOCATIONS['vertexUV'],
                2,
                GL.GL_FLOAT, GL.GL_FALSE,
                self.vbo_stride,
                self.vbo + self.vbo_uv_offset
            )
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6*5)

        GL.glDisableVertexAttribArray(LOCATIONS['vertexPos'])
        GL.glDisableVertexAttribArray(LOCATIONS['vertexUV'])

        # Desbindear VAO
        GL.glBindVertexArray(0)

class Cards:

    def __init__(self, screen_s_cm):
        '''
        Mantiene estado de todas las tarjetas

        Contiene un VAO y modelo, textura, etc. de cada tarjeta
        '''

        self.screen_s_cm = screen_s_cm

        self.vao = ObjectVAO(
            np.array([
                # X, Y, Z, W, U, V
                [-1, 1, 0, 1, 0, 1],
                [-1,-1, 0, 1, 0, 0],
                [ 1,-1, 0, 1, 1, 0],
                [-1, 1, 0, 1, 0, 1],
                [ 1,-1, 0, 1, 1, 0],
                [ 1, 1, 0, 1, 1, 1],
            ], dtype=np.float32)
        )

        # Cargar texturas

        self.textures = []
        for filename in os.listdir('./res/stamps/'):
            if filename.endswith('.png'):
                self.textures.append(
                        load_texture(os.path.join('./res/stamps/', filename)))

        # Crear lista de cartas
        # Cada elemento de la lista va a ser un diccionario

        self.cards = []

        # Tiempo en segundos hasta aparición de nueva carta

        self.timer = prm['scene_3d_interval']

    def create_card(self):
        '''
        Agregar una carta

        Crear una carta más con parámetros aleatorios
        '''

        # Mantiene el tiempo personal de cada carta, cuando se crea empieza en
        # -1.2, cada vez que se hace update_position() se incrementa el tiempo,
        # y cuando llega a 1.2 se debe borrar la carta.
        # El tiempo no tiene unidad, es una cuestión de animación. En
        # update_position() se calcula en cuanto incrementar en cada frame.
        time = -1.2

        # Obtener eje de rotación, es un versor de 3 componentes aleatorio
        # https://codereview.stackexchange.com/a/77944
        axis = np.random.uniform(size=3)
        axis /= glm.vec3(np.linalg.norm(axis))

        # Crear matriz de modelo
        model = glm.mat4(1)

        # Textura aleatoria
        texture = random.choice(self.textures)

        # Agregar a la lista y configurar tiempo hasta aparición de nueva carta
        self.cards.append({
            'time': time,
            'axis': axis,
            'model': model,
            'texture': texture,
        })
        self.timer = prm['scene_3d_interval']

    def update_position(self, delta_t):
        '''
        Mover cartas

        Actualiza las matrices de modelo de cartas existentes y crea nuevas
        cartas si es la hora

        Ecuaciones de movimiento:
        - X(t) = t^5
        - Y(t) = 0.2 * cos(pi * t / 2)
        - Z(t) = 0.4 * cos(pi * t / 2)
        - Rotacion(t) = max_rotation * pi * sin(pi * x / 2)

        Tener en cuenta que la habitación es:
        - -1 < X < 1
        - -1 < Y < 1
        - -1 < Z < 1

        Las ecuaciones hacen que el objeto se mantenga en la habitación durante
        (-1 < t < 1). El objeto se mueve de -X a X. Se escapa por Y = 0 y Z = 0
        en donde debería haber una puerta/ventana.
        La rotación es cero cuando está en el centro y máxima en los extremos.
        El eje de rotación es aleatorio entre carta y carta

        Comprobar en https://christopherchudzicki.github.io/MathBox-Demos/parametric_curves_3D.html
        '''

        # Crear carta si hace falta
        self.timer -= delta_t
        if self.timer < 0:
            self.create_card()

        for card in self.cards:

            # Incrementar tiempo de cada carta, delta_t es el tiempo desde el
            # último frame en segundos, y se multiplica con un factor cualquiera
            # que determina que velocidad de movimiento tiene la carta
            card['time'] += delta_t * prm['scene_3d_speed']

            # Actualizar matrices de modelo
            t = card['time']
            x = t**5
            y = 0.2 * np.cos(np.pi * t / 2)
            z = 0.4 * np.cos(np.pi * t / 2)
            rotation = prm['scene_3d_max_rotation'] * np.pi * np.sin(np.pi * x / 2)

            model = glm.mat4(1)

            # 4°: Aplicar posición escalando por tamaño de habitación
            model = glm.translate(
                model,
                glm.vec3(
                    x * self.screen_s_cm[0], # Multiplico por dimensiones de casa
                    y * self.screen_s_cm[1],
                    z * self.screen_s_cm[0],
                )
            )
            # 3°: Mover hacia atras para centrar en la habitación
            model = glm.translate(model,
                    glm.vec3(0, 0, -1 * self.screen_s_cm[0]))
            # 2°: Escalar imagen
            model = glm.scale(model,
                    glm.vec3(self.screen_s_cm[0]/10, self.screen_s_cm[0]/10, self.screen_s_cm[0]/10))
            # 1°: Rotar
            model = glm.rotate(model, rotation, card['axis'])

            card['model'] = model

        # Eliminar cartas que se fueron de la pantalla
        self.cards = list(filter(lambda c: c['time'] < 1.2, self.cards))

    def draw(self, projection, view):

        for card in self.cards:
            self.vao.draw(projection, view, card['model'], card['texture'])

class House:

    def __init__(self, screen_s_cm):
        '''
        Representa la casa

        Contiene un VAO, modelo, textura, etc.
        '''

        self.screen_s_cm = screen_s_cm

        self.vao = ObjectVAO(
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

        # Obtener matriz de modelo

        self.model = glm.mat4(1)
        self.model = glm.scale(self.model,
                glm.vec3(screen_s_cm[0], screen_s_cm[1], screen_s_cm[0]))
        self.model = glm.translate(self.model, glm.vec3(0, 0, -1))

        # Cargar texturas

        self.texture = load_texture('./res/house/house.png')

    def draw(self, projection, view):

        self.vao.draw(projection, view, self.model, self.texture)

class Scene3D:

    def __init__(self):
        self.video = video.Video()
        self.video.set_mode_3d()
        self.screen_s = self.video.screen_size
        self.screen_s_cm = np.array(self.screen_s) / prm['px_per_cm'] / 2

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

        self.house = House(self.screen_s_cm)
        self.cards = Cards(self.screen_s_cm)

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

        # Dibujar, importante por temas de alpha y depth tests dibujar en orden
        # de atras para adelante, o sea, primero dibujar la casa
        # https://stackoverflow.com/questions/4155397/problems-with-layers-depth-and-blending-in-opengl

        self.house.draw(projection, view)
        self.cards.update_position(delta_t)
        self.cards.draw(projection, view)

        # Desactivar shaders
        GLShaders.glUseProgram(0)


def demo():
    print('Entrado a escena 3D')

    Scene3D()

