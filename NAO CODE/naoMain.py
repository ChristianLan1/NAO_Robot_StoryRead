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
dialogFile = "/home/nao/home/nao/qitopics_enu.top"
dialogFile_Begin = "/home/nao/home/nao/begin_enu.top"
    
#dialogFile = os.path.abspath("\home\\nao\qitopics_enu.top")




def pdfConnection(tts,connectionToPdf):
    
    is_Connected = connectionToPdf.connection()
    if not is_Connected:
        tts.say("The PDF Application is not opened.")
        tts.say("Please open the PDF displayer so that I can show the book to you.")
        time.sleep(1)
        tts.say("When the PDF displayer opened, please talk to me")
    else:
        tts.say("Connected to PDF displayer")
    dialog.subscribe('myModule')
    #dialog.activateTopic(topic)
    print "initilized dialog"
    while(not is_Connected):
        
        time.sleep(0.5)
        
        #dialog.subscribe('myModule')

        # Activate dialog
        dialog.activateTopic(topic)
        
        memoryProxy.removeData("Dialog/Answered")
        memoryProxy.subscribeToEvent("Dialog/Answered","Dialog",IP)
        #time.sleep(5)
        
        dialogOutput = memoryProxy.getData("Dialog/Answered")
        print "first dialog debug", dialogOutput
        while(dialogOutput == None):
            print "no response"
            time.sleep(1)
            dialogOutput = memoryProxy.getData("Dialog/Answered")
            
            print dialogOutput
        memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")
        if dialogOutput.startswith("Ok , Let me check the connection"):
            print "debug"
            #tts.say("Let me check the connection to PDF Displayer")
            is_Connected = connectionToPdf.connection()
        
            if not is_Connected:
                tts.say("I still can't find the displayer")
                tts.say("Can you double check the PDF application.")
                tts.say("Thanks a lot!")
                dialog.deactivateTopic(topic)

                #Used at testing phase skip the connection
                dialog.unloadTopic(topic)
                # Stop dialog
                dialog.unsubscribe('myModule')
                #memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")
                is_Connected = True


            else:
                dialog.deactivateTopic(topic)

                # Unload topic
                dialog.unloadTopic(topic)
                # Stop dialog
                dialog.unsubscribe('myModule')
                #memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")
        



        

        

       
    
def trackChild(tracker,faceProxy,peopleProxy):
    targetName = "People"
    faceWidth = 0.2
    peopleProxy.setTimeBeforePersonDisappears(10)
    #peopleProxy.subscribeToEvent("PeoplePerception/PeopleList")
    memoryProxy.removeData("PeoplePerception/PeopleList")
    memoryProxy.subscribeToEvent("PeoplePerception/PeopleList","PeopleTracker",IP)
    tts.say("Hello my friend, please show your face to me if you are ready to read with me")
    PeopleId = memoryProxy.getData("PeoplePerception/PeopleList")
    while(PeopleId == None or len(PeopleId) ==0):
        time.sleep(2)
        PeopleId = memoryProxy.getData("PeoplePerception/PeopleList")

    print PeopleId
    tracker.registerTarget(targetName, PeopleId)
    #tracker.registerTarget(targetName, faceWidth)
    # Then, start tracker.
    tracker.track(targetName)
    print "ALTracker successfully started, now show your face to robot!"
    
    #faceProxy.clearDatabase()
    #faceProxy.setTrackingEnabled(True)
    #faceProxy.subscribe("Child", 600, 0.0 )
    #tracker.toggleSearch(True)
    #motion.wakeUp()
    #motion.stiffnessInterpolation("Head", 1.0, 1.0)
    #tts.say("If you are ready to read with me, please look at me")
    try:
        while(tracker.isTargetLost()):
            
            #faceProxy.learnFace("Child")
            search = tracker.isSearchEnabled()
            print search
            #if not search:
            #tracker.toggleSearch(True)
            time.sleep(2)
            #tracker.toggleSearch(False)
            #tracker.toggleSearch(False)
            print"looking for target"
            
    except KeyboardInterrupt:
        printc
        print"Interrupted by user"
    #faceData = memoryProxy.getData("FaceDetected")
    #tracker.toggleSearch(False)
    """faceData = faceProxy.getLearnedFacesList()
    if len(faceData) == 0:
        faceProxy.learnFace("Child")
        time.sleep(8)
    print faceData"""
    PeopleId = memoryProxy.getData("PeoplePerception/PeopleList")
    memoryProxy.unsubscribeToEvent("PeoplePerception/PeopleList","PeopleTracker")
    print PeopleId
    
    

    
