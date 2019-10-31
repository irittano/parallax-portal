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

FONT_SIZE = 20
COLOR_DEBUG_TEXT = np.array((1., 0., 1.))

class Video:

    def __init__(self):
        '''
        Inicializar pygame y OpenGL

        Luego se debe llamar a set_mode_3d() o set_mode_2d()
        '''

        # Si el modo es "2d" o "3d"
        self.mode = None
        # Pantalla de pygame
        self._screen = None
        # Un tuple o np.ndarray con ancho y alto de pantalla
        self.screen_size = None

        pygame.init()
        pygame.font.init()

        # Fuente de pygame usada para debugging solamente en modo 2D
        self.pygame_debug_font = pygame.font.Font(
            pygame.font.get_default_font(), FONT_SIZE)

        glutInit()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_NORMALIZE)

    def set_mode_3d(self):
        '''
        Configurar el modo de video en 3D

        Configura a pygame para usar OpenGL para el dibujado
        '''

        self.mode = "3d"

        if prm["screen_auto_size"]:
            # Supongo que la maxima resolucion es la primera devuelta por pygame
            self.screen_size = pygame.display.list_modes()[0]
        else:
            self.screen_size = (prm["screen_w"], prm["screen_h"])

        self.screen = pygame.display.set_mode(self.screen_size,
            HWSURFACE|DOUBLEBUF|OPENGL)

        # No funciona?
        #  self.screen = pygame.display.set_mode(self.screen_size,
            #  FULLSCREEN|HWSURFACE|DOUBLEBUF|OPENGL)

        glViewport(0, 0, self.screen_size[0], self.screen_size[1])

    def set_mode_2d(self):
        '''
        Configurar el modo de video en 2D

        Configura a pygame para dibujar en 2D estándar en lugar de OpenGL
        '''

        self.mode = "2d"

        if prm["screen_auto_size"]:
            # Supongo que la maxima resolucion es la primera devuelta por pygame
            self.screen_size = pygame.display.list_modes()[0]
        else:
            self.scren_size = (prm["screen_w"], prm["screen_h"])

        self.screen = pygame.display.set_mode(self.screen_size,
            HWSURFACE|DOUBLEBUF)

        # No funciona?
        #  self.screen = pygame.display.set_mode(self.screen_size,
            #  FULLSCREEN|SCALED|HWSURFACE|DOUBLEBUF)

    def start_loop(self, loop):
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

            # Tiempo pasado desde ultimo frame en segundos, si es cero le pongo
            # un valor chico para no tener problemas con divisiones por cero
            delta_t = clock.tick() / 1000
            if delta_t == 0:
                delta_t = 1e-9

            loop(self.screen, delta_t, self.screen_size[0], self.screen_size[1])

            if prm["video_show_fps"]:
                self._draw_debug_text(str(round(1 / delta_t)), (0, 0))

            if prm["video_show_prm"]:
                self._draw_parameters(selected)
                selected = self._handle_parameters(event, selected)

            pygame.display.flip()

    def _draw_debug_text(self, text, position):
        '''
        Dibujar linea de texto, no soporta saltos de linea

        Dar posicion como tuple o np.ndarray en pixeles para esquina superior
        izquierda
        '''
        if self.mode == "2d":

            surface = self.pygame_debug_font.render(
                text, False, COLOR_DEBUG_TEXT * 255)
            self.screen.blit(surface, position)

        elif self.mode == "3d":

            glMatrixMode(GL_PROJECTION);
            glPushMatrix();
            glLoadIdentity();
            gluOrtho2D(0.0, self.screen_size[0], 0.0, self.screen_size[1]);
            glMatrixMode(GL_MODELVIEW);
            glPushMatrix();
            glLoadIdentity();

            glColor3f(*COLOR_DEBUG_TEXT);
            glTranslatef(
                position[0],
                self.screen_size[1] - position[1] - FONT_SIZE, 0
            );

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

    def _draw_parameters(self, selected):
        y = 60
        step = 30
        for index, key in enumerate(prm):
            if index == selected:
                self._draw_debug_text("{}: {}".format(key, prm[key]), (40, y))
            else:
                self._draw_debug_text("{}: {}".format(key, prm[key]), (10, y))
            y += step

    def _handle_parameters(self, event, selected):
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
