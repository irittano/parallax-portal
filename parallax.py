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
    images = scene_2d.load_images(screen_s)

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
            for image in images:
                image.draw(eyes_center, screen_s, screen, delta_t)
        #  else:
            # TODO: Kalman

    v.start_loop(loop)

    video_capture.release()
