import cv2
import numpy as np
import video
import pygame


def main(prm, default_prm, args):

    eyesGap = 6.5

    video_capture = cv2.VideoCapture(0)

    #cam_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    #cam_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while True:

        ret, frame = video_capture.read()
        face_detection(frame, modo = True)

        cv2.imshow('Video', cv2.flip(frame,1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def face_detection(frame, modo = False):

    cascPath = "res/haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.2,
        minNeighbors=15,
        minSize=(50, 50),
        #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    if modo == False:

        for (x, y, w, h) in faces:
            left_eye = (int(x+0.30*w), int(y+0.37*h))
            right_eye = (int(x+0.70*w), int(y+0.37*h))
            eyes_center = (int(x+0.5*w), int(y+0.37*h))
            return eyes_center, w, h

    else:

        for (x, y, w, h) in faces:
            face = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            left_eye = (int(x+0.30*w), int(y+0.37*h))
            right_eye = (int(x+0.70*w), int(y+0.37*h))

            cv2.circle(frame, (left_eye), int(0.05*w), (255,255,255),2)
            cv2.circle(frame, (right_eye), int(0.05*w), (255,255,255),2)

            return frame
