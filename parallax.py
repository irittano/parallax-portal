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
    eyes_center = pos[:2]

    for image in images:
        image.draw(eyes_center, screen_s, screen, delta_t)

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

        state = {
            'scene_3d_obj': None,
            'scene_2d_images': None,
            'screen_s': None,
            'current_video_mode': None,
        }

        v.set_mode_2d()

        def loop(state, screen, delta_t, screen_w, screen_h):
            scene_3d_obj = state['scene_3d_obj']
            scene_2d_images = state['scene_2d_images']
            screen_s = state['screen_s']
            current_video_mode = state['current_video_mode']

            # Si se acaba de pasar de modo 3D a 2D
            if prm['parallax_mode'] == prm.mode_2d \
               and current_video_mode != prm.mode_2d:

                # Configurar el video en modo 2D
                v.set_mode_2d()
                screen_s = np.array(v.screen_size)
                current_video_mode = prm.mode_2d

                # Reiniciar el filtro de Kalman, porque estamos cambiando
                # unidades
                pos_filter.reset()

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

                # Reiniciar el filtro de Kalman, porque estamos cambiando
                # unidades
                pos_filter.reset()

                # Cargar escena 3D y borrar la escena 2D
                if scene_3d_obj == None:
                    scene_3d_obj = scene_3d.Scene3D(screen_s)
                scene_2d_images = None

            # Limpiar pantalla
            screen.fill(COLOR_BLACK)

            # Dibujar escena 2D
            if prm['parallax_mode'] == prm.mode_2d \
               and scene_2d_images is not None:

                # Ver si se procesó un frame de video
                try:
                    face_rect = face_queue.get_nowait()

                    # El otro thread detectó una cara
                    if face_rect is not None:
                        eyes_center, eyes_distance = fd.face_rect_to_norm(cam_size, face_rect)
                        pos, jump_detected = pos_filter.filter(delta_t,
                                np.array((eyes_center[0], eyes_center[1], 0)))
                        if jump_detected:
                            prm['parallax_mode'] = prm.mode_3d
                        draw_scene_2d(scene_2d_images, pos, delta_t, screen, screen_s)

                    # El otro thread no detectó ninguna cara
                    else:
                        pos = pos_filter.predict(delta_t)
                        draw_scene_2d(scene_2d_images, pos, delta_t, screen, screen_s)

                # El otro thread no llegó a procesar ningún frame de video
                except queue.Empty:
                    pos = pos_filter.predict(delta_t)
                    draw_scene_2d(scene_2d_images, pos, delta_t, screen, screen_s)

            # Dibujar escena 3D
            elif prm['parallax_mode'] == prm.mode_3d \
                 and scene_3d_obj is not None:

                # Ver si se procesó un frame de video
                try:
                    face_rect = face_queue.get_nowait()

                    # El otro thread detectó una cara
                    if face_rect is not None:
                        face_pos = fd.face_rect_to_cm(cam_size, face_rect)
                        pos, jump_detected = pos_filter.filter(delta_t, face_pos)
                        if jump_detected:
                            prm['parallax_mode'] = prm.mode_2d
                        scene_3d_obj.loop(delta_t, pos)

                    # El otro thread no detectó ninguna cara
                    else:
                        pos = pos_filter.predict(delta_t)
                        scene_3d_obj.loop(delta_t, pos)

                # El otro thread no llegó a procesar ningún frame de video
                except queue.Empty:
                    pos = pos_filter.predict(delta_t)
                    scene_3d_obj.loop(delta_t, pos)

            # TODO dejar de usar este diccionario de state
            state['scene_3d_obj'] = scene_3d_obj
            state['scene_2d_images'] = scene_2d_images
            state['screen_s'] = screen_s
            state['current_video_mode'] = current_video_mode

        try:
            # TODO dejar de usar este diccionario de state
            v.start_loop(lambda screen, delta_t, screen_w, screen_h: loop(state, screen, delta_t, screen_w, screen_h))
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
