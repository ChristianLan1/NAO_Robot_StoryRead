import time
import almath
import argparse
from naoqi import ALProxy

motionProxy = ALProxy("ALMotion", "172.20.10.14",9559)
postureProxy = ALProxy("ALRobotPosture", "172.20.10.14", 9559)

postureProxy.goToPosture("Crouch",1.0)



motionProxy.wakeUp()

motionProxy.openHand('LHand')
motionProxy.closeHand('LHand')


memory = ALProxy("ALMemory","172.20.10.14",9559)
memory.subscribeToEvent("TouchChanged", "ReactToTouch", "172.20.10.14")
#time.sleep(3.0)
touchOrNot = memory.getData("TouchChanged")






#Set the LHand 
motionProxy.setStiffnesses("LWristYaw", 1.0)
motionProxy.setStiffnesses("LShoulderRoll", 1.0)
motionProxy.setStiffnesses("LElbowYaw", 1.0)
motionProxy.setStiffnesses("LElbowRoll", 1.0)





#Middle
names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch"]
angleLists = [-10.5*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 5.0*almath.TO_RAD,80.0*almath.TO_RAD]
times      = [1.0, 1.0,1.0,1.0,1.0]
isAbsolute = True
motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)


#Right top
names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch"]
angleLists = [-1.0*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 25.0*almath.TO_RAD,65.0*almath.TO_RAD]
times      = [1.0, 1.0,1.0,1.0,1.0]
isAbsolute = True
motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)


#Left bottom
names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch"]
angleLists = [-30*almath.TO_RAD,-70.5*almath.TO_RAD, 104.5*almath.TO_RAD, 35.0*almath.TO_RAD,90.0*almath.TO_RAD]
times      = [1.0, 1.0,1.0,1.0,1.0]
isAbsolute = True
motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

#Left top
names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch"]
angleLists = [-88.5*almath.TO_RAD,-15*almath.TO_RAD, 90*almath.TO_RAD, 76.0*almath.TO_RAD,80*almath.TO_RAD]
times      = [1.0, 1.0,1.0,1.0,1.0]
isAbsolute = True
motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

#Right bottom




print touchOrNot
#if (['Head/Touch/Middle', False] or ['Head/Touch/Middle', True]) in touchOrNot:

motionProxy.closeHand('LHand')





#RHand calibration
#motionProxy.setStiffnesses("RWristYaw", 1.0)
#motionProxy.setStiffnesses("RShoulderRoll", 1.0)
#motionProxy.setStiffnesses("RElbowYaw", 1.0)
#motionProxy.setStiffnesses("RElbowRoll", 1.0)


#names      = ["RElbowRoll","RElbowYaw","RWristYaw", "RShoulderRoll","RShoulderPitch"]
#angleLists = [10.0*almath.TO_RAD,-50.0*almath.TO_RAD,15.0*almath.TO_RAD, 18.0*almath.TO_RAD,30.0*almath.TO_RAD]
#times      = [1.0, 1.0,1.0, 1.0,1.0]
#isAbsolute = True
#motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

#time.sleep(5.0)
#motionProxy.rest()

