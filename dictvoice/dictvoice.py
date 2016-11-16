# -*- coding: utf-8 -*-
import wave,pyaudio,os,winsound,win32com.client,time

directory=u'F:/BaiduNetdiskDownload/[142000].voice/voice/f'
wordfile=u'f1.txt'
wordmap={}

repeatnum=5
interval=0.7
timesleep=1.5

def playaudio(f,n):
    time.sleep(timesleep)
    for i in range(n):
        winsound.PlaySound(f,winsound.SND_FILENAME|winsound.SND_NOWAIT)
        time.sleep(interval)

volume=99
rate=-3
speaker=win32com.client.Dispatch("SAPI.Spvoice")
speaker.Voice=speaker.GetVoices().Item(1)
speaker.Rate=rate
speaker.Volume=volume

def ttsaudio(word,n):
    time.sleep(timesleep)
    for i in range(n):
        speaker.Speak(word)
        time.sleep(interval)

for _,_,filenames in os.walk(directory):
    for f in filenames:
        word=f[0:-4]
        voice=directory+'/'+f
        wordmap[word]=voice

with open(wordfile,"r") as wfile:
    content=wfile.read()

while True:
    for w in content.split('\n'):
        w=w.strip()
        if len(w)==0 : continue
        if wordmap.has_key(w):
            playaudio(wordmap[w],repeatnum)
        else:
            ttsaudio(w,repeatnum)

