"""import re
with open('C:/Users/Zoe Chai/Desktop/books/book_pages.txt') as f:
    lines = f.readlines()
    #print lines
    book = []
    count = 0
    pages = []
    for line in lines:
        
        line = line.rstrip()
        if count==1:
            
            line = re.findall("[0-9]+",line)
            print line
            for element in line:
                
                pages.append(int(element))
            line = pages

        book.append(line)
        count += 1
    print book"""
from naoqi import ALProxy
#from pdfReader import convert, layout
import testArm
#import re
#import time
#import io
# -*- coding: utf-8 -*-
#import sys, os
#import PDF_Client
#import Reader
#import Sound
import calibration
IP = "172.20.10.14"
Port = 9559
tts = ALProxy("ALTextToSpeech", IP,Port)
asr = ALProxy("ALSpeechRecognition", IP, Port)
#asr.unsubscribe("WordRecognized")
memoryProxy = ALProxy("ALMemory", IP, Port)
motion = ALProxy("ALMotion", IP ,Port)
postureProxy = ALProxy("ALRobotPosture", IP, Port)
tracker = ALProxy("ALTracker", IP, Port)
faceProxy = ALProxy("ALFaceDetection", IP, Port)
#voice = Sound.SoundFeedback(asr,memoryProxy,IP)

peopleProxy = ALProxy("ALPeoplePerception",IP,Port)

armMotion = testArm.ArmMotion(motion,memoryProxy,postureProxy,tts)
#time.sleep(5)
print "testing jump"
#time.sleep(5)
armMotion.point("leftbottom")

motion.rest()

    
        
  
            
            