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
pos=(dispW-100,25)
font=cv2.FONT_HERSHEY_DUPLEX
height=1
fpsColor=(0,0,255)
weight=(2)
rColor=(0,0,255)


mp_pose=mp.solutions.pose
mpDraw=mp.solutions.drawing_utils
jabcounter=0
crosscounter=0
lKneecounter=0
rKneecounter=0
lKickcounter=0
rKickcounter=0
lTeepcounter=0
rTeepcounter=0
lUppercut=0
rUppercut=0
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
        #fullscreen=cv2.namedWindow(frame,cv2.WND_PROP_FULLSCREEN)
        frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #frameRGB.flags.writeable=False
        cv2.putText(frame, str(int(fps))+'FPS', pos, font, height, fpsColor, weight)
        results=pose.process(frameRGB)
    #    if results.pose_landmarks != None:
    #        mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        try:
            landmarks=results.pose_landmarks.landmark
            #print(landmarks)
            head=[landmarks[mp_pose.PoseLandmark.NOSE.value].x,landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            lShoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            lElbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            lWrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            lHip=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            lKnee=[landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            lAnkle=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            rShoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            rElbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            rWrist=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            rHip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            rKnee=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            rAnkle=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            lToe=[landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
            rToe=[landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]


            lArmAngle=calculate_angle(lShoulder,lElbow,lWrist)
            rArmAngle=calculate_angle(rShoulder,rElbow,rWrist)
            lKneeAngle=calculate_angle(lHip,lKnee,lAnkle)
            rKneeAngle=calculate_angle(rHip,rKnee,rAnkle)
            lTeepAngle=calculate_angle(lToe,lHip,rAnkle)
            rTeepAngle=calculate_angle(rToe,rHip,lAnkle)
            #Show angle
            #cv2.putText(frameRGB,str(lAngle), tuple(np.multiply(lElbow,[dispW,dispH]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),2,cv2.LINE_AA)
            #cv2.putText(frameRGB,str(rAngle), tuple(np.multiply(rElbow,[dispW,dispH]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),2,cv2.LINE_AA)

            if lArmAngle >= 130:
                stance="jab"
            if lArmAngle < 50 and stance=="jab":
                stance="guard"
                jabcounter +=1
                print(jabcounter)
            if rArmAngle >= 130:
                stance="cross"
            if rArmAngle < 50 and stance=="cross":
                stance="guard"
                crosscounter +=1
                print(crosscounter)
            if lKneeAngle <= 70:
                stance="Left Knee"
            if lKneeAngle > 80 and stance=="Left Knee":
                stance="guard"
                lKneecounter +=1
                print(lKneecounter)
            if rKneeAngle <= 60:
                stance="Right Knee"
            if rKneeAngle > 70 and stance=="Right Knee":
                stance="guard"
                rKneecounter +=1
                print(rKneecounter)
            if lTeepAngle >= 90:
                stance="Kick"
            if lTeepAngle < 60 and stance=="Left Teep":
                stance="guard"
                lTeepcounter +=1
                print(lTeepcounter)             
            if rTeepAngle >= 90:
                stance="cross"
            if rTeepAngle < 60 and stance=="Righ Kick":
                stance="guard"
                rTeepcounter +=1
                print(rTeepcounter)
  
            
            
        except:
            pass
        #Status box
        #cv2.rectangle(frame,(0,0),(dispW-180,70), (225,25,55), -1)
        #Reps
        #score=cv2.namedWindow('Score')
        cv2.putText(frame,'Jab:'+str(jabcounter),(15,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(jabcounter),(50,25),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Cross:'+str(crosscounter),(15,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)        
        #cv2.putText(frame,str(crosscounter),(70,55),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Left Knee:'+str(lKneecounter),(120,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(lKneecounter),(10,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Right Knee:'+str(rKneecounter),(120,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(rKneecounter),(10,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Left Teep:'+str(lTeepcounter),(280,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(lKickcounter),(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Right Teep:'+str(rTeepcounter),(280,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(rKickcounter),(10,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)

        #Stance
        cv2.putText(frame,"Stance",(520,12),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,stance,(520,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        
        if results.pose_landmarks != None:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        cv2.imshow("picam", frame)

        if cv2.waitKey(1)==ord('q'):
            break
        tEnd=time.time()
        loopTime=tEnd-tStart
        fps=.9*fps + .1*(1/loopTime)
