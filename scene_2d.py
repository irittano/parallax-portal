'''
Funciones relacionadas a pygame para el dibujado de una escena 2D
'''

import video

import pygame
import numpy as np

from config import prm

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

class Image:
    '''
    Carga una imagen y le da los valores relevantes para el dibujado
    path = STRING relativo al proyecto, imagenes se encuentran en ./res/.jpg
    draw_pos = TUPLE relativo al tamaño de la pantalla
    scaling_factor = FLOAT ancho de la imagen, mantiene relacion w:h
    move_ratio = FLOAT factor de movimiento de la imagen
    scroll_path = STRING relativo al proyecto, imagen de descripcion del procer
    x_threshold = TUPLE (min,max) num entre 0-1 porcentaje de la pantalla
    scroll_pos = TUPLE relativo al tamaño de la pantalla, similar a draw_pos
    '''

    def __init__(
        self,
        path,
        draw_pos,
        scaling_factor,
        move_ratio,
        window, scroll_path = None, x_threshold = None, scroll_pos = None
    ):
        self.path = path
        self.draw_pos = draw_pos
        self.scaling_factor = scaling_factor
        self.move_ratio = move_ratio
        self.scroll_path = scroll_path
        self.x_threshold = x_threshold
        self.scroll_pos = scroll_pos

        if (scroll_path):
            scroll = pygame.image.load("./res/scroll.png").convert_alpha()
            scroll_w = window[0] * 0.15
            scroll_h = ( scroll_w / scroll.get_rect().size[0] ) * scroll.get_rect().size[1]
            self.scaled_scroll = pygame.transform.scale(scroll, (int(scroll_w),int(scroll_h)))
        else:
            pass

        image = pygame.image.load(path).convert_alpha()
        w = window[0] * scaling_factor
        h = ( w / image.get_rect().size[0] ) * image.get_rect().size[1]
        self.scaled_img = pygame.transform.scale(image, (int(w), int(h)))

    def draw_image(self, mouse, window, screen):
        #Toma el cursor de pygame y las dimensiones de la pantalla en forma
        #de np.array
        centered_position = window * self.draw_pos - np.array(self.scaled_img.get_rect().size) / 2
        position = centered_position + self.move_ratio * (mouse - window / 2) #es position + o -?

        screen.blit(self.scaled_img, position)

        if (self.x_threshold):
            if ( self.x_threshold[0] * window[0] < mouse[0] < self.x_threshold[1] * window[0] ):
                centered_position = window * self.scroll_pos - np.array(self.scaled_scroll.get_rect().size) / 2
                position = centered_position + self.move_ratio * (mouse - window / 2)

                screen.blit(self.scaled_scroll, position)
        else:
            pass

def demo():
    print("Entrado a escena 2D")
    print("Mover mouse para hacer paralaje")

    v = video.Video()
    v.set_mode_2d()

    window_s = np.array(v.screen_size)


    sprites = [ Image("./res/casa_tucuman_16_9.jpg", 0.5, 1.3, 0.55, window_s),
                Image("./res/moreno.png", (1.08, 0.8), 0.15, 0.45, window_s),
                Image("./res/paso.png", (1, 0.8), 0.2, 0.45, window_s,
                "./res/scroll.png", (2/15,3/15),(1.025, 0.3)),
                Image("./res/larrea.png", (-0.05, 0.85), 0.3, 0.45, window_s,
                "./res/scroll.png", (13/15,14/15),(-0.05, 0.35)),
                Image("./res/matheu.png", (0.08, 0.8), 0.3, 0.4, window_s,
                "./res/scroll.png", (12/15,13/15),(0.08, 0.3)),
                Image("./res/alberti.png", (0.85, 0.8), 0.3, 0.35, window_s,
                "./res/scroll.png", (3/15,4/15),(0.85, 0.3)),
                Image("./res/azcuenaga.png", (0.2, 0.8), 0.3, 0.35, window_s,
                "./res/scroll.png", (11/15,12/15),(0.2, 0.3)),
                Image("./res/belgrano.png", (0.7, 0.75), 0.3, 0.3, window_s,
                "./res/scroll.png", (4/15,5/15),(0.7, 0.25)),
                Image("./res/castelli.png", (0.3, 0.75), 0.3, 0.25, window_s,
                "./res/scroll.png", (10/15,11/15),(0.3, 0.25)),
                Image("./res/saavedra.png", (0.5, 0.9), 0.5, 0.2, window_s,
                "./res/scroll.png", (7/15,9/15),(0.45, 0.2)),
            ]

    def loop(screen, delta_t, window_w, window_h):

        screen.fill(COLOR_BLACK)
        for sprite in sprites:
            sprite.draw_image(pygame.mouse.get_pos(), window_s, screen)

    v.start_loop(loop)