def dialogSetup(self,topics,is_Topic):
    dialog.subscribe('myModule')
    dialog.activateTopic(topics)
    #dialog.forceOutput()
    if is_Topic:

        dialog.gotoTopic("begin")
    memoryProxy.removeData("Dialog/Answered")
    memoryProxy.subscribeToEvent("Dialog/Answered","Dialog",IP)

    dialogOutput = memoryProxy.getData("Dialog/Answered")
    while(dialogOutput == None):
        time.sleep(1)
        dialogOutput = memoryProxy.getData("Dialog/Answered")
    dialog.deactivateTopic(topic)
    # Unload topic
    #dialog.unloadTopic(topic)
    # Stop dialog
    dialog.unsubscribe('myModule')
    memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")
    
    return dialogOutput



if __name__ == "__main__":
    

    
    tts = ALProxy("ALTextToSpeech", IP,Port)
    
    asr = ALProxy("ALSpeechRecognition", IP, Port)
    memoryProxy = ALProxy("ALMemory", IP, Port)
    motion = ALProxy("ALMotion", IP ,Port)
    postureProxy = ALProxy("ALRobotPosture", IP, Port)
    tracker = ALProxy("ALTracker", IP, Port)
    faceProxy = ALProxy("ALFaceDetection", IP, Port)
    voice = Sound.SoundFeedback(asr,memoryProxy,IP)
    peopleProxy = ALProxy("ALPeoplePerception",IP,Port)
    dialog = ALProxy('ALDialog', IP, Port)
    dialog.setLanguage("English")
    dialogFile = dialogFile.decode('utf-8')
    topic = dialog.loadTopic(dialogFile.encode('utf-8'))
    dialogFile_Begin = dialogFile_Begin.decode('utf-8')
    topic2 = dialog.loadTopic(dialogFile_Begin.encode('utf-8'))
    connectionToPdf = PDF_Client.client()

    

    #Setup Connection to PDF
    pdfConnection(tts,connectionToPdf)
    tts.say("Connection successful")
    tts.say("Now, initializing calibration")
    
    #Setup Calibration
    armMotion = arm.ArmMotion(motion,memoryProxy,postureProxy)
    calibrationInstance = calibration.Calibrations(motion,postureProxy,tts,IP,Port,armMotion)
    calibrationInstance.setupCalibration(memoryProxy)
    print "ready for reading"
    
    
    dialog.subscribe('myModule')
    dialog.activateTopic(topic2)
    #dialog.forceOutput()
    dialog.gotoTopic("begin")
    memoryProxy.removeData("Dialog/Answered")
    memoryProxy.subscribeToEvent("Dialog/Answered","Dialog",IP)
    #time.sleep(5)
    
    dialogOutput = memoryProxy.getData("Dialog/Answered")
    while(dialogOutput == None):
        time.sleep(1)
        dialogOutput = memoryProxy.getData("Dialog/Answered")

    print "second dialog debug", dialogOutput
    while(True):
        print "checking loop"
        if dialogOutput.startswith("Alright"):
            print "alright debug"
            #dialog.stopPush()
            dialog.deactivateTopic(topic)
            # Unload topic
            #dialog.unloadTopic(topic)
            # Stop dialog
            dialog.unsubscribe('myModule')
            memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")

            print "initilizing tracker"
            trackChild(tracker,faceProxy,peopleProxy)
            print "begin read author"
            readInstance = Reader.Reader(convertedFile,tts,tracker,connectionToPdf,IP)
            readInstance.readAuthor()
            dialogOutput = dialogSetup(topic,False)
            

            
            
            break
        else:

            time.sleep(1)
            dialogOutput = memoryProxy.getData("Dialog/Answered")





    
    """tts.say("Now I'm propertly setup.")
    tts.say("Do you want to begin now?")
    
    
    data = voice.getVoiceRec()
    if not data[0] == "no":
        tts.say("Alright, we are ready to go!")
        #Setup Face Tracker
        trackChild(tracker,faceProxy,peopleProxy)
    else:
        tts.say("Ok!")
        tts.say("Let me know when you are ready")
        data = voice.waitFeedback()
        if data:
            #Setup Reader
            tts.say("Alright, we are ready to go!")
            readInstance = Reader.Reader(convertedFile,tts,tracker,connectionToPdf)
            readInstance.readAuthor()"""
            
    

    
    
    time.sleep(1)
    

    
    #The robot will stand up at this sytax sometimes. No idea why
    """data = voice.getVoiceRec()
    if data[0] == "yes":
        tts.say("Do you remember what we liked about that story? Here's another book by this author.")
        tts.say("Let's read this one and see if we like it as well as the other book we read")
    else:
        tts.say("OK! Let's read it")"""

    readInstance = Reader.Reader(convertedFile,tts,tracker,connectionToPdf,IP)
    readInstance.readContent(memoryProxy,asr,armMotion,dialog,topic)


    
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.rest()


