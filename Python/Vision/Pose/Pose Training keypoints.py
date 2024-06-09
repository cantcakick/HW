import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2, Preview
import pickle
picam2=Picamera2(0)

class mpPose:
    import mediapipe as mp
    def __init__(self,still=False,upperBody=False, smoothData=True):
        self.myPose=self.mp.solutions.pose.Pose(still,upperBody,smoothData)
    def Marks(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.myPose.process(frameRGB)
        myP=[]
        if results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:            
                myP.append((int(lm.x*dispW),int(lm.y*dispH)))
        return myP
def findDist(poseData):
    distmatrix=np.zeros([len(poseData),len(poseData)],dtype='float')
    torsoSize=((poseData[11][0]-poseData[12][0])**2+(poseData[11][1]-poseData[12][1])**2)**(1/2)
    for row in range(0,len(poseData)):
        for column in range(0,len(poseData)):
            distmatrix[row][column]=(((poseData[row][11]-poseData[column][11])**2+(poseData[row][12]-poseData[column][12])**2)**(1/2))/torsoSize
    return distmatrix

def findError(posematrix,unknownMatrix,keypoints):
    error=0
    for row in keypoints:
        for column in keypoints:
            error=error+abs(posematrix[row][column]-unknownMatrix[row][column])
    print(error)
    return error
def findPose(unknownPose,knownPoses,keypoints,poseNames,tol):
    errorArray=[]
    for i in range(0,len(poseNames),1):
        error=findError(knownPoses[i],unknownPose,keypoints)
        errorArray.append(error)
    errorMin=errorArray[0]
    minIndex=0
    for i in range(0,len(errorArray),1):
        if errorArray[i]<errorMin:
            errorMin=errorArray[i]
            minIndex=i 
    if errorMin<tol:
        gesture=poseNames[minIndex]
    if errorMin>=tol:
        gesture='Unknown'
    return gesture
 
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
tol=10
findP=mpPose()
keypoints=[0,7,8,11,13,15,19,12,14,16,20,23,25,27,31,24,26,28,32]
s1=11
s2=12
circleRadius=5
circleColor=(0,0,255)
circleThickness=-1 
pose=mp.solutions.pose.Pose(False, False, True,True,True)
mpDraw=mp.solutions.drawing_utils

train=int(input('Enter 1 to train, 0 to Recognize '))
if train==1:
    trainCt=0
    knownPoses=[]
    numPoses=int(input('How many poses will you train? '))
    poseNames=[]
    for i in range(0,numPoses,1):
        prompt='Name of pose #'+str(i+1)+' '
        name=input(prompt)
        poseNames.append(name)
    print(poseNames)
    trainFile=input('Which Training file will you use? Press Enter for Default: ')
    if trainFile=='':
        trainFile='default'
    trainFile=trainFile+'.pkl'
if train==0:
    trainFile=input('What Training data do you want to use?  Press Enter for Default: ')
    if trainFile=='':
        trainFile='default'
    trainFile=trainFile ='.pkl'
    with open(trainFile, 'rb') as f:
        poseNames=pickle.load(f)
        knownPoses=pickle.load(f)    

while True:
    tStart=time.time()
    frame=picam2.capture_array()
    frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.putText(frame, str(int(fps))+' FPS', pos, font, height, fpsColor, weight)
    poseData=findP.Marks(frame)
    if train==1:
        if poseData!=[]:
            print('Show pose',poseNames[trainCt],': Press s to Start ')
            if cv2.waitKey(1) & 0xff==ord('s'):
                knownPose=findDist(poseData[0])
                knownPoses.append(knownPose)
                trainCt=trainCt+1
                if trainCt==numPoses:
                    train=0
                    with open(trainFile,'wb') as f:
                        pickle.dump(poseNames, f)
                        pickle.dump(knownPoses, f)
    if train==0:
        if poseData!=[]:
            unknownPose=findDist(poseData[0])
            myPose=findP(unknownPose,knownPose,keypoints,poseNames,tol)
            cv2.putText(frame,myPose,(100,160),cv2.FONT_HERSHEY_DUPLEX,3,(255,0,0),8)
    
    #if poseLM != []:
    #for p in poseData:    
    #    for ind in keypoints:
    #        cv2.circle(frame,p[ind],circleRadius, circleColor, circleThickness)
    for keypoints in poseData:
        cv2.circle(frame,poseData[keypoints],circleRadius, circleColor, circleThickness)
        
    cv2.imshow("picam", frame)

    if cv2.waitKey(1)==ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)
