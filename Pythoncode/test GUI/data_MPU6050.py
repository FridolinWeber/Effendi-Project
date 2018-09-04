#!usr/bin/env python

# File name: data_MPU6050.py
# Author: Fridolin Weber, Saad Nasir
# Date created: 16.04.2018
# Date last modified: 01.05.2018
# Python Version: 2.7
# many code parts taken from http://electronut.in/plotting-real-time-data-from-arduino-using-python/

# this code reads the serial input of com7, which is always one value that is read out from one force pressure sensor. The data is saved
# into a txt.file and a live plot takes place
# still unknown error if there is an error in conversion


import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


strPort = 'com10'  #change the com Port to the port of the Device. The current port of the Arduino can be read out in the Arduino IDE
docName = "test"   #default name of document to save

# plot class
class AnalogPlot:
    def __init__(self, strPort, maxLen):
        '''
        deques are data containers that can be rapidly accessed for reading and writing. Those
        containers will temporarily save the values that are read out from the sensors and will be
        plotted onto the y axis. maxLen is the maximum number of values that are stored in the deques.
        The Baud Rate of Serial has to be the same as the Baud rate of the Arduino.
        '''
        self.ser = serial.Serial(strPort, 38400)
        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)
        self.az = deque([0.0] * maxLen)

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
        assert (len(data) == 3)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])
        self.addToBuf(self.az, data[2])

    def writedata(self, data, docName):
        '''function that writes measurement data to a .txt file'''
        t = time.clock()
        string = str(self.cnt) + "," + str(t) + "," + str(data) + "\n"

        docfullname = docName + "." + "txt"
        f = open(docfullname, "a+")
        f.write(string)
        f.close()

        self.cnt += 1

    def update(self, frameNum, a0, a1, a2):
        '''
        the update function is continously called by FuncAnimation. A ."." is written to the SerialPort and the
        Arduino in turn writes the current value that is read out from the MPU6050 to the SerialPort. Those str data
        are converted to floats and later written to a txt.file. "frameNum" in the arguments of the function is needed
        that FunkAnimation knows that update function has to be continously called.
        '''
        global cnt
        try:
            self.ser.write(".") #Python sends a "." to the Arduino which causes the Arduino to write the current position to the Serial Port if this feature ist not used the transfer of data is far too slow
            line = self.ser.readline()
            convertList = (line.split(";"))[0:3]


            try:
                data = [float(val) for val in convertList] # line.split is important if more than 2 values are sent over the serial port by the Arduino
                if len(data) == 3:
                    self.add(data)
                    a0.set_data(range(self.maxLen), self.ax)
                    a1.set_data(range(self.maxLen), self.ay)
                    a2.set_data(range(self.maxLen), self.az)
                print data
                self.writedata(data, docName)

            except:
                print 'error in conversion'


        except KeyboardInterrupt:
            print('exiting')
        return a0,

    def close(self):
        ''' close the Serial Ports when program is ended.'''
        # close serial
        self.ser.flush()
        self.ser.close()


def main():
    ''' plot for the parameters is set up and the Animation starts running'''
    print('reading from serial port %s...' % strPort)
    analogPlot = AnalogPlot(strPort, 100) #instance of the class Analog Plot is created.

    print('plotting data...')

    # set up animation
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 100), ylim=(-180, 180))
    a0, = ax.plot([], [])
    a1, = ax.plot([], [])
    a2, = ax.plot([], [])

    anim = animation.FuncAnimation(fig, analogPlot.update, fargs=(a0, a1, a2), interval=20)

    try:
    #show plot
        plt.show()
    except:
        pass
    analogPlot.close()
    # clean up
    print('exiting.')

# call main
if __name__ == '__main__':
    main()
