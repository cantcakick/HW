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

class Striking:



    def counter(self,incr=False):
        count=0
        if incr==True:
            count+=1
    def jab(self, lArmAngle, stance=None,jabcounter=0):
        jabcounter=0
        if 180>lArmAngle>120:
            stance='jab'
        if lArmAngle<30 and stance=='jab':
            stance='guard'
            jabcounter+=1
            print(jabcounter)
    def cross(self, rArmAngle, stance=None,crosscounter=0):
        
        if 180> rArmAngle >120:
            stance='cross'
        if rArmAngle<30 and stance=='cross':
            stance='guard'
            crosscounter+=1    
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
    if velocity > 0.1:
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

        try:
            landmarks=results.pose_landmarks.landmark
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
            lTeepAngle=calculate_angle(lAnkle,lHip,lShoulder)
            rTeepAngle=calculate_angle(rAnkle,rHip,rShoulder)
            lKickAngle=calculate_angle(lToe,lHip,lShoulder)
            rKickAngle=calculate_angle(rToe,rHip,rShoulder)
            groinAngle=calculate_angle(lKnee,lHip,rKnee)
            jabVel=calc_vel(lWrist)
            crossVel=calc_vel(rWrist)
            lKneeVel=calc_vel(lKnee)
            rKneeVel=calc_vel(rKnee)
            lAnlkeVel=calc_vel(lAnkle)
            rAnkleVel=calc_vel(rAnkle)

        except:
            pass
        numJab=str(Striking.jab)
        cv2.putText(frame,"Jab: "+numJab,(100,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)

        if results.pose_landmarks != None:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        cv2.imshow("picam", frame)

        if cv2.waitKey(1)==ord('q'):
            break
        tEnd=time.time()
        loopTime=tEnd-tStart
        fps=.9*fps + .1*(1/loopTime)
