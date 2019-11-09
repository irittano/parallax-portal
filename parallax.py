'''
Punto de entrada del programa que integra todo
'''
import numpy as np
import pygame
import cv2

import queue
import threading

import video
import scene_3d
import scene_2d
import face_detection as fd
import misc
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

    # Inicializar filtro
    pos_filter = misc.PositionFilter()

    # Crear imagenes a mostrar
    images = scene_2d.load_images(screen_s)

    # Cola que permite comunicación entre threads
    # Si está vacía: Significa que el thread de detección no llegó a producir un
    # resultado, el thread principal va a intentar predecir la posición de la
    # cara
    # Si tiene un tuple: Tiene la cara encontrada en el último frame por el
    # thread de detección, el thread principal va a tomarlo y vaciar la cola
    # Si tiene un None: Significa que en el último frame no había cara, el
    # thread principal va a vaciar la cola
    face_queue = queue.Queue(maxsize=1)

    def detection_thread(stop_event, face_queue):
        while not stop_event.is_set():

            # Obtener frame de video
            _, cam_frame = video_capture.read()

            # No se bien por que pero hay que espejar la imagen para que las
            # coordenadas sean las que esperamos
            cam_frame = cv2.flip(cam_frame, 1)

            # Detectar cara
            face_rect = face_detector.detect(cam_frame)

            # Tomar desde la cola para limpiarla en el caso que el thread
            # principal vaya lento y todavía no haya tomado el resultado
            # anterior
            try:
                face_rect = face_queue.get_nowait()
            except queue.Empty:
                pass

            # Colocar nueva detección en la cola
            try:
                face_queue.put_nowait(face_rect)
            except queue.Full:
                # Nunca debería pasar
                print("Error: Detection queue full")


    def main_thread(face_queue):

        def draw_scene_2d(pos, delta_t, screen, screen_s):
            eyes_center = pos[:2]

            for image in images:
                image.draw(eyes_center, screen_s, screen, delta_t)


        def loop(screen, delta_t, screen_w, screen_h):

            # Limpiar pantalla
            screen.fill(COLOR_BLACK)

            # Ver si se procesó un frame de video
            try:
                face_rect = face_queue.get_nowait()

                if face_rect is not None:
                    eyes_center, eyes_distance = fd.face_rect_to_norm(cam_size, face_rect)
                    pos = pos_filter.filter(delta_t,
                            np.array((eyes_center[0], eyes_center[1], 0)))
                    draw_scene_2d(pos, delta_t, screen, screen_s)
                else:
                    pos = pos_filter.predict(delta_t)
                    draw_scene_2d(pos, delta_t, screen, screen_s)

            except queue.Empty:
                pos = pos_filter.predict(delta_t)
                draw_scene_2d(pos, delta_t, screen, screen_s)

        v.start_loop(loop)

    # Usado para indicar al thread de detección que debe parar
    stop_event = threading.Event()

    # Iniciar threads
    main = threading.Thread(target=main_thread,
            args=(face_queue,))
    detect = threading.Thread(target=detection_thread,
            args=(stop_event,face_queue))
    main.start()
    detect.start()

    main.join() # Esperar a que el thread termine (se intente cerrar el programa)
    stop_event.set() # Indicar al thread de detección que debe parar
    detect.join() # Esperar a que el thread de detección termine

    video_capture.release()
