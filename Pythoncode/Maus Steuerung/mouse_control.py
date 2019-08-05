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


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

#Pulling the actual position of the mouse
def mousePos():
    point = POINT()
    windll.user32.GetCursorPos(byref(point))
    return int(point.x), int(point.y)


#According to X, Y values setting the mouse position
def moveMouse(X, Y):
    windll.user32.SetCursorPos(X, Y)


def main(connected_port, sensitivity):

    pressedValue = 300
    unPressedValue = 100
    mouseDown = False

    # Connect to arduino
    arduino = serial.Serial(connected_port, baudrate)

    # Detect screen size and resolution
    screen_width, screen_height = pyautogui.size()

    # Actual position of the mouse
    mouse_x, mouse_y = mousePos()

    # Set movement sensitivity level
    movement_sensitivity = (10 / sensitivity)

    #Entering the endless loop
    while True:

        #Read the last value of the serial port from arduino
        value = arduino.readline()

        #Transform the byte values to the string
        newValue = value.decode('utf-8')
        #remove the last characters '\n\r'
        newValue = newValue[:-2]

        #Split the value that comes from serialport ','
        coordinate = newValue.split(',')

        #The X and Y coordinate of the sensor
        #If you do want to pass a string representation of a float to an int, you can convert to a float first, then to an integer
        sensor_x = int(2 * float(coordinate[0]) / sensitivity)
        sensor_y = int(2 * float(coordinate[1]) / sensitivity)

        # Move mouse by calculated sensor values
        mouse_x += sensor_x
        mouse_y += sensor_y
        # Set boundries for mouse position on screen

        if (mouse_x > screen_width):
            mouse_x = screen_width
        elif (mouse_x < 0):
            mouse_x = 0

        if (mouse_y > screen_height):
            mouse_y = screen_height
        elif (mouse_y < 0):
            mouse_y = 0


        # Set mouse position to new calculated position
        moveMouse(mouse_x, mouse_y)

        #Click function
        currentValue = int(coordinate[2])
        if currentValue > pressedValue and mouseDown == False:
            mouseDown = True
            pyautogui.mouseDown()

        elif currentValue < unPressedValue and mouseDown == True:
            mouseDown = False
            pyautogui.mouseUp()
