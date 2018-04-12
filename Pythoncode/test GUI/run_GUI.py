# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import datatracker


app = QApplication(sys.argv)

w = loadUi("my_test_gui.ui")

def setComport():
    port = str(w.comboBox.currentText())
    print port
    datatracker.strPort = port

def documentName():
    print(w.lineEdit.text())
    datatracker.docName = w.lineEdit.text()

w.connect(w.startFunction, SIGNAL("clicked()"), datatracker.main) #w enthält Referenz auf das gebaute Fenster

w.connect(w.writeCom, SIGNAL("clicked()"), setComport)

w.connect(w.confirmName, SIGNAL("clicked()"), documentName)

w.show()
sys.exit(app.exec_())
