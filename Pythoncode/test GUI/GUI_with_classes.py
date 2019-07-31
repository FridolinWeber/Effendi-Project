# -*- coding: utf-8 -*-

# File name: GUI-with-classes.py
# Author: Fridolin Weber, Saad Nasir
# Date created: 16.04.2018
# Date last modified: 01.05.2018
# Python Version: 2.7


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import datatracker
import datatracker_main


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        loadUi("my_test_gui.ui", self)

        self.connect(self.startFunction, SIGNAL("clicked()"), self.selectFunction)
        self.connect(self.writeCom, SIGNAL("clicked()"), self.setComport)
        self.connect(self.confirmName, SIGNAL("clicked()"), self.documentName)

    def selectFunction(self):
        '''
        function that selects the sensor type
        '''
        if self.SensorSelect.currentText() == "Prototyp":
            datatracker_main.main()

    def setComport(self):
        '''
        change the com Port to the port of the Device. The current port of the Arduino can be read out under Device Manager
        '''
        port = str(self.comboBox.currentText())
        print port
        datatracker.strPort = port

    def documentName(self):
        '''
        default name of document to save
        '''
        print(self.lineEdit.text())
        if self.SensorSelect.currentText() == "Force Pressure / Piezo Sensor":
            datatracker.docName = self.lineEdit.text()
        if self.SensorSelect.currentText() == "MPU6050":
            datatracker_main.docName = self.lineEdit.text()

def main():
    app = QApplication(sys.argv)
    NewWindow = MyWindow(None)
    NewWindow.show()
    sys.exit(app.exec_())

# call main
if __name__ == '__main__':
    main()
