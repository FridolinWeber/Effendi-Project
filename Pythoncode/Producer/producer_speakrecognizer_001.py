import speech_recognition as sr
#import pyaudio

r = sr.Recognizer()

with sr.Microphone() as source:
    print ('Say something')
    audio = r.listen(source)

try:
    print ('I think you said:\n' + r.recognize_google(audio))

except:
    pass
