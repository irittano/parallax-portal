'''
Funciones relacionadas a pygame para el dibujado de una escena 2D
'''

import video

import pygame
import numpy as np


COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def tuple_add(a, b):
    return tuple(np.add(a, b))

def tuple_sub(a, b):
    return tuple(np.subtract(a, b))

def tuple_prod(a, b):
    return tuple(np.multiply(a, b))

def tuple_div(a, b):
    return tuple(np.divide(a, b))

def main(prm, default_prm, args):
    print("Entrado a escena 2D")
    print("Mover mouse para hacer paralaje")

    video.init()
    video.set_mode_2d()

    image = pygame.image.load("./res/casa_tucuman.jpg")
    image_belgrano = pygame.image.load("./res/belgrano.png")

    def loop(screen, delta_t, window_w, window_h):

        window_s = (window_w, window_h)

        screen.fill(COLOR_BLACK)

        resized_image = pygame.transform.scale(image,
            (int(window_w * 1.2), int(window_h * 1.2)))

        # Center image
        pos = tuple_sub(
            tuple_div(window_s, (2, 2)),
            tuple_div(resized_image.get_rect().size, (2, 2))
        )
        pos = tuple_add(
            pos,
            tuple_prod(
                tuple_sub(
                    pygame.mouse.get_pos(),
                    tuple_div(window_s, (2, 2))
                ),
                (0.3, 0.3)
            )
        )

        screen.blit(resized_image, pos)

        resized_image = pygame.transform.scale(image_belgrano,
            (int(window_w * 0.3), int(window_h * 0.7)))
        pos = tuple_div(window_s, (9, 2))
        pos = tuple_add(
            pos,
            tuple_prod(
                tuple_sub(
                    pygame.mouse.get_pos(),
                    tuple_div(window_s, (2, 2))
                ),
                (0.1, 0.1)
            )
        )
        screen.blit(resized_image, pos)

    video.start_loop(loop)
