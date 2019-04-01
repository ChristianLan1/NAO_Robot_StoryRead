from naoqi import ALProxy
from pdfReader import convert
import re
import time
# -*- coding: utf-8 -*-
import sys, os

IP = "172.20.10.14"
Port = 9559



class Reader:
    def __init__(self, filename, tts):
        self.filename = filename
        self.tts = tts

    def readAuthor(self):
        convert("60744-whoop-goes-the-pufferfish.pdf",pages = [0])#getting author info
        with open(self.filename) as f:
            lines = f.readlines()
            print lines
            line = lines[0]
            line = line.lower()
            line = re.split("author:",line)
        self.tts.say("Today we are going to read a story book. Named "+line[0])
        self.tts.say("The author is: "+line[1])
        self.tts.say(" Remember if we read from this author before? ")
    
    def readContent(self,gaze,memoryProxy,atts):
        globalSentence = """"""
        count = 0
        globalFace = 9999
        convert("60744-whoop-goes-the-pufferfish.pdf",pages=[1,2,3,4,5,6,7,8,9,10,11])
        with open('C:/Users/xinjie/OneDrive/NAO CODE/output.txt') as f:
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
            for sytax in sentence:
                
                toleranceRange = gaze.getTolerance()
                print"range",toleranceRange
                #memoryProxy.subscribeToEvent("GazeAnalysis/PersonStopsLookingAtRobot","ALGazeAnalysis","172.20.10.14")
                #print"look back"
                memoryProxy.subscribeToEvent("PeoplePerception/PeopleList","ALGazeAnalysis","172.20.10.14")
            
                time.sleep(2)
                
                PeopleId = memoryProxy.getData("PeoplePerception/PeopleList")
                print"FaceGlobalId", globalFace
                print"FaceId", PeopleId
                if globalFace != PeopleId:
                    globalFace = PeopleId
                    
                    jump = True
                else:
                    jump = False
                #print( "visualData: %s" % visualData )
                #time.sleep(2)
                #memoryProxy.unsubscribeToEvent("PeoplePerception/PeopleList","ALGazeAnalysis")
                #memoryProxy.subscribeToEvent("GazeAnalysis/PersonStopsLookingAtRobot","ALGazeAnalysis","172.20.10.14")
                time.sleep(2)
                if len(PeopleId) != 0 and not jump:
                    try:
                        visualData = memoryProxy.getData("PeoplePerception/Person/"+str(PeopleId[0])+"/IsLookingAtRobot")
                        print( "visualData: %s" % visualData )
                    except RuntimeError:
                        print"skip the error"
                        pass
                
                output = re.sub("([0-9]+)\/[0-9]+","",sytax)
                count += 1
                #if count 
                #print "sytax", output
                #tts.setParameter("speed", 50)
                atts.say(output,{"bodyLanguageMode":"random"})


class SoundFeedback:
    def __init__(self,asr,memoryProxy):
        self.asr = asr
        self.memoryProxy = memoryProxy
    def getVoiceRec(self):
        asr.setVisualExpression(True)
        asr.pause(True)
        asr.setLanguage("English")

        vocabulary = ["yes", "no"]

        asr.setVocabulary(vocabulary, False)
        asr.subscribe(IP)
        print "speech recognition engine started"

        memoryProxy = ALProxy("ALMemory", IP, 9559)
        memoryProxy.subscribeToEvent('WordRecognized',IP,IP)
        #asr.removeAllContext()
        asr.pause(False)
        time.sleep(5)

        asr.unsubscribe(IP)

        data=memoryProxy.getData("WordRecognized")
        print( "data: %s" % data )
        
        memoryProxy.unsubscribeToEvent('WordRecognized',"172.20.10.14")
        return data

   


if __name__ == "__main__":
    gaze = ALProxy("ALGazeAnalysis",IP,Port)
    tts = ALProxy("ALTextToSpeech", IP,Port)
    atts = ALProxy("ALAnimatedSpeech",IP,Port)
    asr = ALProxy("ALSpeechRecognition", "172.20.10.14", 9559)
    memoryProxy = ALProxy("ALMemory", "172.20.10.14", 9559)
    motion = ALProxy("ALMotion", IP ,Port)

    #InitializeMotion
    motion.wakeUp()
    motion.stiffnessInterpolation("Head", 1.0, 1.0)
    
    #Initializing Tracker
    tracker = ALProxy("ALTracker", IP, Port)
    targetName = "Face"
    faceWidth = 0.1
    tracker.registerTarget(targetName, faceWidth)
    # Then, start tracker.
    tracker.track(targetName)
    print "ALTracker successfully started, now show your face to robot!"

    try:
        while(tracker.isTargetLost()):
            time.sleep(1)
            print"looking for target"
    except KeyboardInterrupt:
        print
        print"Interrupted by user"

    



    r = Reader('C:/Users/xinjie/OneDrive/NAO CODE/output.txt',tts)
    r.readAuthor()

    voice = SoundFeedback(asr,memoryProxy)
    data = voice.getVoiceRec()
    if data[0] == "yes":
        tts.say("Do you remember what we liked about that story? Here's another book by this author.")
        tts.say("Let's read this one and see if we like it as well as the other book we read")
    else:
        tts.say("OK! Let's read it")

    r.readContent(gaze,memoryProxy,atts)


    gaze.unsubscribe("ALGazeAnalysis")
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.rest()

