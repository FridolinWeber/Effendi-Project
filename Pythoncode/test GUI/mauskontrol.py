#!usr/bin/env python

# File name: datatracker_main.py
# Author: Fridolin Weber, Diyar Guer
# Date created: 16.04.2018
# Date last modified: XX
# Python Version: 2.7
# many code parts taken from http://electronut.in/plotting-real-time-data-from-arduino-using-python/

# this code reads the serial input of comX, which is always one value that is read out from one force pressure sensor. The data is saved
# into a txt.file and a live plot takes place
# still unknown error if there is an error in conversion


import sys, serial
from ctypes import windll, Structure, c_long, byref
import win32gui, win32api, win32con
from time import sleep
import glob
import pyautogui as pag
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


def listSerialPort(): #this function is used to list all of the aktive serial ports.
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

print("# Serial Ports")
ports = listSerialPort()

while True:# an infinity loop is used in case of an error while choosing the port
    for port in ports:
        print("\t># " + str(port))

        pickPort = port
        if(pickPort in ports):#is the picked port active?
            break
        else:
            print("There is no such a port!")
    break

while True:
    sensitivity = 1;
    sens = [10,9,8,7,6,5,4,3,2,1]
    pickSensitivity = int(input("\n>> Choose Sensitivity [1-10] : "))

    if(pickSensitivity < 1 or sensitivity > 10):

        print("# Invalid Value!")
    else:
        sensitivity = int(sens[pickSensitivity-1])

        break

class Mouse:
    MOUSEEVENTF_MOVE = 0x0001 # mouse move
    MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down
    MOUSEEVENTF_LEFTUP = 0x0004 # left button up
    MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down
    MOUSEEVENTF_RIGHTUP = 0x0010 # right button up
    MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down
    MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up
    MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled
    MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1


class Point (Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def mousePos():
    pt = Point()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}


def moveMouse(X,Y):
    windll.user32.SetCursorPos(X, Y)


#Screen Resolution
screen = pag.size()
screenX = screen[0]
screenY = screen[1]

#Mouse Position
pos = mousePos()
posX = int(pos['x'])
posY = int(pos['y'])

#Mouse Object
mouse = Mouse()


# plot class
class AnalogPlot:
    def __init__(self, port, maxLen):
        '''
        deques are data containers that can be rapidly accessed for reading and writing. Those
        containers will temporarily save the values that are read out from the sensors and will be
        plotted onto the y axis. maxLen is the maximum number of values that are stored in the deques.
        The Baud Rate of Serial has to be the same as the Baud rate of the Arduino.
        '''
        self.ser = serial.Serial(port, 38400)
        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)

        self.maxLen = maxLen
        self.cnt = 0

    def addToBuf(self, buf, val):
        '''
        the current read out values are appended to the deques. buf.pop() deletes the oldest value in the
        deques.
        '''
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val) #ax list is updated with the current value from the readout

    def add(self, data):
        '''
        this function calls the addToBuf function that adds the read out values to the buffer.
        '''
        assert (len(data) == 2)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])


        while True:
            self.ser.write(".") #Python sends a "." to the Arduino which causes the Arduino to write the current position to the Serial Port if this feature ist not used the transfer of data is far too slow
            line = self.ser.readline()
            #convertList = (line.split(";"))[0:2]


            newValue = line.decode('uft-8')
            newValue = newValue[:-2]

            coordinate = newValue.split(',')

            coorX = int(coordinate[0])
            coorX = int(coorX/sensitivity)

            coorY = int(coordinate[1])
            coorY = int(coorY/sensitivity)

            if(posX>=screenX):
                posX = screenX
            elif(posX<=0):
                posX=0

            if(posY>=screenY):
                posY = screenY
            elif(posY<=0):
                posY=0

            if(coorX<(-10/sensitivity) or coorX>(10/sensitivity)):
                posX += coorX

            if(coorY<(-10/sensitivity) or coorY>(10/sensitivity)):
                posY += coorY



            moveMouse(posX, posY)
