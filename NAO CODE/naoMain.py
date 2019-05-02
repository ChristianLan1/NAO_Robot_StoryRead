from naoqi import ALProxy
from pdfReader import convert, layout
import arm
import re
import time
import io
# -*- coding: utf-8 -*-
import sys, os
import PDF_Client

IP = "172.20.10.14"
Port = 9559
convertedFile = 'C:\Users\Christian Lan\OneDrive\NAO CODE\output.txt'
    


class Reader:
    def __init__(self, filename, tts, tracker,connectionToPdf):
        self.filename = filename
        self.tts = tts
        self.tracker = tracker
        self.pages = [1,2,3,4,5,6,7,8,9,10,11]
        self.countPage = 0
        self.turnPage = 0
        self.connectionToPdf = connectionToPdf
    def readAuthor(self):
        convert("60744-whoop-goes-the-pufferfish.pdf",[0])#getting author info
        with open(self.filename) as f:
            lines = f.readlines()
            print lines
            line = lines[0]
            line = line.lower()
            line = re.split("author:",line)
        self.tts.say("Today we are going to read a story book. \\pau=1000\\ Named "+line[0])
        self.tts.say("The author is: "+line[1])
        self.tts.say(" Remember if we read from this author before? ")
    
    def readContent(self,gaze,memoryProxy,atts,asr,armMotion,faceProxy):
        globalSentence = """"""
        count = 0
        globalFace = 9999
        
        convert("60744-whoop-goes-the-pufferfish.pdf",self.pages)
        fileName = 'C:\Users\Christian Lan\OneDrive\NAO CODE\output.txt'
        #fileName = 'c:/Users/Zoe Chai/Desktop/output.txt'
        dictTxt = layout(True, "60744-whoop-goes-the-pufferfish.pdf",self.pages)
        dictImg = layout(False, "60744-whoop-goes-the-pufferfish.pdf",self.pages)

        with open(fileName ) as f:
            lines = f.readlines()
            for line in lines:
                #re.sub("^ [0-9]\/[0-9][0-9]"," ",line)
                #sentence = re.split("\.",line)
                line = line.strip()
                line = line.ljust(len(line)+1)
                #line = line.join("\\pau=100\\")
                #print "line", line
                globalSentence = globalSentence+line
            #print "global sentence", globalSentence
            sentence = re.split("\.",globalSentence)
            #print "sentence", sentence
            gaze.subscribe("ALGazeAnalysis")
            memoryProxy.subscribeToEvent("PeoplePerception/VisiblePeopleList","ALGazeAnalysis",IP)
            for sytax in sentence:
                
                toleranceRange = gaze.getTolerance()
                print"range",toleranceRange
                #memoryProxy.subscribeToEvent("GazeAnalysis/PersonStopsLookingAtRobot","ALGazeAnalysis",IP)
                #print"look back"
                
            
                time.sleep(2)
                
                PeopleId = memoryProxy.getData("PeoplePerception/VisiblePeopleList")
                print"FaceGlobalId", globalFace
                print"FaceId", PeopleId
                faceData = faceProxy.getLearnedFacesList()
                
                targetPosition = self.tracker.getTargetPosition(0)
                print targetPosition
                if globalFace != PeopleId:
                    globalFace = PeopleId
                    
                    jump = True
                else:
                    jump = False
                #if self.tracker.isNewTargetDetected():

                #print( "visualData: %s" % visualData )
                #time.sleep(2)
                #memoryProxy.unsubscribeToEvent("PeoplePerception/PeopleList","ALGazeAnalysis")
                #memoryProxy.subscribeToEvent("GazeAnalysis/PersonStopsLookingAtRobot","ALGazeAnalysis",IP)
                time.sleep(2)
                print faceData
                if len(PeopleId) != 0 and not jump or faceData == "Child":
                    try:
                        visualData = memoryProxy.getData("PeoplePerception/Person/"+str(PeopleId[0])+"/IsLookingAtRobot")
                        print( "visualData: %s" % visualData )
                        LedProxy = ALProxy("ALLeds", IP, 9559)
                        LedProxy.randomEyes(2)
                        if visualData != 1:
                            tts.say("Hey my little friend!")
                            tts.say("Can you tell me what just happened in the story?")
                            listen = SoundFeedback(asr,memoryProxy)
                            sound = listen.getVoiceRec()
                            if sound == "No":
                                tts.say("Aw")
                                tts.say("I would feel sad if you are not reading it with me")
                                tts.say("Please come back")
                            else:
                                tts.say("That's right!")
                                tts.say("Let's continue!")

                    except RuntimeError:
                        print"skip the error"
                        pass
                page = re.search("([0-9]+)\/[0-9]+",sytax)
                
                #count the pagenum and call the def locationToPoint to return a location
                
                if self.countPage == 0 and self.turnPage == 0:
                    pagenum = self.pages[0]
                    if dictTxt[pagenum] == "rightbottom":
                        location = dictImg[pagenum]
                    else:
                        location = dictTxt[pagenum]
                    self.turnPage = 1
                    #self.tracker.setTimeOut(2000)
                    tts.say("Let's look at this picture")
                    armMotion.point(location)
                    #self.tracker.lookAt(targetPosition,0,0.5,False)
                    
                    
                
                if page:
                    self.connectionToPdf.turnPage()
                    #Send a msg to pdf displayer to turn page
                    self.countPage = self.countPage + 1
                    pagenum = self.pages[self.countPage]
                    if dictTxt[pagenum] == "rightbottom":
                        location = dictImg[pagenum]
                    else:
                        location = dictTxt[pagenum]
                    #location = self.locationToPoint(pagenum)
                    #self.tracker.setTimeOut(2000)
                    armMotion.point(location)
                    tts.say("Let's look ar this sentence")
                self.tracker.lookAt(targetPosition,0,0.5,False)
                
                time.sleep(1)

                output = re.sub("([0-9]+)\/[0-9]+","",sytax)
                count += 1
                #if count 
                print "sytax", output
                #tts.setParameter("speed", 50)
                atts.say(output.lower(),{"bodyLanguageMode":"random"})
    
    

