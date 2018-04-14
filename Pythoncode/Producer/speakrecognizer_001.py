import speech_recognition as sr


output = "no input"

def recognizer():
    global output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print ('Say something')
        audio = r.listen(source)
    try:
        #print ('I think you said:\n' + r.recognize_google(audio))

        output = str(r.recognize_google(audio))
        print output
    except:
        print "could not convert audio to text"

if __name__ == '__main__':
    recognizer()



