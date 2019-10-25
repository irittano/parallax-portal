'''
Funciones de bajo nivel para manejar OpenGL y pygame (pero no para OpenCV)
'''

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Mantiene estado del modo de video, ya sea "2d" o "3d"
MODE = None

# Tamaño de pantalla en px
SCREEN_W = None
SCREEN_H = None

# Pantalla
SCREEN = None

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

def set_mode_3d():
    '''
    Configurar el modo de video en 3D

    Configura a pygame para usar OpenGL para el dibujado
    '''

    global MODE
    MODE = "3d"

    # Supongo que la maxima resolucion es la primera devuelta por pygame
    max_screen_size = pygame.display.list_modes()[0]

    screen = pygame.display.set_mode(max_screen_size,
        HWSURFACE|DOUBLEBUF|OPENGL)

    # No funciona?
    #  screen = pygame.display.set_mode(max_screen_size,
        #  FULLSCREEN|HWSURFACE|DOUBLEBUF|OPENGL)

    global SCREEN_W
    global SCREEN_H
    SCREEN_W = max_screen_size[0]
    SCREEN_H = max_screen_size[1]

    glViewport(0, 0, SCREEN_W, SCREEN_H)

def set_mode_2d():
    '''
    Configurar el modo de video en 2D

    Configura a pygame para dibujar en 2D estándar en lugar de OpenGL
    '''

    global MODE
    MODE = "2d"

    # Supongo que la maxima resolucion es la primera devuelta por pygame
    max_screen_size = pygame.display.list_modes()[0]

    global SCREEN
    SCREEN = pygame.display.set_mode(max_screen_size,
        HWSURFACE|DOUBLEBUF)

    global SCREEN_W
    global SCREEN_H
    SCREEN_W = max_screen_size[0]
    SCREEN_H = max_screen_size[1]


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
    - width: Ancho de ventana en px
    - height: Alto de ventana en px
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

        loop(SCREEN, delta_t, SCREEN_W, SCREEN_H)

        pygame.display.flip()
