import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2, Preview
import pickle
picam2=Picamera2(0)

dispW=720
dispH=480
camera_config = picam2.create_video_configuration({'format': 'RGB888', 'size' : (dispW,dispH)})
picam2.configure(camera_config)
picam2.start()
fps=0
pos=(dispW-150,30)
font=cv2.FONT_HERSHEY_DUPLEX
height=1
fpsColor=(0,0,255)
weight=(3)
rColor=(0,0,255)


mp_pose=mp.solutions.pose
mpDraw=mp.solutions.drawing_utils
jabcounter=0
crosscounter=0
stance=None
def calculate_angle(a,b,c):
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)
    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle=360-angle
    return angle

with mp_pose.Pose(min_detection_confidence=.5,min_tracking_confidence=.5) as pose:
    while True:
        tStart=time.time()
        frame=picam2.capture_array()
        frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #frameRGB.flags.writeable=False
        cv2.putText(frame, str(int(fps))+' FPS', pos, font, height, fpsColor, weight)
        results=pose.process(frameRGB)
    #    if results.pose_landmarks != None:
    #        mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        try:
            landmarks=results.pose_landmarks.landmark
            #print(landmarks)
            lShoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            lElbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            lWrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            rShoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            rElbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            rWrist=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            lAngle=calculate_angle(lShoulder,lElbow,lWrist)
            rAngle=calculate_angle(rShoulder,rElbow,rWrist)
            #Show angle
            #cv2.putText(frameRGB,str(lAngle), tuple(np.multiply(lElbow,[dispW,dispH]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),2,cv2.LINE_AA)
            #cv2.putText(frameRGB,str(rAngle), tuple(np.multiply(rElbow,[dispW,dispH]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),2,cv2.LINE_AA)

            if lAngle > 160:
                stance="jab"
            if lAngle < 30 and stance=="jab":
                stance="guard"
                jabcounter +=1
                print(jabcounter)
            if rAngle > 160:
                stance="cross"
            if rAngle < 30 and stance=="cross":
                stance="guard"
                crosscounter +=1
                print(crosscounter)

                
            
        except:
            pass
        #Status box
        cv2.rectangle(frame,(0,0),(dispW-180,70), (225,25,55), -1)
        #Reps
        cv2.putText(frame,'Jab',(15,12),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,str(jabcounter),(10,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(frame,'Cross',(100,12),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)        
        cv2.putText(frame,str(crosscounter),(80,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)

        #Stance
        cv2.putText(frame,"Stance",(200,12),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,0),1,cv2.LINE_AA)
        cv2.putText(frame,stance,(200,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
        
        if results.pose_landmarks != None:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        cv2.imshow("picam", frame)

        if cv2.waitKey(1)==ord('q'):
            break
        tEnd=time.time()
        loopTime=tEnd-tStart
        fps=.9*fps + .1*(1/loopTime)
