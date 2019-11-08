'''
Punto de entrada del programa que integra todo
'''
import numpy as np
import pygame
import cv2
import video
import scene_3d
import scene_2d
import face_detection
from config import prm

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
PREVIOUS_FACE = None

def main():

    face_detector = face_detection.FaceDetector()
    v = video.Video()
    v.set_mode_2d()

    window_s = np.array(v.screen_size)

    sprites = [ scene_2d.Image("./res/casa_tucuman_16_9.jpg", 0.5, 1.3, 0.55, window_s),
                scene_2d.Image("./res/moreno.png", (1.08, 0.8), 0.15, 0.45, window_s),
                scene_2d.Image("./res/paso.png", (1, 0.8), 0.2, 0.45, window_s,
                "./res/scroll.png", (2/15,3/15),(1.025, 0.3)),
                scene_2d.Image("./res/larrea.png", (-0.05, 0.85), 0.3, 0.45, window_s,
                "./res/scroll.png", (13/15,14/15),(-0.05, 0.35)),
                scene_2d.Image("./res/matheu.png", (0.08, 0.8), 0.3, 0.4, window_s,
                "./res/scroll.png", (12/15,13/15),(0.08, 0.3)),
                scene_2d.Image("./res/alberti.png", (0.85, 0.8), 0.3, 0.35, window_s,
                "./res/scroll.png", (3/15,4/15),(0.85, 0.3)),
                scene_2d.Image("./res/azcuenaga.png", (0.2, 0.8), 0.3, 0.35, window_s,
                "./res/scroll.png", (11/15,12/15),(0.2, 0.3)),
                scene_2d.Image("./res/belgrano.png", (0.7, 0.75), 0.3, 0.3, window_s,
                "./res/scroll.png", (4/15,5/15),(0.7, 0.25)),
                scene_2d.Image("./res/castelli.png", (0.3, 0.75), 0.3, 0.25, window_s,
                "./res/scroll.png", (10/15,11/15),(0.3, 0.25)),
                scene_2d.Image("./res/saavedra.png", (0.5, 0.9), 0.5, 0.2, window_s,
                "./res/scroll.png", (7/15,9/15),(0.45, 0.2)),
            ]

    def loop(screen, delta_t, window_w, window_h):

        face = face_detector.face_detection()
        screen.fill(COLOR_BLACK)
        if face != None:

            eyes_center, w, h = face
            global PREVIOUS_FACE
            PREVIOUS_FACE = eyes_center
            for sprite in sprites:
                # TODO: Cambiar 4 por factor configurable pero dentro de scene_2d, no aca
                sprite.draw_image(np.array(eyes_center), window_s, screen, delta_t)
        else:
            if PREVIOUS_FACE != None:
                for sprite in sprites:
                    sprite.draw_image(np.array(PREVIOUS_FACE), window_s, screen, delta_t)
    v.start_loop(loop)
