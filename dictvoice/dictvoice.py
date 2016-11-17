# -*- coding: utf-8 -*-
import os,winsound,win32com.client,time,threading

class Dvoice(threading.Thread):

    def __init__(self, *args, **kwargs):

        super(Dvoice, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

        self.directory=u'F:/BaiduNetdiskDownload/[142000].voice/voice'
        self.wordfile=u'f1.txt'
        self.speaker=win32com.client.Dispatch("SAPI.Spvoice")
        self.mutexlock=threading.Lock()
        self.interval,self.timesleep=0.7,1.5
        self.repeatnum=5

        self.speaker.Voice=self.speaker.GetVoices().Item(1)
        self.speaker.Rate=-3
        self.speaker.Volume=99

    def setWordFile(self,wfile):
        self.wordfile=wfile

    def setDirectory(self,vfiles):
        self.directory=vfiles

    def _prepare(self):
        #read all words
        with open(self.wordfile,"r") as wfile:
            content=wfile.read()
        #load all wav files
        wordmap={}
        for path,_,filenames in os.walk(self.directory):
            for f in filenames:
                if not f.endswith('.wav'): continue
                word=f[0:-4]
                voice=path+'/'+f
                wordmap[word]=voice
        return content,wordmap

    def _playaudio(self,f,n,t1,t2):
        time.sleep(t2)
        for i in range(n):
            winsound.PlaySound(f,winsound.SND_FILENAME|winsound.SND_NOWAIT)
            if self.stopped(): break
            time.sleep(t1)

    def _ttsaudio(self,word,n,t1,t2):
        time.sleep(t2)
        for i in range(n):
            self.speaker.Speak(word)
            if self.stopped(): break
            time.sleep(t1)

    def setparams(self,i=0.7,t=1.5):
        self.mutexlock.acquire()
        self.interval=i
        self.timesleep=t
        self.mutexlock.release()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        content,wordmap=self._prepare()
        self.setparams()
        while not self.stopped():
            for w in content.split('\n'):
                w=w.strip()
                if len(w)==0 : continue
                if self.stopped(): break
                self.mutexlock.acquire()
                t1,t2=self.interval,self.timesleep
                self.mutexlock.release()
                if wordmap.has_key(w):
                    self._playaudio(wordmap[w],self.repeatnum,t1,t2)
                else:
                    self._ttsaudio(w,self.repeatnum,t1,t2)

if __name__ == '__main__':
    d=Dvoice()
    d.setDirectory('F:/BaiduNetdiskDownload/[142000].voice/voice')
    d.start()
    time.sleep(60)
    d.stop()
