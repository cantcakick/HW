import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2, Preview
picam2=Picamera2(0)

class mpFaceMesh:
    import mediapipe as mp
    def __init__(self,still=False,numFaces=3,drawMesh=True):
        self.myFaceMesh=self.mp.solutions.face_mesh.FaceMesh(still,numFaces)
        self.myDraw=self.mp.solutions.drawing_utils
        self.draw=drawMesh
    def Marks(self,frame):
        global dispW
        global dispH
        drawSpecCircle=self.myDraw.DrawingSpec(thickness=0,circle_radius=0,color=(255,0,0))
        drawSpecLine=self.myDraw.DrawingSpec(thickness=3,circle_radius=2,color=(255,0,0))
        frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results=self.myFaceMesh.process(frameRGB)
        facesMeshLms=[]
        if results.multi_face_landmarks != None:
            for faceMesh in results.multi_face_landmarks:
                faceMeshLms=[]
                for lm in faceMesh.landmark:
                    loc=(int(lm.x*dispW),int(lm.y*dispH))
                    faceMeshLms.append(loc)
                facesMeshLms.append(faceMeshLms)
                if self.draw==True:
                    self.myDraw.draw_landmarks(frame,faceMesh,self.mp.solutions.face_mesh.FACE_CONNECTIONS,drawSpecCircle,drawSpecLine)
        return facesMeshLms
 
class mpFace:
    import mediapipe as mp 
    def __init__(self):
        self.myFace=self.mp.solutions.face_detection.FaceDetection()
    def Marks(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.myFace.process(frameRGB)
        faceBoundBoxs=[]
        if results.detections != None:
            for face in results.detections:
                bBox=face.location_data.relative_bounding_box
                topLeft=(int(bBox.xmin*dispW),int(bBox.ymin*dispH))
                bottomRight=(int((bBox.xmin+bBox.width)*dispW),int((bBox.ymin+bBox.height)*dispH))
                faceBoundBoxs.append((topLeft,bottomRight))
        return faceBoundBoxs
 
class mpPose:
    import mediapipe as mp
    def __init__(self,still=False,upperBody=False, smoothData=True):
        self.myPose=self.mp.solutions.pose.Pose(still,upperBody,smoothData)
    def Marks(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.myPose.process(frameRGB)
        poseLandmarks=[]
        if results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:            
                poseLandmarks.append((int(lm.x*dispW),int(lm.y*dispH)))
        return poseLandmarks
 
class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands)
    def Marks(self,frame):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            #print(results.multi_handedness)
            for hand in results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*dispW),int(landMark.y*dispH)))
                myHands.append(myHand)
        return myHands,handsType
 

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
tColor=(0,0,255)
tSize=.1
tThick=1
#pose=mp.solutions.pose.Pose(False, False, True,True,True)
#mpDraw=mp.solutions.drawing_utils

findHands=mpHands(2)
findFace=mpFace()
findPose=mpPose()
findMesh=mpFaceMesh(drawMesh=True)
keypoints=[0,7,8,11,13,15,19,12,14,16,20,23,25,27,31,24,26,28,32]
circleRadius=5
circleColor=(0,0,255)
circleThickness=-1 
while True:
    tStart=time.time()
    frame=picam2.capture_array()
    frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.putText(frame, str(int(fps))+' FPS', pos, font, height, fpsColor, weight)
    handsLM,handsType=findHands.Marks(frame)
    faceLoc=findFace.Marks(frame)
    poseLM=findPose.Marks(frame)
    facesMeshLM=findMesh.Marks(frame)
    if poseLM != []:
        for ind in keypoints:
            cv2.circle(frame,poseLM[ind],circleRadius, circleColor, circleThickness)
        for face in faceLoc:
            cv2.rectangle(frame,face[0],face[1],(255,0,0),3)
        for hand,handType in zip (handsLM, handsType):
            if handType=='Right':
                lbl='Right'
            if handType=='Left':
                lbl='Left'
            cv2.putText(frame(lbl,hand[8],font,2,tColor,2))
        #for faceMeshLM in facesMeshLM:
        #    cnt=0
        #    for lm in faceMeshLM:
        #        cv2.putText(frame,str(cnt),lm,font,tSize,tColor,tThick)
        #        cnt=cnt+1

    cv2.imshow("picam", frame)

    if cv2.waitKey(1)==ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)