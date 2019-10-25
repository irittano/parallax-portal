'''
Funciones de bajo nivel para manejar OpenGL y pygame (pero no para OpenCV)
'''

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Mantiene estado del modo de video, ya sea "2d" o "3d"
MODE = None

def init():
    '''
    Inicializar, pygame and OpenGL

    Luego se debe llamar a set_mode_3d() o set_mode_2d()
    '''
    pygame.init()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_NORMALIZE)

    #  glutInit()
    #  glutInitDisplayMode(GLUT_RGBA)
    #  glutInitWindowSize(500, 500)
    #  glutInitWindowPosition(0, 0)
    #  wind = glutCreateWindow("OpenGL Coding Practice")
    #  glutDisplayFunc(showScreen)
    #  glutIdleFunc(showScreen)
    #  glutMainLoop()

def set_mode_3d():
    '''
    Configurar el modo de video en 3D

    Configura a pygame para usar OpenGL para el dibujado
    '''

    MODE = "3d"

    # Supongo que la maxima resolucion es la primera devuelta por pygame
    max_screen_size = pygame.display.list_modes()[0]

    screen = pygame.display.set_mode(max_screen_size,
        HWSURFACE|DOUBLEBUF|OPENGL)

    # No funciona?
    #  screen = pygame.display.set_mode(max_screen_size,
        #  FULLSCREEN|HWSURFACE|DOUBLEBUF|OPENGL)

    glViewport(0, 0, max_screen_size[0], max_screen_size[1])

def set_mode_2d():
    '''
    Configurar el modo de video en 2D

    Configura a pygame para dibujar en 2D estándar en lugar de OpenGL
    '''

    MODE = "2d"

    # Supongo que la maxima resolucion es la primera devuelta por pygame
    max_screen_size = pygame.display.list_modes()[0]

    screen = pygame.display.set_mode(max_screen_size,
        HWSURFACE|DOUBLEBUF)

    # No funciona?
    #  screen = pygame.display.set_mode(max_screen_size,
        #  FULLSCREEN|SCALED|HWSURFACE|DOUBLEBUF)

def update():
    '''
    Refrescar la pantalla
    '''

    pygame.display.flip()

def start_loop(loop):
    '''
    Iniciar loop, llamando a la función dada en cada frame

    Argumentos dados a la función de callback:
    - delta_t: Tiempo pasado desde ultimo frame en segundos
    '''

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

        # Tiempo pasado desde ultimo frame en segundos
        delta_t = clock.tick() / 1000

        loop(delta_t)
        print(delta_t)

        pygame.display.flip()

def _resize():
    width, height = pygame.screen.get_size()

    if MODE == "3d":
        glViewport(0, 0, width, height)

