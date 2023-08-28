import cv2
import time
import os


wCam,hCam = 640,480
dim = (200,200)

cap = cv2.VideoCapture(2)
#cap.set(3, wCam)
#cap.set(4, hCam)


pTime = 0


while True:
    success, img = cap.read()
    cTime = time.time()
    fps = 1/ (cTime- pTime)
    pTime = cTime

    cv2.putText(img,f"FPS : {int(fps)}",(400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)