import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2, Preview
import tkinter as tk
import pickle
picam2=Picamera2(1)

dispW=720
dispH=480
camera_config = picam2.create_video_configuration({'format': 'RGB888', 'size' : (dispW,dispH)})
picam2.configure(camera_config)
picam2.start()
fps=0
pos=(15,100)
font=cv2.FONT_HERSHEY_DUPLEX
height=1
fpsColor=(0,0,255)
weight=(2)
rColor=(0,0,255)


mp_pose=mp.solutions.pose
mpDraw=mp.solutions.drawing_utils
jabcounter=0
crosscounter=0
lUcutcounter=0
rUcutcounter=0
lKneecounter=0
rKneecounter=0
lKickcounter=0
rKickcounter=0
lTeepcounter=0
rTeepcounter=0
stance=None
velocity=0
jabVel=0
crossVel=0
lKneeVel=0
rKneeVel=0
lAnlkeVel=0
rAnkleVel=0
#cv2.namedWindow('Tracker')


def calculate_angle(a,b,c):
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)
    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle=360-angle
    return angle

def calc_vel(d):
    d=np.array(d)
    t=(tEnd-tStart)*1000
    velocity=((d[1]-d[0]))/t
    roundedV=round(velocity)
    if velocity > 0:
        return roundedV

