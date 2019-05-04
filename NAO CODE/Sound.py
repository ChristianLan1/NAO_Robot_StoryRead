import time
class SoundFeedback:
    def __init__(self,asr,memoryProxy,IP):
        self.asr = asr
        self.memoryProxy = memoryProxy
        self.IP = IP
        
    def getVoiceRec(self):
        self.asr.setVisualExpression(True)
        self.asr.pause(True)
        self.asr.setLanguage("English")

        vocabulary = ["yes", "no"]

        self.asr.setVocabulary(vocabulary, False)
        self.asr.subscribe(self.IP)
        print "speech recognition engine started"

        #memoryProxy = ALProxy("ALMemory", self.IP, 9559)
        self.memoryProxy.subscribeToEvent('WordRecognized',self.IP,self.IP)
        #asr.removeAllContext()
        self.asr.pause(False)
        time.sleep(5)

        self.asr.unsubscribe(self.IP)

        data= self.memoryProxy.getData("WordRecognized")
        print( "data: %s" % data )
        
        return data
    def waitFeedback(self):
        self.asr.setVisualExpression(True)
        self.asr.pause(True)
        self.asr.setLanguage("English")

        vocabulary = ["yes", "ok","done","connected","finished"]

        self.asr.setVocabulary(vocabulary, False)
        self.asr.subscribe(self.IP)
        print "speech recognition engine started"
        #isFeedback = self.memoryProxy.subscribeToEvent("SpeechDetected",self.IP,self.IP)
            
        #memoryProxy = ALProxy("ALMemory", self.IP, 9559)
        """while(not isFeedback):
            time.sleep(1)
            isFeedback = self.memoryProxy.subscribeToEvent("SpeechDetected",self.IP,self.IP)"""
        self.memoryProxy.subscribeToEvent('WordRecognized',self.IP,self.IP)
        #asr.removeAllContext()
        
        self.asr.pause(False)
        self.asr.setAudioExpression(False)
        while(True):

            time.sleep(2)
            print "listening"
        
        
            data=self.memoryProxy.getData("WordRecognized")
            if not data[0] =='':
                print data
                if data[1] < 0.5:
                    continue
                else:
                    break
            
                
        self.memoryProxy.unsubscribeToEvent('WordRecognized',self.IP)
        self.asr.unsubscribe(self.IP)
        return data