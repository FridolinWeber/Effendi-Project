#!usr/bin/env python

# File name: datatracker.py
# Author: Fridolin Weber, Saad Nasir
# Date created: 16.04.2018

# Date last modified: 01.05.2018
# Python Version: 2.7
# many code parts taken from http://electronut.in/plotting-real-time-data-from-arduino-using-python/

# this code reads the serial input of comPort, which is always one value that is read out from one force pressure sensor. The data is saved
# into a file and a live plot takes place


import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#from moviepy.editor import VideoClip
import time


strPort = "com8" #Com port of the Arduino Devices
docName = "test"


class AnalogPlot:

    def __init__(self, strPort, maxLen):
        '''
        deques are data containers that can be rapidly accessed for reading and writing. Those
        containers will temporarily save the values that are read out from the sensors and will be
        plotted onto the y axis. maxLen is the maximum number of values that are stored in the deques.
        The Baud Rate of Serial has to be the same as the Baud rate of the Arduino.
        '''
        # open serial port
        self.ser = serial.Serial(strPort, 38400)

        self.au = deque([0.0] * maxLen)
        self.av = deque([0.0] * maxLen)
        self.aw = deque([0.0] * maxLen)
        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)
        self.az = deque([0.0] * maxLen)
        self.ap = deque([0.0] * maxLen)
        self.at = deque([0.0] * maxLen)
        #self.aq = deque([0.0] * maxLen)
        #self.ar = deque([0.0] * maxLen)

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


        assert(len(data) == 5)
        self.addToBuf(self.au, data[0])
        self.addToBuf(self.av, data[1])
        self.addToBuf(self.aw, data[2])
        self.addToBuf(self.ax, data[3])
        self.addToBuf(self.ay, data[4])
        self.addToBuf(self.az, data[5])
        self.addToBuf(self.ap, data[6])
        self.addToBuf(self.at, data[7])
        #self.addToBuf(self.aq, data[8])
        #self.addToBuf(self.ar, data[9])


    def writedata(self, data, docName):
        '''function that writes measurement data to a .txt file'''
        t = time.clock()
        string = str(self.cnt) + "," + str(t) + "," + str(data) + "\n"

        docfullname = docName + "." + "txt"
        f = open(docfullname, "a+")
        f.write(string)
        f.close()

        self.cnt += 1

    def update(self, frameNum, a0=(), a1=(), a2=(), a3=(), a4=(), a5=(), a6=(), a7=(), a8=(), a9=()):
        '''
        the update function is continously called by FuncAnimation. The str data from the serial port
        are converted to floats and later written to a txt.file. "frameNum" in the arguments of the function is needed
        that FunkAnimation knows that update function has to be continously called.
        '''
        global cnt
        try:
            self.ser.write(".")
            line = self.ser.readline()

            convertList = (line.split(";"))[0:8]
            if convertList[-1] == '\r\n':
                convertList.pop(-1)

            print convertList

            try:
                data = [float(val) for val in convertList]

                self.add(data)
                a0.set_data(range(self.maxLen), self.au)
                a1.set_data(range(self.maxLen), self.av)
                a2.set_data(range(self.maxLen), self.aw)
                a3.set_data(range(self.maxLen), self.ax)
                a4.set_data(range(self.maxLen), self.ay)
                a5.set_data(range(self.maxLen), self.az)
                a6.set_data(range(self.maxLen), self.ap)
                a7.set_data(range(self.maxLen), self.at)
                #a8.set_data(range(self.maxLen), self.aq)
                #a9.set_data(range(self.maxLen), self.ar)

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

    print('reading from serial port %s...' % strPort)

    # plot parameters
    analogPlot = AnalogPlot(strPort, 100)

    print('plotting data...')

    # set up animation
    fig = plt.figure()
    ax  = plt.axes(xlim=(0, 100), ylim=(0, 1023))
    a0, = ax.plot([], [])
    a1, = ax.plot([], [])
    a2, = ax.plot([], [])
    a3, = ax.plot([], [])
    a4, = ax.plot([], [])
    a5, = ax.plot([], [])
    a6, = ax.plot([], [])
    a7, = ax.plot([], [])
    a8, = ax.plot([], [])
    a9, = ax.plot([], [])


    anim = animation.FuncAnimation(fig, analogPlot.update, frames=25, fargs=(a0, a1, a2, a3, a4, a5, a6, a7), interval=10)
    #Writer = animation.writers['ffmpeg']
    #WriterFile = animation.writers['ffmpeg_file']
    #anim.save('osc.mp4', writer=Writer(fps=100), dpi=200)
    try:
    # show plot
        plt.show()
    except:
        pass

    analogPlot.close()

    # clean up
    print('exiting.')

# call main
if __name__ == '__main__':
    main()
