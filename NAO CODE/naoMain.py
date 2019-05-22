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
bookInfo = 'C:\Users\Christian Lan\OneDrive\NAO CODE\\books\\book_pages.txt'
bookInfoZoe = 'C:\Users\Zoe Chai\Desktop\\books\\book_pages.txt'
authorL = 'C:\Users\Christian Lan\OneDrive\\nao_story_read\NAO CODE\outputAuthor.txt'
contentL = 'C:\Users\Christian Lan\OneDrive\\nao_story_read\NAO CODE\outputContent.txt'
authorZ = 'C:/Users/Zoe Chai/Desktop/nao/nao_story_read/NAO CODE/outputAuthor.txt'
contentZ = 'C:/Users/Zoe Chai/Desktop/nao/nao_story_read/NAO CODE/outputContent.txt'

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
    dialog.subscribe('myModule1')
    #dialog.activateTopic(topic)
    print "initilized dialog"
    while(not is_Connected):
        
        time.sleep(0.5)
        
        #dialog.subscribe('myModule')

        # Activate dialog
        #dialog.activateTopic(topic)
        #dialog.setFocus(topic)
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
                #dialog.deactivateTopic(topic)

                #Used at testing phase skip the connection
                """dialog.unloadTopic(topic)
                # Stop dialog
                dialog.unsubscribe('myModule1')
                #memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")
                is_Connected = True"""


            #else:
                #dialog.deactivateTopic(topic)

                # Unload topic
                #dialog.unloadTopic(topic)
                # Stop dialog
                #dialog.unsubscribe('myModule1')
                #memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")
    dialog.unsubscribe('myModule1')
        



        

        

       
    
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
            PeopleId = memoryProxy.getData("PeoplePerception/PeopleList")
            #faceProxy.learnFace("Child")
            while(PeopleId == None or len(PeopleId) ==0):
                time.sleep(2)
                PeopleId = memoryProxy.getData("PeoplePerception/PeopleList")

            print PeopleId
            tracker.registerTarget(targetName, PeopleId)
            #search = tracker.isSearchEnabled()
            #print search
            #if not search:
            #tracker.toggleSearch(True)
            time.sleep(1)
            #tracker.toggleSearch(False)
            #tracker.toggleSearch(False)
            print"looking for target"
            
    except KeyboardInterrupt:
        
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
    
    

    
def dialogSetup(topics,is_Topic):
    print "debug standup0"
    #time.sleep(10)
    dialog.subscribe('myModule1')
    print "debug standup0.5"
    #time.sleep(5)
    #dialog.activateTopic(topics)
    #dialog.setFocus(topics)
    #dialog.forceOutput()
    #This is where it stand up!
    print "debug standup1"
    #time.sleep(10)
    if is_Topic:
        print "debug standup1.5"
        #time.sleep(10)
        dialog.setFocus(topics)
        dialog.gotoTopic("begin")
    memoryProxy.removeData("Dialog/Answered")
    memoryProxy.subscribeToEvent("Dialog/Answered","Dialog",IP)
    print "debug standup2"
    time.sleep(10)
    dialogOutput = memoryProxy.getData("Dialog/Answered")
    while(dialogOutput == None):
        time.sleep(1)
        dialogOutput = memoryProxy.getData("Dialog/Answered")
    dialog.deactivateTopic(topics)
    # Unload topic
    #dialog.unloadTopic(topic)
    # Stop dialog
    dialog.unsubscribe('myModule1')
    memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")
    
    return dialogOutput

def getBookInfo():
    with open(bookInfo) as f:
        lines = f.readlines()
        #print lines
        book = []
        count = 0
        pages = []
        try:
            for line in lines:
                
                line = line.rstrip()
                print line
                if count==1:
                   
                    line = re.findall("[0-9]+",line)
                    for element in line:
                       pages.append(int(element))
                    line = pages

                book.append(line)
                count += 1
            print book

        except:
            print "Incorrect file format"
    return book
            
            




if __name__ == "__main__":
    #Initialize Proxy
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
    #Initilize Dialog
    dialog = ALProxy('ALDialog', IP, Port)
    dialog.setLanguage("English")
    dialogFile = dialogFile.decode('utf-8')
    topic = dialog.loadTopic(dialogFile.encode('utf-8'))
    dialogFile_Begin = dialogFile_Begin.decode('utf-8')
    topic2 = dialog.loadTopic(dialogFile_Begin.encode('utf-8'))
    dialog.activateTopic(topic)
    dialog.activateTopic(topic2)
    dialog.setAnimatedSpeechConfiguration({"bodyLanguageMode":"random"})
    #Getting book Info
    book = getBookInfo()
    #Parse Book by author and content
    convert(book[0],[0])
    convert(book[0],book[1])
    #memoryProxy.unsubscribeToEvent('ALSpeechRecognition/IsRunning',IP,IP)
    
    #Setup Connection to PDF
    connectionToPdf = PDF_Client.client()
    pdfConnection(tts,connectionToPdf)
    readInstance = Reader.Reader(authorL,contentL,tts,tracker,connectionToPdf,IP,book)
    tts.say("Connection successful")
    tts.say("Now, initializing calibration")
    
    #DataListName = memoryProxy.getEventList()
    #print DataListName
    #EventList = memoryProxy.getEventList()
    #print EventList
    
    #Setup Calibration
    armMotion = arm.ArmMotion(motion,memoryProxy,postureProxy,tts)
    #time.sleep(5)
    print "testing jump"
    #time.sleep(5)
    #armMotion.setupCalibration()
    print "ready for reading"
    #time.sleep(10)
    #Setup dialog to ask user if start to read"""
    motion.setStiffnesses("LHand",0.0)
    dialogOutput = dialogSetup(topic2,True)
    print "second dialog debug", dialogOutput
    while(True):
        print "checking loop"
        
        #If starts with alright, starting to read
        if dialogOutput.startswith("Alright"):
            print "alright debug"
            #dialog.stopPush()
            #dialog.deactivateTopic(topic)
            #dialog.unsubscribe('myModule')
            #memoryProxy.unsubscribeToEvent("Dialog/Answered","Dialog")

            print "initilizing tracker"
            trackChild(tracker,faceProxy,peopleProxy)
            print "begin read author"
            
            readInstance.readAuthor()
            dialogOutput = dialogSetup(topic,False)
         
            break
        else:

            time.sleep(1)
            dialogOutput =  dialogSetup(topic2,True)





    
    #tts.say("Now I'm propertly setup.")
    #tts.say("Do you want to begin now?")
    
    
    """data = voice.getVoiceRec()
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
            
    

    
    
    #time.sleep(1)
    

    
    #The robot will stand up at this sytax sometimes. No idea why
    """data = voice.getVoiceRec()
    if data[0] == "yes":
        tts.say("Do you remember what we liked about that story? Here's another book by this author.")
        tts.say("Let's read this one and see if we like it as well as the other book we read")
    else:
        tts.say("OK! Let's read it")"""

    #readInstance = Reader.Reader(convertedFile,tts,tracker,connectionToPdf,IP)
    connectionToPdf.turnPage()
    readInstance.readContent(memoryProxy,asr,armMotion,dialog,topic)

    
    
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.rest()


