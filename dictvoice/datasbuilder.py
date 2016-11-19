import sqlite3,os
import win32com.client
import re,urllib

speaker=win32com.client.Dispatch("SAPI.SpVoice")
speaker.Voice=speaker.GetVoices().Item(1)
speaker.Rate=-3
speaker.Volume=99

def speak(w):
    speaker.Speak(w)

#only run one time
def _makeVoices():

    conn=sqlite3.connect('voices.db')
    c=conn.cursor()
    
    c.execute('''create  table voice(word text primary key, wav blob)''')
    conn.commit()

    count=0

    for path,_,filenames in os.walk("F:/BaiduNetdiskDownload/[142000].voice/voice"):
        for f in filenames:
            if not f.endswith('.wav'):continue
            word=f[0:-4]
            voice=path+'/'+f
            with open(voice,'rb') as f:
                voice=sqlite3.Binary(f.read())
            c.execute("insert into voice(word,wav) values(?,?)",(word,voice))
            count+=1
            print count
            if count%1000==0 :
                conn.commit()

    conn.close()

def getWavs(words):

    conn=sqlite3.connect('voices.db')
    c=conn.cursor()

    wordslist=""
    for w in words:
        w="'"+w+"'"
        wordslist+=w+','
    wordslist=wordslist[:-1]

    c.execute("select word,wav from voice where word in ({seq})".format(seq=wordslist))

    rows=c.fetchall()

    #make a directory audio
    audio="audio"
    from os.path import isdir,isfile
    if not isdir(audio):
        os.mkdir(audio)

    for row in rows:
        word= row[0]
        word=audio+"/"+word+".wav"
        if isfile(word):continue
        with open(word,'wb') as f:
            f.write(row[1])

    conn.close()

def getWord(word):
    
    conn=sqlite3.connect('oald_cn.dict.sqlite')
    cur=conn.cursor()
    sql="select * from data where word='{w}'".format(w=word)
    cur.execute(sql)
    row=cur.fetchone()
    conn.close()
    if row is None:
        return youdao(word) 
    
    text=""
    text=row[1]+"\n"+row[2]+"\n"+row[3]+"\n"+row[4]+"\n"+row[5]+"\n"+row[6]+"\n"+row[7]+"\n"+row[8]+"\n"+row[9]+"\n"+row[10]
    if len(text)<20:
        return youdao(word)
    return text

def youdao(word):

    url='http://dict.youdao.com/search?q=%s'%word
    content=urllib.urlopen(url)
    pattern=re.compile("</h2.*?</ul>",re.DOTALL)
    result=pattern.search(content.read()).group()
    pattern2=re.compile('<li>.*?</li>')
    text=""
    for i in pattern2.findall(result):
        text+=i.strip('<li>').strip('</li>').decode('utf-8')+"\n"
    return text

def text2html(text):
    t1=text.find('/')
    if t1== -1 : return text
    t2=text[t1+1:].find('/')
    if t2==-1 : return text
    text="<div style='font-size:15px'>"+text+""
    return text

if __name__=='__main__':
    #words=('time','go','dog','cat')
    #getWavs(words)
    #print getWord('time')
    #_makeVoices()
    #speak('time')
    #print text2html(text)
    print 0
