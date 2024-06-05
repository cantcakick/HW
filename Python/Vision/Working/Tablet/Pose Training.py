import cv2
import time
import numpy as np
import mediapipe as mp
import pickle
from picamera2 import Picamera2, Preview

def findPose(unknownPose,knownPose,pose,poseNames,tol):
    errorArray=[]
    for i in range(0, len(poseNames),1):
        error=findError()

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

pose=mp.solutions.pose.Pose(False, False, True,True,True)
mpDraw=mp.solutions.drawing_utils

train=int(input('Enter 1 to train, Enter 0 to run '))
if train==1:
    trainCount=0
    knownPoses=[]
    numPoses=int(input('How many poses do you want to train? '))
    poseNames=[]
    for i in range(0,numPoses,1):
        prompt='Name of Pose #'+str(i+1)+' '
        name=input(prompt)
        poseNames.append(name)
    print(poseNames)
    trainFile=input('Enter training data file.  Press Enter for Default')
    if trainFile=='':
        trainFile='Default'
        trainFile=trainFile+'.pkl'
        with open(trainFile, 'rb') as f:
            poseNames=pickle.load(f)
            knownPoses=pickle.load(f)
            
total=10

while True:
    tStart=time.time()
    frame=picam2.capture_array()
    frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.putText(frame, str(int(fps))+' FPS', pos, font, height, fpsColor, weight)

    results=pose.process(frameRGB)
    #print(results)
    if train == 1:
        if results.pose_landmarks != None:
            mpDraw.draw_landmarks(frame, pose, mp.solutions.pose.POSE_CONNECTIONS)
            print('Please show pose',poseNames[trainCount],': Press s to Start')
            if cv2.waitKey(1) & 0xff==ord('s'):
                knownPose=pose
                knownPoses.append(knownPose)
                trainCount=trainCount+1
                if trainCount==numPoses:
                    train=0
                    with open(trainFile,'wb') as f:
                        pickle.dump(poseNames,f)
                        pickle.dump(knownPoses,f)
    #if train == 0:
    #    if results.pose_landmarks != None:
    #        unknownPose=0
    #        myPose=findPose(unknownPose,knownPose,results.pose_landmarks,poseNames,tol)
    
    cv2.imshow("picam pose", frame)
    if cv2.waitKey(1)==ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)
cv2.destroyAllWindows()