with mp_pose.Pose(min_detection_confidence=.5,min_tracking_confidence=.5) as pose:
    while True:
        tStart=time.time()
        frame=picam2.capture_array()
        #fullscreen=cv2.namedWindow(frame,cv2.WND_PROP_FULLSCREEN)
        frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #frameRGB.flags.writeable=False
        cv2.putText(frame, str(int(fps))+'FPS', pos, font, height, fpsColor, weight)
        results=pose.process(frameRGB)
        
        #window=tk.Tk()
        #window.geometry("360x240")
        #T=tk.Text(window, height=10, width= 60)
        #jabLabel=tk.Label(window,text="Jabs: ")
        #crossLabel=tk.Label(window,text="Cross: ")
        #leftKickLabel=tk.Label(window, text="Left Kick: ")
        #rightKickLabel=tk.Label(window, text="Right Kick: ")
        #leftKneeLabel=tk.Label(window,text="Left Knee: ")
        #rightKneeLabel=tk.Label(window,text="Right Knee: ")
        #jabLabel.pack()
        #crossLabel.pack()
        #leftKickLabel.pack()
        #rightKickLabel.pack()
        #leftKneeLabel.pack()
        #rightKneeLabel.pack()
        #T.insert(tk.END,jabcounter) 
        #labelFrame=tk.Frame(window)

        
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
            lToe=[landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
            rShoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            rElbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            rWrist=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            rHip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            rKnee=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            rAnkle=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            rToe=[landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]


            lArmAngle=calculate_angle(lShoulder,lElbow,lWrist)
            rArmAngle=calculate_angle(rShoulder,rElbow,rWrist)
            lArmPitAngle=calculate_angle(lHip,lShoulder,lElbow)
            rArmPitAngle=calculate_angle(rHip,rShoulder,rElbow)
            lKneeAngle=calculate_angle(lHip,lKnee,lAnkle)
            rKneeAngle=calculate_angle(rHip,rKnee,rAnkle)
            lTeepAngle=calculate_angle(lToe,lHip,rAnkle)
            rTeepAngle=calculate_angle(rToe,rHip,lAnkle)
            lKickAngle=calculate_angle(lToe,lHip,lShoulder)
            rKickAngle=calculate_angle(rToe,rHip,rShoulder)
            groinAngle=calculate_angle(lKnee,lHip,rKnee)
            jabVel=calc_vel(lWrist)
            crossVel=calc_vel(rWrist)
            lKneeVel=calc_vel(lKnee)
            rKneeVel=calc_vel(rKnee)
            lAnlkeVel=calc_vel(lAnkle)
            rAnkleVel=calc_vel(rAnkle)


            #Show angle
            #cv2.putText(frameRGB,str(lAngle), tuple(np.multiply(lElbow,[dispW,dispH]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),2,cv2.LINE_AA)
            #cv2.putText(frameRGB,str(rAngle), tuple(np.multiply(rElbow,[dispW,dispH]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),2,cv2.LINE_AA)
#Boxing
            if 180 > lArmAngle > 130:
                stance="jab"
            if lArmAngle < 30 and stance=="jab":
                stance="guard"
                jabcounter +=1
                print(jabcounter)
            if 180 > rArmAngle > 130:
                stance="cross"
            if rArmAngle < 30 and stance=="cross":
                stance="guard"
                crosscounter +=1
                print(crosscounter)
        #    if lArmAngle < 90 and :
        #        stance="Left Uppercut"
        #    if lArmAngle and stance=="Left Uppercut":
        #        stance="guard"
        #        lUcutcounter +=1
        #        print(lUcutcounter)
        #    if rArmAngle and :
        #        stance="Right Uppercut"
        #    if rArmAngle and stance=="Right Uppercut"            
#Muay Thai

            if 70 >= lKneeAngle >= 10:
                stance="Left Knee"
            if lKneeAngle > 120 and stance=="Left Knee":
                stance="guard"
                lKneecounter +=1
                print(lKneecounter)
            if 70 >= rKneeAngle >= 10:
                stance="Right Knee"
            if rKneeAngle > 120 and stance=="Right Knee":
                stance="guard"
                rKneecounter +=1
                print(rKneecounter)
            if 180 >= lTeepAngle >= 130:
                stance="Left Teep"
            if lTeepAngle < 60 and stance=="Left Teep":
                stance="guard"
                lTeepcounter +=1
                print(lTeepcounter)             
            if 180 >= rTeepAngle >= 130:
                stance="Right Teep"
            if rTeepAngle < 60 and stance=="Righ Teep":
                stance="guard"
                rTeepcounter +=1
                print(rTeepcounter)
            if lKickAngle <= 90 and groinAngle >= 90:
                stance="Left Kick"
            if lKickAngle > 110 and stance=="Left Kick":
                stance="guard"
                lKickcounter +=1
                print(lKickcounter)
            if rKickAngle <=90 and groinAngle >= 90:
                stance="Right Kick"
            if rKickAngle >110 and stance=="Right Kick":
                stance="guard"
                rKickcounter +=1
                print(rKickcounter)            
   
        except:
            pass
        #Status box
        #cv2.rectangle(frame,(0,0),(dispW-180,70), (225,25,55), -1)
        #Reps
        #score=cv2.namedWindow('Score')
        cv2.putText(frame,'Jab:'+str(jabcounter)+ ' Vel: '+str(jabVel),(15,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(jabcounter),(50,25),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Cross:'+str(crosscounter)+ ' Vel: '+str(crossVel),(15,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)        
        #cv2.putText(frame,str(crosscounter),(70,55),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Left Knee:'+str(lKneecounter)+ ' Vel: '+str(lKneeVel),(200,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(lKneecounter),(10,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Right Knee:'+str(rKneecounter)+ ' Vel: '+str(rKneeVel),(200,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(rKneecounter),(10,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,'Left Teep:'+str(lTeepcounter),(280,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(lKickcounter),(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,'Right Teep:'+str(rTeepcounter),(280,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,str(rKickcounter),(10,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
    #    cv2.putText(frame,'Left Uppercut:'+str(lUcutcounter),(280,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
    #    cv2.putText(frame,'Right Uppercut:'+str(rUcutcounter),(280,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Left Kick:'+str(lKickcounter)+ ' Vel: '+str(lAnlkeVel),(400,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Right Kick:'+str(rKickcounter)+ ' Vel: '+str(rAnkleVel),(400,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)

        #Stance
        cv2.putText(frame,"Stance: " + str(stance),(10,60),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame,stance,(520,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        #print(jabVel)
        if results.pose_landmarks != None:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        cv2.imshow("picam", frame)

        if cv2.waitKey(1)==ord('q'):
            break
        tEnd=time.time()
        loopTime=tEnd-tStart
        fps=.9*fps + .1*(1/loopTime)

