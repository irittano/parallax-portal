import cv2
import numpy as np
import video
import pygame

from config import prm

class FaceDetector():

    def __init__(self):
        '''
        Inicializa la cámara y la detección
        '''

        self.video_capture = cv2.VideoCapture(prm["camera_device_index"])
        self.cam_width = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cam_height = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        cascade_path = "res/haarcascade_frontalface_alt.xml"
        self.faceCascade = cv2.CascadeClassifier(cascade_path)

        # Lista de caras encontradas en el frame anterior
        self.faces = []

    def face_detection(self, modo = False):

        ret, frame = self.video_capture.read()

        # El flip es porque estaba mal el eje de coordenadas
        frame = cv2.flip(frame,1)

        # Si en el frame anterior se encontraron caras
        if len(self.faces) > 0:

            # Recortar imagen a las proximidades de la cara
            face = self.faces[0]
            x1 = max(int(face[0]-face[2]*0.2), 0)
            y1 = max(int(face[1]-face[3]*0.2), 0)
            x2 = min(int(face[0]+face[2]*1.2), int(self.cam_width))
            y2 = min(int(face[1]+face[3]*1.2), int(self.cam_height))
            width = x2-x1
            height = y2-y1
            crop_img = frame[y1:y1+height, x1:x1+width]

            # Buscar caras sólo en la imagen recortada
            self.faces = self.faceCascade.detectMultiScale(
                crop_img,
                scaleFactor=1.2,
                minNeighbors=15,
                minSize=(50, 50),
            )

            # La cara encontrada tiene coordenadas respecto a la imagen
            # recortada, entonces convertimos a las coordenadas que tendría la
            # cara en la imagen completa
            if len(self.faces) > 0:
                self.faces[0][0] += x1
                self.faces[0][1] += y1

        # En el frame anterior no se encontró ninguna cara
        else:
            # Buscar caras en la imagen completa
            self.faces = self.faceCascade.detectMultiScale(
                frame,
                scaleFactor=1.2,
                minNeighbors=15,
                minSize=(50, 50),
            )

        # TODO: Emprolijar
        if modo == False:

            for (x, y, w, h) in self.faces:
                left_eye = (int(x+0.30*w), int(y+0.37*h))
                right_eye = (int(x+0.70*w), int(y+0.37*h))
                eyes_center = (int(x+0.5*w), int(y+0.37*h))

                normRightEye = (right_eye[0] - self.cam_width/2)/prm["camera_f"]
                normLeftEye = (left_eye[0] - self.cam_width/2)/prm["camera_f"]
                normCenterX = (eyes_center[0] - self.cam_width/2)/prm["camera_f"]
                normCenterY = (eyes_center[1] - self.cam_height/2)/prm["camera_f"]

                # Obtener coodenadas espaciales
                tempZ = prm["eyes_gap"]/(normRightEye - normLeftEye)
                tempX = normCenterX*tempZ
                # Suponiendo webcam ubicada arriba a 1cm del borde superior
                # TODO: Cambiar nombre a prm
                tempY = -normCenterY*tempZ + prm["distance_camera_screen"]

                return (normCenterX, normCenterY), w, h
        else:
            if len(self.faces) == 0:
                return frame

            else:
                face = self.faces[0]
                x = int(face[0])
                y = int(face[1])
                a = int(face[2])
                h = int(face[3])
                left_eye =(int(x+0.3*a) , int(y+0.37*h))
                right_eye = (int(x+0.7*a), int(y+0.37*h))

                face = cv2.rectangle(frame,(x, y),(x+a,y+h),(255,0,0),2)
                cv2.circle(frame, left_eye, int(0.05*a), (255,255,255), 2)
                cv2.circle(frame, right_eye, int(0.05*a), (255,255,255), 2)
                return frame

    def __del__(self):

        self.video_capture.release()
        cv2.destroyAllWindows()

def demo():

    face_detector = FaceDetector()

    while True:

        frame = face_detector.face_detection(modo = True)
        cv2.imshow('Video', cv2.flip(frame,1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
