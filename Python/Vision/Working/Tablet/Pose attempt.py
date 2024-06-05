import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2, Preview

class mpPose:
    import mediapipe as mp
    def __init__(self,still=False,upperBody=False,smoothData=True):
        self.myPose=self.mp.solutions.pose.Pose(still,upperBody,smoothData)
    def Marks(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.myPose.process(frameRGB)
        poseLandmarks=[]
        if results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:
                poseLandmarks.append((int(lm.x*dispW),int(lm.y*dispH)))
            return poseLandmarks
picam2=Picamera2(0)
dispW=720
dispH=480
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

findPose=mpPose()
pose=mp.solutions.pose.Pose(False, False, True,True,True)
mpDraw=mp.solutions.drawing_utils

while True:
    tStart=time.time()
    frame=picam2.capture_array(0)
    frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.putText(frame, str(int(fps))+' FPS', pos, font, height, fpsColor, weight)

    poseData=findPose.Marks(frame)
    if len(poseData)!=0:
        cv2.circle(frame,poseData[0],5,(0,255,0),3)
    
    results=pose.process(frameRGB)
    print(results)
    if results.pose_landmarks != None:
       mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
    cv2.imshow("picam pose", frame)

    if cv2.waitKey(1)==ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)
cv2.destroyAllWindows()