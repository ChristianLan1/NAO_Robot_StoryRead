from naoqi import ALProxy
from pdfReader import convert, layout
import arm
import re
import time
import io
# -*- coding: utf-8 -*-
import sys, os
import PDF_Client
import Reader
import Sound
import calibration

IP = "172.20.10.14"
Port = 9559
convertedFile = 'C:\Users\Christian Lan\OneDrive\NAO CODE\output.txt'
dialogFile = '/behaviours/qitopics.top'
    





def pdfConnection(tts,voice):
    connectionToPdf = PDF_Client.client()
    is_Connected = connectionToPdf.connection()
    if not is_Connected:
        tts.say("The PDF Application is not opened.")
        tts.say("Please open the PDF displayer so that I can show the book to you.")
        time.sleep(1)
        tts.say("When the PDF displayer opened, please talk to me")
    while(not is_Connected):
        
        time.sleep(0.5)
        #dialog.subscribe('myModule')

        # Activate dialog
        #dialog.activateTopic(topic)
        data = voice.waitFeedback()
        print data
        
        if data[0]:
            tts.say("Let me check if the connection to PDF Displayer")
            is_Connected = connectionToPdf.connection()
            if not is_Connected:
                tts.say("I still can't find the displayer")
                tts.say("Can you double check the PDF application.")
                tts.say("Thanks a lot!")
    



if __name__ == "__main__":
    

    gaze = ALProxy("ALGazeAnalysis",IP,Port)
    tts = ALProxy("ALTextToSpeech", IP,Port)
    atts = ALProxy("ALAnimatedSpeech",IP,Port)
    asr = ALProxy("ALSpeechRecognition", IP, Port)
    memoryProxy = ALProxy("ALMemory", IP, Port)
    motion = ALProxy("ALMotion", IP ,Port)
    postureProxy = ALProxy("ALRobotPosture", IP, Port)
    tracker = ALProxy("ALTracker", IP, Port)
    faceProxy = ALProxy("ALFaceDetection", IP, Port)
    voice = Sound.SoundFeedback(asr,memoryProxy,IP)
    
    """dialog = ALProxy('ALDialog', IP, Port)
    dialog.setLanguage("English")
    dialogFile = dialogFile.decode('utf-8')
    topic = dialog.loadTopic(dialogFile.encode('utf-8'))

    dialog.subscribe('myModule')
    dialog.activateTopic(topic)"""
    #Setup Connection to PDF
    #pdfConnection(tts,voice)
    
    #Setup Calibration
    calibrationInstance = calibration.Calibrations(motion,postureProxy,tts,IP,Port)
    calibrationInstance.setupCalibration(motion,memoryProxy,tracker)
    #Setup Face Tracker
    trackChild(tracker,faceProxy)
    tts.say("Alright, we are ready to go!")
    
    time.sleep(1)
    #Setup Reader
    r = Reader.Reader(convertedFile,tts,tracker,connectionToPdf)
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


def trackChild(tracker,):
    targetName = "Face"
    faceWidth = 0.1
    tracker.registerTarget(targetName, faceWidth)
    # Then, start tracker.
    tracker.track(targetName)
    print "ALTracker successfully started, now show your face to robot!"
    
    faceProxy.clearDatabase()
    faceProxy.setTrackingEnabled(True)
    faceProxy.subscribe("Child", 600, 0.0 )
    #tracker.toggleSearch(True)
    
    try:
        while(tracker.isTargetLost()):
            self.tts.say("If you are ready to read with me, please look at me for 10 seconds")
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


    