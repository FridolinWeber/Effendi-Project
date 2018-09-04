# File name: speakrecognizer_001.py
# Author: Fridolin Weber, Saad Nasir
# Date created: 16.04.2018
# Date last modified: 01.05.2018
# Python Version: 2.7
# Requires PyAudio

import speech_recognition as sr


output = "no input"

def recognizer():
    global output
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print ('Say something')
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        output = str(r.recognize_google(audio))
        print output
    except:
        print "could not convert audio to text"
# call main
if __name__ == '__main__':
    recognizer()
