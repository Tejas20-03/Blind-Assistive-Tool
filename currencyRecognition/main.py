from Detection.Detector import Detector
import pyttsx3
import datetime
import speech_recognition as sr
from subprocess import call
import sys
import os
import cv2
import time
from Detection.config import *

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 200)

def chatbot():
    python_executable = sys.executable  
    call([python_executable, os.path.join('..', 'main.py')])

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 500
        audio = r.listen(source, 0, 4)
    try:
        speak("Understanding...")
        print("Understanding...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"You Said: {query}\n")
    except Exception as e:
        speak("Say that again")
        return ""
    return query.lower()

def main():
    detect_obj = Detector()
    detect_obj.start()
    
    print("\nCurrency Detection System Started")
    print("Commands:")
    print("- 'detect currency': Start currency detection")
    print("- Press 's': Stop current detection")
    print("- 'exit': Exit the program\n")
    
    speak("Currency detection system is ready")
    speak("Say detect currency to detect the currency in front of you")
    
    detection_active = False
    last_detection_time = 0
    detection_cooldown = 3  # seconds between voice announcements
    
    while True:
        if not detection_active:
            query = takeCommand()
            
            if "detect currency" in query:
                detection_active = True
                speak("Starting currency detection")
            elif "exit" in query:
                speak("Exiting currency detection system")
                break
        
        if detection_active:
            if not detect_obj.detect():
                speak("Camera not available")
                detection_active = False
                continue
                
            current_time = time.time()
            if detect_obj.detectedCurrency and (current_time - last_detection_time) > detection_cooldown:
                speak(f"Detected Currency: {detect_obj.detectedCurrency} Rupees")
                last_detection_time = current_time
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                detection_active = False
                speak("Detection stopped")
                cv2.destroyAllWindows()
    
    detect_obj.stop()
    chatbot()

if __name__ == "__main__":
    main()