class SoundFeedback:
    def __init__(self,asr,memoryProxy):
        self.asr = asr
        self.memoryProxy = memoryProxy
    def getVoiceRec(self):
        self.asr.setVisualExpression(True)
        self.asr.pause(True)
        self.asr.setLanguage("English")

        vocabulary = ["yes", "no"]

        self.asr.setVocabulary(vocabulary, False)
        self.asr.subscribe(IP)
        print "speech recognition engine started"

        #memoryProxy = ALProxy("ALMemory", IP, 9559)
        self.memoryProxy.subscribeToEvent('WordRecognized',IP,IP)
        #asr.removeAllContext()
        self.asr.pause(False)
        time.sleep(5)

        self.asr.unsubscribe(IP)

        data=memoryProxy.getData("WordRecognized")
        print( "data: %s" % data )
        
        memoryProxy.unsubscribeToEvent('WordRecognized',IP)
        return data

   


if __name__ == "__main__":
    

    gaze = ALProxy("ALGazeAnalysis",IP,Port)
    tts = ALProxy("ALTextToSpeech", IP,Port)
    atts = ALProxy("ALAnimatedSpeech",IP,Port)
    asr = ALProxy("ALSpeechRecognition", IP, 9559)
    memoryProxy = ALProxy("ALMemory", IP, 9559)
    motion = ALProxy("ALMotion", IP ,Port)
    postureProxy = ALProxy("ALRobotPosture", IP, 9559)
    voice = SoundFeedback(asr,memoryProxy)

    connectionToPdf = client()
    is_Connected = connectionToPdf.connection()
    while(not is_Connected):
        tts.say("The PDF Application is not opened.")
        tts.say("Please open the PDF displayer so that I can show the book to you.")
        time.sleep(1)
        tts.say("When the PDF displayer opened, please talk to me")
        data = voice.getVoiceRec()
        if data[0] == "connected":

    
    #initializePosture
    motion.rest
    postureProxy.goToPosture("Crouch",1.0)

    #InitializeMotion
    motion.wakeUp()
    motion.stiffnessInterpolation("Head", 1.0, 1.0)

    tts.say("please put a pen for me")
    #Initialize armMotion instance
    armMotion = arm.ArmMotion(motion,memoryProxy,postureProxy)
    #Calibrate the hand
    tts.say("Calibration")
    tts.say("Please place the center of the tablet to where I'm pointing at")
    tts.say("Please touch my head when calibration finished")
    armMotion.point("calibration")
    
    tts.say("Calibration finished.")
    #Initializing Tracker
    tracker = ALProxy("ALTracker", IP, Port)
    targetName = "Face"
    faceWidth = 0.1
    tracker.registerTarget(targetName, faceWidth)
    # Then, start tracker.
    tracker.track(targetName)
    print "ALTracker successfully started, now show your face to robot!"
    faceProxy = ALProxy("ALFaceDetection", IP, Port)
    faceProxy.clearDatabase()
    faceProxy.setTrackingEnabled(True)
    faceProxy.subscribe("Child", 600, 0.0 )
    #tracker.toggleSearch(True)
    
    try:
        while(tracker.isTargetLost()):
            
            
           
            
            tts.say("If you are ready to read with me, please look at me for 10 seconds")
            faceProxy.learnFace("Child")
            time.sleep(8)
            print"looking for target"
    except KeyboardInterrupt:
        printc
        print"Interrupted by user"
    #faceData = memoryProxy.getData("FaceDetected")
    #tracker.toggleSearch(False)
    faceData = faceProxy.getLearnedFacesList()
    if len(faceData) == 0:
        faceProxy.learnFace("Child")
        time.sleep(8)
    print faceData


    tts.say("Alright, we are ready to go!")
    time.sleep(1)
    
    r = Reader(convertedFile,tts,tracker,connectionToPdf)
    r.readAuthor()

    
    #The robot will stand up at this sytax. No idea why
    data = voice.getVoiceRec()
    if data[0] == "yes":
        tts.say("Do you remember what we liked about that story? Here's another book by this author.")
        tts.say("Let's read this one and see if we like it as well as the other book we read")
    else:
        tts.say("OK! Let's read it")

    r.readContent(gaze,memoryProxy,atts,asr,armMotion,faceProxy)


    gaze.unsubscribe("ALGazeAnalysis")
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.rest()