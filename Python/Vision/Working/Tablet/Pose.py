import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2, Preview
picam2=Picamera2(0)

dispW=640
dispH=320
camera_config = picam2.create_video_configuration({'format': 'RGB888', 'size' : (dispW,dispH)})
picam2.configure(camera_config)
picam2.start()
fps=0
pos=(20,40)
font=cv2.FONT_HERSHEY_DUPLEX
height=1.5
fpsColor=(0,0,255)
weight=(3)
rColor=(0,0,255)

pose=mp.solutions.pose.Pose(False, False, True,True,True)
mpDraw=mp.solutions.drawing_utils

while True:
    tStart=time.time()
    frame=picam2.capture_array()
    frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.putText(frame, str(int(fps))+' FPS', pos, font, height, fpsColor, weight)

    results=pose.process(frameRGB)
    #print(results)
    if results.pose_landmarks != None:
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
    cv2.imshow("picam", frame)

    if cv2.waitKey(1)==ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)