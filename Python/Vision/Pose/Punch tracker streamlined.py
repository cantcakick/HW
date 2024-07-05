import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2, Preview
import tkinter as tk
import pickle
picam2=Picamera2(0)

class calcAngle:
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


    

class lm():
    mp_pose=mp.solutions.pose
    mpDraw=mp.solutions.drawing_utils
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
    def counter():
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