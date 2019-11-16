import cv2
import numpy as np
import video
import pygame

from config import prm

class FaceDetector():

    def __init__(self):
        '''
        Inicializa la cámara y la detección

        Devuelve tuple con tamaño de cámara en píxeles
        '''

        cascade_path = "res/haarcascade_frontalface_alt.xml"
        self.faceCascade = cv2.CascadeClassifier(cascade_path)

        # Cara encontrada en el frame anterior
        self.face = None

    def detect(self, frame):
        '''
        Capturar imagen de webcam y detectar caras

        Devuelve rectángulo de OpenCV con parámetros de cara detectada o None si
        no se encontró ninguna cara

        Las unidades devueltas son en píxeles
        '''

        # Convertir imagen a grises
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_height, frame_width = frame.shape

        # Si en el frame anterior se encontraron caras
        if self.face is not None:

            face = self.face
            # Recortar imagen a las proximidades de la cara
            x1 = max(int(face[0]-face[2]*0.2), 0)
            y1 = max(int(face[1]-face[3]*0.2), 0)
            x2 = min(int(face[0]+face[2]*1.2), int(frame_width))
            y2 = min(int(face[1]+face[3]*1.2), int(frame_height))
            width = x2-x1
            height = y2-y1
            crop_img = frame[y1:y1+height, x1:x1+width]

            # Buscar caras sólo en la imagen recortada
            faces = self.faceCascade.detectMultiScale(
                crop_img,
                scaleFactor=prm['face_detection_scale_factor'],
                minNeighbors=prm['face_detection_min_neighbors'],
                minSize=(
                    prm['face_detection_min_size'],
                    prm['face_detection_min_size']
                ),
            )

            # La cara encontrada tiene coordenadas respecto a la imagen
            # recortada, entonces convertimos a las coordenadas que tendría la
            # cara en la imagen completa
            if len(faces) > 0:
                self.face = faces[0]
                self.face[0] += x1
                self.face[1] += y1
            else:
                self.face = None

        # En el frame anterior no se encontró ninguna cara
        else:
            # Buscar caras en la imagen completa
            faces = self.faceCascade.detectMultiScale(
                frame,
                scaleFactor=prm['face_detection_scale_factor'],
                minNeighbors=prm['face_detection_min_neighbors'],
                minSize=(
                    prm['face_detection_min_size'],
                    prm['face_detection_min_size']
                ),
            )

            if len(faces) > 0:
                self.face = faces[0]
            else:
                self.face = None

        return self.face

def face_rect_to_norm(cam_size, face_rect):
    '''
    Convertir rectángulo de cara en píxeles a posición normalizada de cara

    Devuelve un tuple con la posición normalizada de la cara y la distancia
    normalizada entre los ojos
    '''

    x, y, w, h = face_rect
    cam_size = np.array(cam_size)

    # Distancia entre ojos aproximada en píxeles
    eyes_distance = 0.4 * w
    # Coordenadas en píxeles de punto medio entre los dos ojos
    center = np.array((
        int(x + 0.5 * w),
        int(y + 0.37 * h)
    ))

    # Convertir a unidades normalizadas usando el parámetro f de cámara
    norm_eyes_distance = eyes_distance / prm["camera_f"]
    norm_center = (center - cam_size / 2) / prm["camera_f"]

    return norm_center, norm_eyes_distance

def face_rect_to_cm(cam_size, face_rect):
    '''
    Convertir rectángulo de cara en píxeles a posición real tridimensional de la
    cara

    Devuelve un np.ndarray con coordenadas (X, Y, Z) en cm, siendo Z siempre
    positivo
    '''

    norm_center, norm_eyes_distance = face_rect_to_norm(cam_size, face_rect)

    z = prm['eyes_gap'] / norm_eyes_distance,
    x = norm_center[0] * np.float64(z)
    y = -norm_center[1] * np.float64(z) + prm["camera_vertical_distance"]

    return np.array((x, y, z))

def face_rect_draw(frame, face_rect):
    '''
    Dibujar rectangulo de cara sobre frame de OpenCV
    '''
    x, y, w, h = face_rect
    left_eye =(int(x+0.3*w) , int(y+0.37*h))
    right_eye = (int(x+0.7*w), int(y+0.37*h))

    face = cv2.rectangle(frame,(x, y),(x+w,y+h),(255,0,0),2)
    cv2.circle(frame, left_eye, int(0.05*w), (255,255,255), 2)
    cv2.circle(frame, right_eye, int(0.05*w), (255,255,255), 2)
    return frame

def demo():

    # Inicializar video para mostrado en pantalla
    v = video.Video()
    v.set_mode_2d()

    # Inicializar webcam
    video_capture = cv2.VideoCapture(prm["camera_device_index"])
    cam_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    cam_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Inicializar detector de cara
    face_detector = FaceDetector()

    def loop(screen, delta_t, window_w, window_h):

        # Obtener frame de video
        _, cam_frame = video_capture.read()

        # No se bien por que pero hay que espejar la imagen para que las
        # coordenadas sean las que esperamos
        cam_frame = cv2.flip(cam_frame, 1)

        # Detectar caras
        face_rect = face_detector.detect(cam_frame)

        # Dibujar rectangulos sobre caras
        if face_rect is not None:
            face_rect_draw(cam_frame, face_rect)

        # Convertir color, necesario para dibujado en pygame
        cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)

        # Intercambiar filas por columnas de la imagen, necesario para dibujado
        # en pygame
        cam_frame = cam_frame.swapaxes(0,1)

        # Dibujar en pantalla de pygame
        surf = pygame.surfarray.make_surface(cam_frame)
        surf = pygame.transform.scale(surf, (window_w, window_h))
        screen.blit(surf, (0, 0))

    v.start_loop(loop)

    video_capture.release()
