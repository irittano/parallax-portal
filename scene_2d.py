'''
Funciones relacionadas a pygame para el dibujado de una escena 2D
'''

import video

import pygame
import numpy as np


COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

class Imagen:
    '''
    Carga una imagen y le da los valores relevantes para el dibujado
    path = STRING relativo al proyecto, imagenes se encuentran en ./res/.jpg
    draw_position = TUPLE relativo al tamaño de la pantalla
    scaling_factor = TUPLE relación ancho/alto de la imagen
    move_ratio = TUPLE factor de movimiento de la imagen
    '''

    def __init__(self, path, draw_position, scaling_factor, move_ratio, window):
        self.path = path
        self.draw_position = draw_position
        self.scaling_factor = scaling_factor
        self.move_ratio = move_ratio

        self.image = pygame.image.load(path)
        self.scaled_img = pygame.transform.scale(self.image, (window * scaling_factor).astype(int))

    def draw_image(self, mouse, window, screen):
        #Toma el cursor de pygame y las dimensiones de la pantalla en forma
        #de np.array
        position = window * self.draw_position - np.array(self.scaled_img.get_rect().size) / 2
        position = position - self.move_ratio * (mouse - window / 2) #es position + o -?

        screen.blit(self.scaled_img, position)

def main(prm, default_prm, args):
    print("Entrado a escena 2D")
    print("Mover mouse para hacer paralaje")

    video.init()
    video.set_mode_2d()

    window_s = np.array((video.SCREEN_W, video.SCREEN_H))

    casa_rosada = Imagen("./res/casa_tucuman_16_9.jpg", 0.5, 1.3, 0.3, window_s)
    belgrano = Imagen("./res/belgrano.png", (0.2, 0.7), (0.3, 0.7), 0.1, window_s)

    def loop(screen, delta_t, window_w, window_h):

        screen.fill(COLOR_BLACK)
        print(window_s)
        casa_rosada.draw_image(pygame.mouse.get_pos(), window_s, screen)
        belgrano.draw_image(pygame.mouse.get_pos(), window_s, screen)

    video.start_loop(loop)
