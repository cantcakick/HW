import cv2
import time
import numpy as np
import mediapipe as mp
import pickle
from picamera2 import Picamera2, Preview
picam2=Picamera2(1)

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

pose=mp.solutions.pose.Pose(False, False, True,True,True)
mpDraw=mp.solutions.drawing_utils
class mpPose:
    import mediapipe as mp
    def __init__(self):
        self.pose=self.mp.solutions.pose.Pose()
    def Marks(self,frame):
        myPoses=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.pose.process(frameRGB)
        #landmarks=results.pose_landmarks.landmark
        if results.pose_landmarks != None:
            for landmark in results.pose_landmarks.landmark:
                myPose=[]
                myPose.append((int(landmark.x*dispW),int(landmark.y*dispH)))
            myPoses.append(myPose)
        return myPoses
    def findDist(poseData):
        distMatrix=np.zeros(len[poseData],len[poseData],dtype='float')
        #handDist=
        #footDist=
        #kneeDist=
        #elbowDist=
        for row in range(0,len(poseData)):
            for column in range(0,len(poseData)):
                distMatrix[row][column]=(((poseData[row][0]-poseData[column][0])**2+(poseData[row][1]-poseData[column][1])**2)**(1./2.))
        return distMatrix
    def findError(gesturematrix,newMatrix,landmarks):
        error=0
        for row in landmarks:
            for column in landmarks:
                error=error+abs(gesturematrix[row][column]-newMatrix[row][column])
        return error
    def findPose(newPose,knownPose,landmarks,poseNames,tol):
        errorArray=[]
        for i in range(0,len(poseNames),1):
            error=mpPose.findError(knownPose[i],newPose,landmarks)
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
    
findPoses=mpPose()
train=int(input('Enter 1 to Train, Enter 0 to Play'))
if train==1:
    trainCnt=0
    knownPose=[]
    numPoses=int(input('How many poses do you want to train?'))
    poseNames=[]
    for i in range(0,numPoses,1):
        prompt='Name of pose #' +str(i+1)+' '
        name=input(prompt)
        poseNames.append(name)
    print(poseNames)
    trainName=input('Filename for data? (Enter for default) ')
    if trainName=='':
        trainName='default'
    trainName=trainName+'.pkl'
if train==0:
    trainName=input('Select training file. (Press enter for default) ')
    if trainName=='':
        trainName='default'
    trainName=trainName+'.pkl'
    with open(trainName,'rb')as f:
        poseNames=pickle.load(f)
        knownPoses=pickle.load(f)
#lm=mpPose.Marks.results
#landmarks=lm.pose_landmarks.landmark   
landmarks=[0,12,14,16,11,13,15,24,26,28,23,25,27]
while True:
    tStart=time.time()
    frame=picam2.capture_array()
    frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.putText(frame, str(int(fps))+' FPS', pos, font, height, fpsColor, weight)
    poseData=findPoses.Marks(frame)
    if train==1:
        if poseData!=[]:
            print('Show Pose ',poseNames[trainCnt],': Press t when ready')
            if cv2.waitKey(1)&0xff==ord('t'):
                knownPose=mpPose.findDist(poseData[0])
                knownPoses.append(knownPose)
                trainCnt=trainCnt+1
                if trainCnt==numPoses:
                    train=0
                    with open(trainName,'wb') as f:
                        pickle.dump(poseNames,f)
                        pickle.dump(knownPoses,f)
    if train==0:
        if poseData !=[]:
            newPose=mpPose.findDist(poseData[0])
            myPose=mpPose.findPose(newPose,knownPose,landmarks,poseNames,tol)
            cv2.putText(frame,myPose,(100,200),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),8)
    
#insert code

    cv2.imshow("picam", frame)

    if cv2.waitKey(1)==ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)