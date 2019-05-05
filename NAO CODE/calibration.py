import arm
class Calibrations:
    def __init__(self,motion,postureProxy,tts,IP,PORT,armMotion):
        self.motion = motion
        self.postureProxy = postureProxy
        self.tts = tts
        self.IP =IP
        self.Port = PORT
        self.armMotion = armMotion
        
    
    def setupCalibration(self,memoryProxy):
        #initializePosture
        #self.motion.rest
        self.postureProxy.goToPosture("Crouch",0.5)

        #InitializeMotion
        #self.motion.wakeUp()
        self.motion.stiffnessInterpolation("Head", 1.0, 1.0)
        #Initialize armMotion instance
        #armMotion = arm.ArmMotion(self.motion,memoryProxy,self.postureProxy)
        self.tts.say("please put a pen for me")
        self.armMotion.holdPen()
        
        
        
        #Calibrate the hand
        self.tts.say("Calibration")
        self.tts.say("Please place the center of the tablet to where I'm pointing at")
        self.tts.say("Please touch my head when calibration finished")
        self.armMotion.point("calibration")
        
        self.tts.say("Calibration finished.")
        
        
