import pyttsx3
import speech_recognition as sr
from subprocess import call
import sys
import os

# Text-to-speech engine setup
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
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

    speak('This Smart Glasses contains features like navigation, object detection and avoidance, remote monitoring, currency detection and other numerous features')
    speak('You can access these features by saying the following commands:')
    speak('say navigate to start autonomous movement')
    speak('say remote monitoring to start remote monitoring')

    speak('or you can say hello to interact with Glasses')

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
            
        elif 'read text' in query:
            speak('Text Reader Activated')
            imagetotext()
            
        elif "hello" in query:
            from GreetMe import greetMe
            greetMe()
    
            while True:
                query = takeCommand()
                if "go to sleep" in query:
                    speak("Ok sir! You can call me anytime")
                    break
                elif "hello" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine" in query:
                    speak("That's great sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("You are welcome, sir")
                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)
