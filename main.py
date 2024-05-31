import pyttsx3
import speech_recognition
from subprocess import call

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

rate = engine.setProperty("rate",170)

def autonomous():
    call(['python','autonomous/1.py'])

def remotemonitor():
    call(['python','remotemonitor/app.py'])

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
#
def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 500
        audio = r.listen(source,0,4)
    try:
        print("Understanding..")
        query = r.recognize_google(audio, language="en-IN")
        print(f"You Said:{query}\n")
    except Exception as e:
        print("Say that again")
        return ""
    return query

if __name__ == "__main__":
    speak('Welcome to Autonomous Wheelchair')
    speak('Guided by Innovation, Driven by Independence')

    speak('This Wheelchair contains autonomous navigation, object detection and avoidance, remote monitoring, fall detection and other numerous features')
    speak('You can access these features by saying the following commands:')
    speak('say navigate to start autonomous movement')
    speak('say remote monitoring to start remote monitoring')

    speak('or you can say hello to interact with wheelchair')

    while True:
        query = takeCommand().lower(),

        if 'navigate' in query:
            speak('Autonomous mode activated')
            autonomous()
        elif 'remote monitor' in query:
            speak('Remote monitoring activated')
            remotemonitor()
        elif "hello" in query:
            from GreetMe import greetMe
            greetMe()
    
            while True:
                query = takeCommand().lower()
                if "go to sleep" in query :
                    speak("Ok sir! You can call me anytime")
                    break
                elif "hello" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine" in query:
                    speak("that's great sir")
                elif "remote monitor" in query:
                    speak('remote monitoring activated')
                    remotemonitor()
                    break
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
                elif "google" in query:
                    from SearchNow import searchGoogle
    
                    searchGoogle(query)
                elif "youtube" in query:
                    from SearchNow import searchYoutube
    
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
    
                    searchWikipedia(query)
        

