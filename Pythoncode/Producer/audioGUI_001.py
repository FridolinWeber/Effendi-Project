# -*- coding: utf-8 -*-

# File name: audioGUI_001.py
# Author: Fridolin Weber, Saad Nasir
# Date created: 16.04.2018
# Date last modified: 01.05.2018
# Python Version: 2.7

'''
computer has to be connected to the internet!! otherwise the sound to text module will not work
'''
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import storeAudio_test_002
import speakrecognizer_001

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        loadUi("ui_audio.ui", self)
        self.connect(self.runAudio, SIGNAL("clicked()"), self.run_function)


    def run_function(self):
        if self.AudioToText.isChecked() == True:
            speakrecognizer_001.recognizer()
            self.TextEdit.insertPlainText(speakrecognizer_001.output)

        if self.recordAudio.isChecked() == True:
            if self.recordTime.value() != 0:
                storeAudio_test_002.time_of_record = self.recordTime.value()
            if self.fileName.text() != "":
                storeAudio_test_002.filename = str(self.fileName.text())
            else:
                storeAudio_test_002.filename = "output"
            storeAudio_test_002.main()

def main():
    app = QApplication(sys.argv)
    NewWindow = MyWindow(None)
    NewWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
