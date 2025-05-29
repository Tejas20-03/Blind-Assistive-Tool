import pyttsx3
import speech_recognition as sr
from subprocess import call
import sys
import os

# Text-to-speech engine setup
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 180)

def autonomous():
    python_executable = sys.executable
    call([python_executable, os.path.join('autonomous', '1.py')])

def remotemonitor():
    python_executable = sys.executable
    call([python_executable, os.path.join('remotemonitor', 'app.py')])
    
def imagetotext():
    python_executable = sys.executable
    call([python_executable, os.path.join('imgtotext', 'main.py')])

def currencyRecognition():
    python_executable = sys.executable
    call([python_executable, os.path.join('currencyRecognition', 'main.py')])
    
def sceneDetection():
    python_executable = sys.executable
    call([python_executable, os.path.join('sceneDetection', 'main.py')])

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 500
        audio = r.listen(source, 0, 4)
    try:
        speak("Understanding...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"You Said: {query}\n")
    except Exception as e:
        speak("Say that again")
        return ""
    return query.lower()

if __name__ == "__main__":
    speak('Welcome to Beyond Vision')
    speak('An Assistive tool for Blind Persons')

    speak('Beyond Vision contains features like navigation, object detection and avoidance, remote monitoring, currency detection and other numerous features')
    speak('You can access these features by saying the following commands:')
    speak('say navigate to start autonomous movement')
    speak('say remote monitoring to start remote monitoring')
    speak('say detect currency to identify the currency')
    speak('say detect surrounding to detect the objects in front of you')


    while True:
        query = takeCommand()

        if 'navigate' in query:
            speak('Autonomous mode activated')
            autonomous()
        elif 'remote monitor' in query:
            speak('Remote monitoring activated')
            remotemonitor()
        elif 'detect currency' in query:
            speak("Currency Detection Activated")
            currencyRecognition()
        
        elif 'detect surrounding' in query:
            speak('Scene Detection activated')
            sceneDetection()
            