'''
Punto de entrada del programa que integra todo
'''
import numpy as np
import pygame
import cv2
import video
import scene_3d
import scene_2d
import face_detection as fd
from config import prm

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def main():

    # Inicializar video para mostrado en pantalla
    v = video.Video()
    v.set_mode_2d()
    screen_s = np.array(v.screen_size)

    # Inicializar webcam
    video_capture = cv2.VideoCapture(prm["camera_device_index"])
    cam_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    cam_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cam_size = np.array((cam_width, cam_height))

    # Inicializar detector de cara
    face_detector = fd.FaceDetector()

    # Crear imagenes a mostrar
    sprites = [ scene_2d.Image("./res/casa_tucuman_16_9.jpg", 0.5, 1.3, 0.55, screen_s),
                scene_2d.Image("./res/moreno.png", (1.08, 0.8), 0.15, 0.45, screen_s),
                scene_2d.Image("./res/paso.png", (1, 0.8), 0.2, 0.45, screen_s,
                "./res/scroll.png", (2/15,3/15),(1.025, 0.3)),
                scene_2d.Image("./res/larrea.png", (-0.05, 0.85), 0.3, 0.45, screen_s,
                "./res/scroll.png", (13/15,14/15),(-0.05, 0.35)),
                scene_2d.Image("./res/matheu.png", (0.08, 0.8), 0.3, 0.4, screen_s,
                "./res/scroll.png", (12/15,13/15),(0.08, 0.3)),
                scene_2d.Image("./res/alberti.png", (0.85, 0.8), 0.3, 0.35, screen_s,
                "./res/scroll.png", (3/15,4/15),(0.85, 0.3)),
                scene_2d.Image("./res/azcuenaga.png", (0.2, 0.8), 0.3, 0.35, screen_s,
                "./res/scroll.png", (11/15,12/15),(0.2, 0.3)),
                scene_2d.Image("./res/belgrano.png", (0.7, 0.75), 0.3, 0.3, screen_s,
                "./res/scroll.png", (4/15,5/15),(0.7, 0.25)),
                scene_2d.Image("./res/castelli.png", (0.3, 0.75), 0.3, 0.25, screen_s,
                "./res/scroll.png", (10/15,11/15),(0.3, 0.25)),
                scene_2d.Image("./res/saavedra.png", (0.5, 0.9), 0.5, 0.2, screen_s,
                "./res/scroll.png", (7/15,9/15),(0.45, 0.2)),
            ]

    def loop(screen, delta_t, screen_w, screen_h):

        # Obtener frame de video
        _, cam_frame = video_capture.read()

        # No se bien por que pero hay que espejar la imagen para que las
        # coordenadas sean las que esperamos
        cam_frame = cv2.flip(cam_frame, 1)

        # Detectar cara
        face_rect = face_detector.detect(cam_frame)

        # Mostrar pantalla
        screen.fill(COLOR_BLACK)

        if face_rect is not None:
            eyes_center, eyes_distance = fd.face_rect_to_norm(cam_size, face_rect)
            for sprite in sprites:
                sprite.draw_image(eyes_center, screen_s, screen, delta_t)
        #  else:
            # TODO: Kalman

    v.start_loop(loop)

    video_capture.release()
