import cv2
import numpy as np
#import recursos

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)




# ------FLAGS--------
sensb=70000
flag2 = 0
flag1 = 0
k = 0
w1 = 50
h1 = 50
x3 = 200
y3 = 200
contadorinicio = 0
contadorfd = 0
contadorcara=15
img = cv2.imread('camp2.png', -1)

# -----------------------------------------------------------------------------
#       Main program loop
# -----------------------------------------------------------------------------

# collect video input from first webcam on system
video_capture = cv2.VideoCapture(0)
#video_capture.set(3,960)
#video_capture.set(4,720)

while True:
    # Capture video feed

    ret, frame = video_capture.read()

    # Create greyscale image from the video feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        # ---- Detect faces in input video stream -----
    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.2,
        minNeighbors=15,
        minSize=(30, 30),
        #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    #print(faces)
    for (x,y,w,h) in faces:
        face = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = face[y:y+h, x:x+w]
        eye1 = np.array([[int((x+0.35*w)), int((y+0.37*h)), int(w*0.05), int(h*0.05)]])
        eye2 = np.array([[int((x+0.65*w)), int((y+0.37*h)), int(w*0.05), int(h*0.05)]])
        #print(eye1)
        #print(type(faces), type(eye1))
        for (ex,ey,ew,eh) in eye1:
            #cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
            cv2.circle(frame, (ex,ey), ew, (255,255,0),2)
        for (ex, ey, ew, eh) in eye2:
            #cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
            cv2.circle(frame, (ex,ey), ew, (255,255,0),2)
    # Display the resulting frame
    cv2.imshow('Video', frame)
    # press any key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
