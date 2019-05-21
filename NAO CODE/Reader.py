from naoqi import ALProxy
from pdfReader import convert, layout
import arm
import re
import time
import io
# -*- coding: utf-8 -*-
import sys, os
import PDF_Client

class Reader:
    def __init__(self, authorFileName, tts, tracker,connectionToPdf,IP,book):
        self.authorFileName = authorFileName
        #self.contentFileName = contentFileName
        self.tts = tts
        self.tracker = tracker
        
        self.countPage = 0
        self.turnPage = 0
        self.connectionToPdf = connectionToPdf
        self.IP = IP
        self.book = book
        self.bookTitle = book[0]
        self.pages = book[1]
        self.dictTxt = layout(True, self.bookTitle,self.pages)
        self.dictImg = layout(False, self.bookTitle,self.pages)

    def readAuthor(self):
        #convert(self.bookTitle,[0],True)#getting author info
        with open(self.authorFileName) as f:
            lines = f.readlines()
            print lines
            line = lines[0]
            line = line.lower()
            line = re.split("author:",line)
        self.tts.say("Today we are going to read a story book. \\pau=1000\\ Named "+line[0])
        self.tts.say("The author is: "+line[1])
        self.tts.say(" Remember if we read from this author before? ")
    
    def readContent(self,memoryProxy,asr,armMotion,dialog,topic):

        gaze = ALProxy("ALGazeAnalysis",self.IP,9559)
        atts = ALProxy("ALAnimatedSpeech",self.IP,9559)
        aup = ALProxy("ALAudioPlayer", self.IP, 9559)

        globalSentence = """"""
        count = 0
        globalFace = 9999
        
        #convert(self.bookTitle,self.pages,False)
        #fileName = 'C:\Users\Christian Lan\OneDrive\NAO CODE\output.txt'
        #fileName = 'c:/Users/Zoe Chai/Desktop/output.txt'
        #dictTxt = layout(True, self.bookTitle,self.pages)
        #dictImg = layout(False, self.bookTitle,self.pages)

        with open(self.authorFileName) as f:
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
            memoryProxy.subscribeToEvent("PeoplePerception/VisiblePeopleList","ALGazeAnalysis",self.IP)
            for sytax in sentence:
                
                toleranceRange = gaze.getTolerance()
                print"range",toleranceRange
                #memoryProxy.subscribeToEvent("GazeAnalysis/PersonStopsLookingAtRobot","ALGazeAnalysis",self.self.IP)
                #print"look back"
                
            
                time.sleep(2)
                
                PeopleId = memoryProxy.getData("PeoplePerception/VisiblePeopleList")
                print"FaceGlobalId", globalFace
                print"FaceId", PeopleId
                #faceData = faceProxy.getLearnedFacesList()
                
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
                #memoryProxy.subscribeToEvent("GazeAnalysis/PersonStopsLookingAtRobot","ALGazeAnalysis",self.IP)
                time.sleep(2)
                #print faceData
                if len(PeopleId) != 0 and not jump:
                    try:
                        visualData = memoryProxy.getData("PeoplePerception/Person/"+str(PeopleId[0])+"/IsLookingAtRobot")
                        print( "visualData: %s" % visualData )
                        LedProxy = ALProxy("ALLeds", self.IP, 9559)
                        LedProxy.randomEyes(2)
                        if visualData != 1:
                            #add dialog here
                            dialog.subscribe('myModule')
                            dialog.activateTopic(topic)
                            #dialog.forceOutput()
                            dialog.gotoTopic("ExampleDialog")
                            #aup.playFile("/home/nao/home/nao/random.wav")
                            """memoryProxy.removeData("Dialog/Answered")
                            memoryProxy.subscribeToEvent("Dialog/Answered","Dialog",IP)

                            dialogOutput = memoryProxy.getData("Dialog/Answered")
                            while(dialogOutput == None):
                                time.sleep(1)
                                dialogOutput = memoryProxy.getData("Dialog/Answered")"""
                            dialog.deactivateTopic(topic)
                            # Unload topic
                            #dialog.unloadTopic(topic)
                            # Stop dialog
                            dialog.unsubscribe('myModule')
                            self.tts.say("Let's continue")
                            #memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")
                            """self.tts.say("Hey my little friend!")
                            self.tts.say("Can you tell me what just happened in the story?")
                            listen = SoundFeedback(asr,memoryProxy)
                            sound = listen.getVoiceRec()
                            if sound == "No":
                                self.tts.say("Aw")
                                self.tts.say("I would feel sad if you are not reading it with me")
                                self.tts.say("Please come back")
                            else:
                                self.tts.say("That's right!")
                                self.tts.say("Let's continue!")"""

                    except RuntimeError:
                        print"skip the error"
                        pass
                page = re.search("([0-9]+)\/[0-9]+",sytax)
                
                #count the pagenum and call the def locationToPoint to return a location
                
                if self.countPage == 0 and self.turnPage == 0:
                    pagenum = self.pages[0]
                    if self.dictTxt[pagenum] == "rightbottom":
                        location = self.dictImg[pagenum]
                    else:
                        location = self.dictTxt[pagenum]
                    self.turnPage = 1
                    #self.tracker.setTimeOut(2000)
                    self.tts.say("Let's look at this picture")
                    time.sleep(2)
                    armMotion.point(location)
                    #self.tracker.lookAt(targetPosition,0,0.5,False)
                    
                    
                
                if page:    
                    self.connectionToPdf.turnPage()
                    #Send a msg to pdf displayer to turn page
                    self.countPage = self.countPage + 1
                    pagenum = self.pages[self.countPage]
                    if self.dictTxt[pagenum] == "rightbottom":
                        location = self.dictImg[pagenum]
                    else:
                        location = self.dictTxt[pagenum]
                    #location = self.locationToPoint(pagenum)
                    #self.tracker.setTimeOut(2000)
                    armMotion.point(location)
                    self.tts.say("Let's look at this sentence")
                    time.sleep(2)
                self.tracker.lookAt(targetPosition,0,0.5,False)
                
                time.sleep(0.5)

                output = re.sub("([0-9]+)\/[0-9]+","",sytax)
                count += 1
                #if count 
                print "sytax", output
                #tts.setParameter("speed", 50)
                atts.say(output.lower(),{"bodyLanguageMode":"random"})
        gaze.unsubscribe("ALGazeAnalysis")
        memoryProxy.subscribeToEvent("PeoplePerception/VisiblePeopleList","ALGazeAnalysis",self.IP)
    
    
