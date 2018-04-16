# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import datatracker
import data_MPU6050


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        loadUi("my_test_gui.ui", self)

        self.connect(self.startFunction, SIGNAL("clicked()"), self.selectFunction) #w enthält Referenz auf das gebaute Fenster
        self.connect(self.writeCom, SIGNAL("clicked()"), self.setComport)
        self.connect(self.confirmName, SIGNAL("clicked()"), self.documentName)

    def selectFunction(self):
        if self.SensorSelect.currentText() == "Force Pressure / Piezo Sensor":
            datatracker.main()
        if self.SensorSelect.currentText() == "MPU6050":
            data_MPU6050.main()

    def setComport(self):
        port = str(self.comboBox.currentText())
        print port
        datatracker.strPort = port

    def documentName(self):
        print(self.lineEdit.text())
        datatracker.docName = self.lineEdit.text()

def main():
    app = QApplication(sys.argv)
    NewWindow = MyWindow(None)
    NewWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
