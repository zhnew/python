#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication,QPushButton,QComboBox,QLabel)
from PyQt5.QtGui import QIcon,QColor

import dictvoice

class Example(QMainWindow):
    
    def __init__(self):
        super(Example,self).__init__()
        self.initUI()
        self.wordfile=""
        self.voicedirectory=""
        self.dv=""
        
    def initUI(self):      
    
        btn1=QPushButton("voices",self)
        btn1.move(30,40)
        
        btn2=QPushButton("words",self)
        btn2.move(30,80)

        btn1.clicked.connect(self.selectvoices)
        btn2.clicked.connect(self.selectwords)

        self.textShow=QTextEdit(self)
        self.textShow.setReadOnly(True)
        self.textShow.setTextColor(QColor('red'))
        self.textShow.setTextBackgroundColor(QColor('gray'))
        self.textShow.setFixedSize(300,100)
        self.textShow.move(159,40)
        
        label1=QLabel("interval",self)
        label1.move(30,120)
        combo1 = QComboBox(self)
        combo1.addItem("0.5")
        combo1.addItem("0.7")
        combo1.addItem("0.9")
        combo1.addItem("1.1")
        combo1.setFixedSize(50,30)
        combo1.move(90,120)
        self.combo1=combo1

        label2=QLabel("timesleep",self)
        label2.move(30,160)
        combo2 = QComboBox(self)
        combo2.addItem("0.5")
        combo2.addItem("0.7")
        combo2.addItem("0.9")
        combo2.addItem("1.1")
        combo2.addItem("1.3")
        combo2.addItem("1.5")
        combo2.setFixedSize(50,30)
        combo2.move(90,160)
        self.combo2=combo2
        
        btn3 = QPushButton("start",self)
        btn3.move(30,200)

        btn4=QPushButton("stop",self)
        btn4.move(30,240)

        btn3.clicked.connect(self.startPlay)
        btn4.clicked.connect(self.stopPlay)
        
        self.setGeometry(300, 300, 550, 300)
        self.setWindowTitle('words speaker')
        self.show()
        
    def selectwords(self):

        wordsfile=QFileDialog.getOpenFileName(self,'Open file','D:/Users/zhn/Documents/src/python/voice')
        text=self.textShow.toPlainText()
        text+="\n"+"words files is: "+wordsfile[0]
        self.textShow.setText(text)
        self.wordfile=wordsfile[0]

    def selectvoices(self):

        voicesdir=QFileDialog.getExistingDirectory(self,'voices director','F:/BaiduNetdiskDownload/[142000].voice/voice')
        text=self.textShow.toPlainText()
        text+="\n"+"voices in directory: "+voicesdir
        self.textShow.setText(text)
        self.voicedirectory=voicesdir

    def startPlay(self):
        interval=float(str(self.combo1.currentText()))
        timesleep=float(str(self.combo2.currentText()))
        self.dv=dictvoice.Dvoice()
        self.dv.setWordFile(self.wordfile)
        self.dv.setDirectory(self.voicedirectory)
        self.dv.setparams(interval,timesleep)
        self.dv.start()

    def stopPlay(self):
       self.dv.stop()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
