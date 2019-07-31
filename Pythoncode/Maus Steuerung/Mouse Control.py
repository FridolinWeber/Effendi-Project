#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This librarys are for the mouse
from ctypes import windll, Structure, c_long, byref
import win32gui, win32api, win32con

#Sleep Function
from time import sleep

#Pyautogui
import pyautogui

#Serial port and system librarys
import sys
import glob
import serial

pyautogui.FAILSAFE = False
baudrate = 38400

#a function that allows you to list all active ports
def listSerialPort():
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
arduino = serial.Serial(activePort, baudrate)

#Selecting sensitivity
while True:
    sensitivity = 1
    senn = [10,9,8,7,6,5,4,3,2,1]
    selectSen = int(input("\n>> Sensitivity [1-10] : "))
    #Is sensitivit between 1-10 ?
    if(selectSen < 1 or selectSen > 10):
        #Select a valid value
        print("# Invalid Sensitivity")
    else:
        #Pick the sensitivity
        sensitivity = int(senn[selectSen-1])
        #Get out of the loop
        break

#Mouse Object
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


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

#Pulling the actual position of the mouse
def mousePos():
    point = POINT()
    windll.user32.GetCursorPos(byref(point))
    return {"x": point.x, "y": point.y}

#According to X, Y values setting the mouse position
def moveMouse(X, Y):
    windll.user32.SetCursorPos(X, Y)

#Screen resolution
width, height = pyautogui.size()
screenX = width
screenY = height

#Actual position of the mouse
pos = mousePos()
posX = int(pos['x'])
posY = int(pos['y'])

#Mouse object
mouse = Mouse()

print("\n# Starts in 3 Seconds")
print("\n# --Strg+C-- to stop ")
sleep(3)

previousClickValue0 = 0
pressedValue = 200
unPressedValue = 100
mouseDown = False

#Entering the endless loop
try:
    while True:

        #Read the last value of the serial port from arduino
        value = arduino.readline()

        #Transform the byte values to the string
        newValue = value.decode('utf-8')
        #remove the last characters '\n\r'
        newValue = newValue[:-2]

        #Split the valuse that comes from serialport ','
        coordinate = newValue.split(',')

        #The X coordinate
        #If you do want to pass a string representation of a float to an int, you can convert to a float first, then to an integer
        coorX = int(float(coordinate[0]))
        coorX = int(2 * coorX / sensitivity)

        #the Y Coordinate
        coorY = int(float(coordinate[1]))
        coorY = int(2 * coorY / sensitivity)

        print(coorX, coorY)

        #If the position_X of the mause at the beginning of the screen
        if(posX >= screenX):
            posX = screenX
        elif(posX <= 0):
            posX = 0

        #If the position_Y of the mause at the beginning of the screen
        if(posY >= screenY):
            posY = screenY
        elif(posY <= 0):
            posY = 0

        #If the X_Values are not between -10 and 10
        #if(coorX < (-10 / sensitivity) or coorX > (10 / sensitivity)):
        #MOUSE_X, increase as much as coorX
        posX += coorX

        #If the Y_Values are not between -10 and 10
        #if(coorY < (-10 / sensitivity) or coorY > (10 / sensitivity)):
        #MOUSE_Y, increase as much as coorY
        posY += coorY
        print(coorX, coorY)
        moveMouse(posX, posY)

        #Click function
        currentValue = int(coordinate[2])
        if (currentValue > pressedValue and mouseDown == False):
            mouseDown = True
            pyautogui.mouseDown()
        elif (currentValue < unPressedValue and mouseDown == True):
            mouseDown = False
            pyautogui.mouseUp()


except KeyboardInterrupt:
    sys.exit(0)
except:
    print("fuckkk")
