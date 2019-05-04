import time
import almath
import argparse
from naoqi import ALProxy

class ArmMotion:
    def __init__(self,motionProxy,memoryProxy,postureProxy):
        self.motionProxy = motionProxy
        self.memory = memoryProxy
        self.postureProxy = postureProxy

    
        #Set the LHand 
        self.motionProxy.setStiffnesses("LWristYaw", 1.0)
        self.motionProxy.setStiffnesses("LShoulderRoll", 1.0)
        self.motionProxy.setStiffnesses("LElbowYaw", 1.0)
        self.motionProxy.setStiffnesses("LElbowRoll", 1.0)


        #hold pen
        self.names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
        self.angleLists = [-60.0*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 5.0*almath.TO_RAD,100.0*almath.TO_RAD,
                    30.0*almath.TO_RAD, -10.0*almath.TO_RAD]
        self.times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
        self.isAbsolute = True
        
    def holdPen(self):
        self.motionProxy.angleInterpolation(self.names, self.angleLists, self.times, self.isAbsolute)
        self.motionProxy.openHand('LHand')
        #say "put a pen in my hand"
        time.sleep(2.0)
        self.motionProxy.closeHand('LHand')

        self.postureProxy.goToPosture("Crouch",1.0)


    def point(self,location):
        if location == "calibration":
            #Need to extrat a single ifelse for calibration
            #self.postureProxy.goToPosture("Crouch",1.0)
            #Middle-calibration
            names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
            angleLists = [-10.5*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 5.0*almath.TO_RAD,80.0*almath.TO_RAD,
                        60*almath.TO_RAD, 20*almath.TO_RAD]
            times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
            isAbsolute = True
            self.motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)

            #tell the teacher to keep adjusting the tablet until the pen points to the middle of the screen, then press the head buttom
            #self.memory.unsubscribeToEvent("TouchChanged","ReactToTouch")
            
            #print touchOrNot
            while(True):
                self.memory.subscribeToEvent("MiddleTactilTouched", "ReactToTouch", "172.20.10.14")
                time.sleep(3)
                touchOrNot = self.memory.getData("MiddleTactilTouched")
            
                print(touchOrNot)
                #if (['Head/Touch/Middle', False] or ['Head/Touch/Middle', True]) in touchOrNot:
                if touchOrNot == 1.0:
                    #colibration completed
                    self.memory.unsubscribeToEvent("MiddleTactilTouched","ReactToTouch")
                    self.postureProxy.goToPosture("Crouch",1.0)
                    break
                else:
                    time.sleep(1)
            
        elif location == "righttop":
            #self.postureProxy.goToPosture("Crouch",1.0)
            #Right top
            names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
            angleLists = [-1.0*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 25.0*almath.TO_RAD,65.0*almath.TO_RAD,
                        60*almath.TO_RAD, 15*almath.TO_RAD]
            times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
            isAbsolute = True
            self.motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)
            time.sleep(1.5)
            #self.postureProxy.goToPosture("Crouch",1.0)

        

        elif location == "leftbottom":
            #self.postureProxy.goToPosture("Crouch",1.0)
            #Left bottom
            names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
            angleLists = [-30*almath.TO_RAD,-70.5*almath.TO_RAD, 104.5*almath.TO_RAD, 35.0*almath.TO_RAD,90.0*almath.TO_RAD,
                        40*almath.TO_RAD, 29*almath.TO_RAD]
            times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
            isAbsolute = True
            self.motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)
            time.sleep(1.5)
            #self.postureProxy.goToPosture("Crouch",1.0)
        elif location == "middle":
            #self.postureProxy.goToPosture("Crouch",1.0)
            #Middle-calibration
            names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
            angleLists = [-10.5*almath.TO_RAD,-109.5*almath.TO_RAD, -104.5*almath.TO_RAD, 5.0*almath.TO_RAD,80.0*almath.TO_RAD,
                        60*almath.TO_RAD, 20*almath.TO_RAD]
            times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
            isAbsolute = True
            self.motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)
            time.sleep(1.5)
            #self.postureProxy.goToPosture("Crouch",1.0)

            
        else:
            #self.postureProxy.goToPosture("Crouch",1.0)
            #Left top
            names      = ["LElbowRoll","LElbowYaw","LWristYaw", "LShoulderRoll","LShoulderPitch","HeadYaw","HeadPitch"]
            angleLists = [-88.5*almath.TO_RAD,-15*almath.TO_RAD, 90*almath.TO_RAD, 76.0*almath.TO_RAD,80*almath.TO_RAD,
                        40*almath.TO_RAD, 15*almath.TO_RAD]
            times      = [1.0, 1.0,1.0,1.0,1.0,1.0,1.0]
            isAbsolute = True
            self.motionProxy.post.angleInterpolation(names, angleLists, times, isAbsolute)
            time.sleep(1.5)
            #self.postureProxy.goToPosture("Crouch",1.0)

       


