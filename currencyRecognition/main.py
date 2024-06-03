from Detection.Detector import Detector
import pyttsx3
import datetime
import speech_recognition as sr
from subprocess import call
import sys
import os

# Text-to-speech engine setup
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 200)

def chatbot():
    python_executable = sys.executable  # Get the path to the current Python interpreter
    call([python_executable, os.path.join('..', 'main.py')])

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

# Initialize Detector object
detect_obj = Detector()
detect_obj.start()

try:
    while True:
        query = takeCommand()
        if "detect currency" in query:
            try:
                detect_obj.detect()
                print("[INFO] Detected Currency: {}".format(detect_obj.detectedCurrency))
                print("[INFO] Matching Points: {}".format(detect_obj.maxMatching))
            except KeyboardInterrupt:
                detect_obj.stop()
        elif "exit" in query:
            speak("Exiting program")
            break
finally:
    detect_obj.stop()
    chatbot()

speak("Program exited successfully")
