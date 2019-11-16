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
from misc import RequestRestartException
from config import prm

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def draw_scene_2d(images, pos, delta_t, screen, screen_s):

    # Convertir de centimetros a posición normalizada
    x, y, z = pos
    face_norm = np.array((
        x / z,
        - y / z
    ))

    for image in images:
        image.draw(face_norm, screen_s, screen, delta_t)

def main():

    # Inicializar webcam
    video_capture = cv2.VideoCapture(prm["camera_device_index"])
    cam_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    cam_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cam_size = np.array((cam_width, cam_height))

    # Cola que permite comunicación entre threads
    # Si está vacía: Significa que el thread de detección no llegó a producir un
    # resultado, el thread principal va a intentar predecir la posición de la
    # cara
    # Si tiene un tuple: Contiene la cara encontrada en el último frame por el
    # thread de detección, el thread principal va a tomarlo y vaciar la cola
    # Si tiene un None: Significa que en el último frame no había cara, el
    # thread principal va a vaciar la cola
    face_queue = queue.Queue(maxsize=1)

    def detection_thread(stop_event, face_queue):

        # Inicializar detector de cara
        face_detector = fd.FaceDetector()

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
                print("Error: Queue de detección llena")

    def main_thread(request_restart_event, face_queue):

        # Inicializar video para mostrado en pantalla
        v = video.Video()

        # Inicializar filtro
        pos_filter = misc.PositionFilter()

        # Declarar variables que mantienen estado, se inicializan en el loop
        scene_3d_obj = None
        scene_2d_images = None
        screen_s = None
        current_video_mode = None

        # Poner un modo cualquiera
        v.set_mode_2d()

        def loop(screen, delta_t, screen_w, screen_h):
            # Variables que mantienen estado
            nonlocal scene_3d_obj
            nonlocal scene_2d_images
            nonlocal screen_s
            nonlocal current_video_mode

            # Si se acaba de pasar de modo 3D a 2D
            if prm['parallax_mode'] == prm.mode_2d \
               and current_video_mode != prm.mode_2d:

                # Configurar el video en modo 2D
                v.set_mode_2d()
                screen_s = np.array(v.screen_size)
                current_video_mode = prm.mode_2d

                # Cargar escena 2D y borrar la escena 3D
                if scene_2d_images == None:
                    scene_2d_images = scene_2d.load_images(screen_s)
                scene_3d_obj = None

            # Si se acaba de pasar de modo 2D a 3D
            if prm['parallax_mode'] == prm.mode_3d \
               and current_video_mode != prm.mode_3d:

                # Configurar el video en modo 3D
                v.set_mode_3d()
                screen_s = np.array(v.screen_size)
                current_video_mode = prm.mode_3d

                # Cargar escena 3D y borrar la escena 2D
                if scene_3d_obj == None:
                    scene_3d_obj = scene_3d.Scene3D(screen_s)
                scene_2d_images = None

            # Limpiar pantalla
            screen.fill(COLOR_BLACK)

            # Ver si se procesó un frame de video, obtener posición de cabeza
            # (detectada o predicha) y si se detectó un salto
            pos = None
            jump_detected = None

            try:
                face_rect = face_queue.get_nowait()
                # El otro thread detectó una cara
                if face_rect is not None:
                    face_pos = fd.face_rect_to_cm(cam_size, face_rect)
                    pos, jump_detected = pos_filter.filter(delta_t, face_pos)
                # El otro thread no detectó ninguna cara
                else:
                    pos = pos_filter.predict(delta_t)
                    jump_detected = False
            # El otro thread no llegó a procesar ningún frame de video
            except queue.Empty:
                pos = pos_filter.predict(delta_t)
                jump_detected = False

            if jump_detected:
                # Change between scene_2d and scene_3d
                prm['parallax_mode'] = not prm['parallax_mode']

            # Dibujar escena 2D
            if prm['parallax_mode'] == prm.mode_2d \
               and scene_2d_images is not None:

                draw_scene_2d(scene_2d_images, pos, delta_t, screen, screen_s)

            # Dibujar escena 3D
            elif prm['parallax_mode'] == prm.mode_3d \
                 and scene_3d_obj is not None:

                scene_3d_obj.loop(delta_t, pos)

        try:
            v.start_loop(loop)
        except RequestRestartException:
            request_restart_event.set()

    # Usado para indicar al thread de detección que debe parar
    stop_event = threading.Event()
    # Usado para que el thread principal solicite reinicio
    request_restart_event = threading.Event()

    # Iniciar threads
    main = threading.Thread(target=main_thread,
            args=(request_restart_event, face_queue))
    detect = threading.Thread(target=detection_thread,
            args=(stop_event,face_queue))
    main.start()
    detect.start()

    main.join() # Esperar a que el thread termine (se intente cerrar el programa)
    stop_event.set() # Indicar al thread de detección que debe parar
    detect.join() # Esperar a que el thread de detección termine}

    video_capture.release()

    if request_restart_event.is_set():
        raise RequestRestartException
