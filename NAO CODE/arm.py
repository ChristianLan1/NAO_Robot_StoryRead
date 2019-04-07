import time
import almath
import argparse
from naoqi import ALProxy

motionProxy = ALProxy("ALMotion", "172.20.10.14",9559)
postureProxy = ALProxy("ALRobotPosture", "172.20.10.14", 9559)

postureProxy.goToPosture("Crouch",1.0)



motionProxy.wakeUp()





memory = ALProxy("ALMemory","172.20.10.14",9559)
memory.subscribeToEvent("TouchChanged", "ReactToTouch", "172.20.10.14")

touchOrNot = memory.getData("TouchChanged")






#Set the LHand 
motionProxy.setStiffnesses("LWristYaw", 1.0)
motionProxy.setStiffnesses("LShoulderRoll", 1.0)
motionProxy.setStiffnesses("LElbowYaw", 1.0)
motionProxy.setStiffnesses("LElbowRoll", 1.0)


#hold pen
names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
angleLists = [-60.0*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 5.0*almath.TO_RAD,100.0*almath.TO_RAD,
              30.0*almath.TO_RAD, -10.0*almath.TO_RAD]
times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
isAbsolute = True
motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)
motionProxy.openHand('LHand')
#say "put a pen in my hand"
time.sleep(2.0)
motionProxy.closeHand('LHand')

postureProxy.goToPosture("Crouch",1.0)

def point(location):
    if location == "middle":
        postureProxy.goToPosture("Crouch",1.0)
        #Middle-calibration
        names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
        angleLists = [-10.5*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 5.0*almath.TO_RAD,80.0*almath.TO_RAD,
                    60*almath.TO_RAD, 20*almath.TO_RAD]
        times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
        isAbsolute = True
        motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)

        #tell the teacher to keep adjusting the tablet until the pen points to the middle of the screen, then press the head buttom
        #print touchOrNot
        #if (['Head/Touch/Middle', False] or ['Head/Touch/Middle', True]) in touchOrNot:
            #colibration completed
        
    elif location == "righttop":
        postureProxy.goToPosture("Crouch",1.0)
        #Right top
        names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
        angleLists = [-1.0*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 25.0*almath.TO_RAD,65.0*almath.TO_RAD,
                    60*almath.TO_RAD, 15*almath.TO_RAD]
        times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
        isAbsolute = True
        motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)

       

    elif location == "leftbottom":
        postureProxy.goToPosture("Crouch",1.0)
        #Left bottom
        names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
        angleLists = [-30*almath.TO_RAD,-70.5*almath.TO_RAD, 104.5*almath.TO_RAD, 35.0*almath.TO_RAD,90.0*almath.TO_RAD,
                    40*almath.TO_RAD, 29*almath.TO_RAD]
        times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
        isAbsolute = True
        motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)

        
    else:
        postureProxy.goToPosture("Crouch",1.0)
        #Left top
        names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
        angleLists = [-88.5*almath.TO_RAD,-15*almath.TO_RAD, 90*almath.TO_RAD, 76.0*almath.TO_RAD,80*almath.TO_RAD,
                    40*almath.TO_RAD, 15*almath.TO_RAD]
        times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
        isAbsolute = True
        motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)

       


