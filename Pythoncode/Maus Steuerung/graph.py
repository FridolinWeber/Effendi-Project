#
# Real-time plot from serial data. 
#
 
import serial
import matplotlib.pyplot as plt

from ctypes import windll, Structure, c_long, byref
import win32gui, win32api, win32con

#Sleep Function
from time import sleep

#Pyautogui is for screen resolution
import pyautogui as pag

#Serial port and system librarys
import sys
import glob
import serial
 
s = serial.Serial('COM10',38400) # check your arduino code baudrate
 
l = 100 # length
x = range(l) # x axis
T = [240 for i in range(l)] # initial temp value
 
plt.ion()
plt.show()
 
while True:
   t = int(s.readline().strip())
   newValue = t.decode('utf-8')
   newValue = newValue[:-2]
   T=T[1:] # pop first value
   T.append( newValue ) # push at the end keeping list of same size
 
   plt.axis([0,l,min(T),max(T)])
   sid = plt.scatter(x,T,linewidth=0)
   plt.draw()
   sid.remove()
