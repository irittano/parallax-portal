'''
Funciones relacionadas a pygame para el dibujado de una escena 2D
'''

import video

import pygame

def loop(screen, delta_t, window_w, window_h):

    rect = pygame.Rect((0, 0), (32, 32))
    surf = pygame.Surface((32, 32))
    surf.fill((255, 255, 255))
    screen.blit(surf, rect)

def main(prm, default_prm, args):
    print("Entrado a escena 2D")

    video.init()
    video.set_mode_2d()

    video.start_loop(loop)
