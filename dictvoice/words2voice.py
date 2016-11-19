from PyQt5 import QtCore
import threading,time
import os,winsound,win32com.client
from datasbuilder import *

class W2Vthread(QtCore.QThread):
    
    update = QtCore.pyqtSignal(str)
    
    def __init__(self, parent):

        super(W2Vthread, self).__init__(parent)

        self.mutexlock=threading.Lock()
        self.stopped=True #not run yet, so stopped

        self.interval,self.timesleep=0.7,1.5
        self.repeatnum=5

        self.wordfile='f1.txt'

    def _playaudio(self,f,n,t1,t2):
        time.sleep(t2)
        for i in range(n):
            winsound.PlaySound(f,winsound.SND_FILENAME|winsound.SND_NOWAIT)
            if self.isStopped(): break
            time.sleep(t1)

    def _ttsaudio(self,word,n,t1,t2):
        time.sleep(t2)
        for i in range(n):
            speak(word)
            if self.isStopped(): break
            time.sleep(t1)

    def setparams(self,i=0.7,t=1.5):
        self.mutexlock.acquire()
        self.interval=i
        self.timesleep=t
        self.mutexlock.release()

    def setWordFile(self,wf):

        self.wordfile=wf
    
    def _prepare(self):#load wordfile & wavs
        
        with open(self.wordfile,"r") as wfile:
            content=wfile.read()
        #load all wav files
        wordset=content.split()
        getWavs(wordset)
        wordmap={}
        for path,_,filenames in os.walk('audio'):
            for f in filenames:
                if not f.endswith('.wav'): continue
                word=f[0:-4]
                voice=path+'/'+f
                wordmap[word]=voice
        return content,wordmap

    def setStop(self,s):

        self.mutexlock.acquire()
        self.stopped=s
        self.mutexlock.release()
 
    def isStopped(self):

        return self.stopped

    def run(self):

        content,wordmap=self._prepare()
        self.stopped=False #run

        while not self.isStopped():

            for w in content.split('\n'):
                w=w.strip()
                if len(w)==0 : continue
                if self.isStopped(): break
                #emit
                self.update.emit(w)
                #get params
                self.mutexlock.acquire()
                t1,t2=self.interval,self.timesleep
                self.mutexlock.release()

                if wordmap.has_key(w):
                    self._playaudio(wordmap[w],self.repeatnum,t1,t2)
                else:
                    #self._ttsaudio(w,self.repeatnum,t1,t2)
                    time.sleep(10)

 
if __name__=="__main__":
    print 0
