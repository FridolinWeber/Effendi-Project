#!usr/bin/env python
# many code parts taken from http://electronut.in/plotting-real-time-data-from-arduino-using-python/

# this code reads the serial input of com7, which is always one value that is read out from one force pressure sensor. The data is safed
# into a file and a live plot takes place

#  still unknown error if there is an error in conversion

import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation


strPort = 'com10'
cnt = 0



# plot class
class AnalogPlot:
    # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(strPort, 9600)

        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)
        self.az = deque([0.0] * maxLen)
        self.maxLen = maxLen

    # add to buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)

        else:
            buf.pop()
            buf.appendleft(val) #ax list is updated with the current value from the readout

    # add data
    def add(self, data):
        assert (len(data) == 3)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])
        self.addToBuf(self.az, data[2])


    # update plot
    def update(self, frameNum, a0, a1, a2):
        global cnt

        try:
            line = self.ser.readline()
            #print line
            #y = line.split(";")
            #print(y.decode('utf-8'))

            convertList = (line.split(";"))[0:3]

            try:
                data = [float(val) for val in convertList] # line.split is important if more than 2 values are sent over the serial port by the Arduino
                #print data
                if len(data) == 3:
                    self.add(data)
                    a0.set_data(range(self.maxLen), self.ax)
                    a1.set_data(range(self.maxLen), self.ay)
                    a2.set_data(range(self.maxLen), self.az)

                    string = str(cnt) + "," + str(data) + "\n"

                    f = open("test.txt", "a+")
                    f.write(string)
                    f.close()
                    cnt += 1
            except:
                print 'error in conversion'


        except KeyboardInterrupt:
            print('exiting')

        return a0,


    # clean up
    def close(self):
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
    ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))
    a0, = ax.plot([], [])
    a1, = ax.plot([], [])
    a2, = ax.plot([], [])
    print "hello"
    anim = animation.FuncAnimation(fig, analogPlot.update, fargs=(a0, a1, a2), interval=20)

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
