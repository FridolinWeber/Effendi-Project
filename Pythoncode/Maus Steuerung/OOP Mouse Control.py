#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This librarys are for the mouse
from ctypes import windll, Structure, c_long, byref
import win32gui, win32api, win32con

#Sleep Function
from time import sleep

#Pyautogui is for screen resolution
import pyautogui
import pyautogui as pag

#Serial port and system librarys
import sys
import glob
import serial

class Arduino:
    #a function that allows you to list all active ports
    def listSerialPort(self):

        #If the code runs on WINDOWS
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]

        #If the code runs on LINUX
        elif sys.platform.startswith('linux'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        else:
            raise EnvironmentError('Unsupported Platform!!!')

        result = []

        #Test the ports that are active and add them as a result
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    ports = listSerialPort()

if len(ports) > 0:
    print("Connected to -> " + str(ports[0]))
else:
    print ("There isn't any active ports!!")

activePort = ports[0]

#Connect to Arduino
arduino = serial.Serial(activePort, 38400)
