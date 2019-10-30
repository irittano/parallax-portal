'''
Funciones de bajo nivel para manejar OpenGL y pygame (pero no para OpenCV)
'''

import pygame
from pygame.locals import *
import numpy as np

from config import prm

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Mantiene estado del modo de video, ya sea "2d" o "3d"
MODE = None

# Tamaño de pantalla en px
SCREEN_W = None
SCREEN_H = None

# Pantalla
SCREEN = None

FONT_SIZE = 20
COLOR_DEBUG_TEXT = np.array((1., 0., 1.))
# Fuente usada para debugging
PYGAME_DEBUG_FONT = None

def init():
    '''
    Inicializar pygame y OpenGL

    Luego se debe llamar a set_mode_3d() o set_mode_2d()
    '''
    pygame.init()
    pygame.font.init()
    global PYGAME_DEBUG_FONT
    PYGAME_DEBUG_FONT = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)

    glutInit()
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

def draw_debug_text(text, position):
    '''
    Dibujar linea de texto, no soporta saltos de linea

    Dar posicion como tuple o np.ndarray en pixeles para esquina superior
    izquierda
    '''
    if MODE == "2d":
        surface = PYGAME_DEBUG_FONT.render(text, False, COLOR_DEBUG_TEXT * 255)
        SCREEN.blit(surface, position)
    elif MODE == "3d":
        glMatrixMode(GL_PROJECTION);
        glPushMatrix();
        glLoadIdentity();
        gluOrtho2D(0.0, SCREEN_W, 0.0, SCREEN_H);
        glMatrixMode(GL_MODELVIEW);
        glPushMatrix();
        glLoadIdentity();

        glColor3f(*COLOR_DEBUG_TEXT);
        glTranslatef(position[0], SCREEN_H - position[1] - FONT_SIZE, 0);
        # La fuente por defecto tiene aprox 150px de alto
        glScalef(FONT_SIZE / 150, FONT_SIZE / 150, 0)
        glLineWidth(2);
        for char in text:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char));
            pass

        glMatrixMode(GL_PROJECTION);
        glPopMatrix();
        glMatrixMode(GL_MODELVIEW);
        glPopMatrix();

def start_loop(loop):
    '''
    Iniciar loop, llamando a la función dada en cada frame

    Argumentos dados a la función de callback:
    - screen: Pantalla de pygame
    - delta_t: Tiempo pasado desde ultimo frame en segundos
    - width: Ancho de ventana en px
    - height: Alto de ventana en px
    '''

    clock = pygame.time.Clock()
    selected = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

        # Tiempo pasado desde ultimo frame en segundos
        delta_t = clock.tick() / 1000
        if delta_t == 0:
            delta_t = 1e-9

        loop(SCREEN, delta_t, SCREEN_W, SCREEN_H)

        if prm["video_show_fps"]:
            draw_debug_text(str(round(1 / delta_t)), (0, 0))

        if prm["video_show_prm"]:
            draw_parameters(selected)
            selected = handle_parameters(event, selected)

        pygame.display.flip()

def draw_parameters(selected):
    y = 60
    step = 30
    for index, key in enumerate(prm):
        if index == selected:
            draw_debug_text("{}: {}".format(key, prm[key]), (40, y))
        else:
            draw_debug_text("{}: {}".format(key, prm[key]), (10, y))
        y += step

def handle_parameters(event, selected):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected -= 1
        if event.key == pygame.K_DOWN:
            selected += 1
        if event.key == pygame.K_RIGHT:
            for index, key in enumerate(prm):
                if index == selected:
                    prm.increment(key)
        if event.key == pygame.K_LEFT:
            for index, key in enumerate(prm):
                if index == selected:
                    prm.decrement(key)

    return selected
