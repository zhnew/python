#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we select a file with a
QFileDialog and display its contents
in a QTextEdit.

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication,QPushButton,QComboBox,QLabel)
from PyQt5.QtGui import QIcon,QColor


class Example(QMainWindow):
    
    def __init__(self):
        super(Example,self).__init__()
        
        self.initUI()
        
        
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

        label2=QLabel("timesleep",self)
        label2.move(30,160)
        combo2 = QComboBox(self)
        combo2.addItem("0.5")
        combo2.addItem("0.7")
        combo2.addItem("0.9")
        combo2.addItem("1.1")
        combo2.setFixedSize(50,30)
        combo2.move(90,160)

        self.setGeometry(300, 300, 550, 300)
        self.setWindowTitle('words speaker')
        self.show()
        
    def selectwords(self):

        wordsfile=QFileDialog.getOpenFileName(self,'Open file','/home')
        text=self.textShow.toPlainText()
        text+="\n"+"words files is: "+wordsfile[0]
        self.textShow.setText(text)

    def selectvoices(self):

        voicesdir=QFileDialog.getExistingDirectory(self,'voices director','/home')
        print voicesdir
        text=self.textShow.toPlainText()
        text+="\n"+"voices in directory: "+voicesdir
        self.textShow.setText(text)

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
