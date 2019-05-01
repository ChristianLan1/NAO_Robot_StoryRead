from naoqi import ALProxy
from pdfReader import convert
import re
import time
# -*- coding: utf-8 -*-
import sys, os
globalFace = 9999

sys.path.append('c:/Users/xinjie/Desktop/NAO CODE/')
sys.path.append('C:/Users/xinjie/OneDrive/NAO CODE/')


motion = ALProxy("ALMotion", "172.20.10.14" ,9559)
motion.wakeUp()
motion.stiffnessInterpolation("Head", 1.0, 1.0)
#convert("60744-whoop-goes-the-pufferfish.pdf",pages=[1,2,3,4,5,6,7,8,9,10,11])
#generate script

tracker = ALProxy("ALTracker", "172.20.10.14", 9559)
targetName = "Face"
faceWidth = 0.1
tracker.registerTarget(targetName, faceWidth)

# Then, start tracker.
tracker.track(targetName)

print "ALTracker successfully started, now show your face to robot!"


while(tracker.isTargetLost()):
    print"monitoring"

gaze = ALProxy("ALGazeAnalysis","172.20.10.14",9559)


tts = ALProxy("ALTextToSpeech", "172.20.10.14",9559)
atts = ALProxy("ALAnimatedSpeech","172.20.10.14",9559)

#connecting to robot /call speech modulue

convert("60744-whoop-goes-the-pufferfish.pdf",pages = [0])#getting author info
with open('C:/Users/xinjie/OneDrive/NAO CODE/output.txt') as f:
    lines = f.readlines()
    print lines
    line = lines[0]
    line = line.lower()
    line = re.split("author:",line)
tts.say("Today we are going to read a story book. Named "+line[0])
tts.say("The author is: "+line[1])

tts.say(" Remember if we read from this author before? ")

asr = ALProxy("ALSpeechRecognition", "172.20.10.14", 9559)
asr.setVisualExpression(True)
asr.pause(True)
asr.setLanguage("English")

vocabulary = ["yes", "no"]

asr.setVocabulary(vocabulary, False)
asr.subscribe("172.20.10.14")
print "speech recognition engine started"

memoryProxy = ALProxy("ALMemory", "172.20.10.14", 9559)
memoryProxy.subscribeToEvent('WordRecognized',"172.20.10.14",'172.20.10.14')
#asr.removeAllContext()
asr.pause(False)
time.sleep(5)




asr.unsubscribe("172.20.10.14")

data=memoryProxy.getData("WordRecognized")
print( "data: %s" % data )
memoryProxy.unsubscribeToEvent('WordRecognized',"172.20.10.14")

if data[0] == "yes":
    tts.say("Do you remember what we liked about that story? Here's another book by this author.")
    tts.say("Let's read this one and see if we like it as well as the other book we read")
   
else:
    tts.say("OK! Let's read it")
   







globalSentence = """"""
count = 0
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
            visualData = memoryProxy.getData("PeoplePerception/Person/"+str(PeopleId[0])+"/IsLookingAtRobot")
            print( "visualData: %s" % visualData )
        
        output = re.sub("([0-9]+)\/[0-9]+","",sytax)
        count += 1
        #if count 
        #print "sytax", output
        #tts.setParameter("speed", 50)
        atts.say(output,{"bodyLanguageMode":"random"})
    gaze.unsubscribe("ALGazeAnalysis")
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.rest()

#motion.moveInit()

#threadMove = motion.post.moveTo(1.0,0.0,0.0)

#motion.wait(threadMove,0)
#atts.say("Hello! Nice to meet you!", {"bodyLanguageMode":"contextual"})

class Reader:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename) as f:
            r = readlines(f)


if __name__ == "__main__":
    r = Reader('c:\testfile.txt')
    r.read()
