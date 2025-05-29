import cv2
import pyttsx3
import speech_recognition as sr
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
from subprocess import call
import sys
import os

# Text-to-speech engine setup
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 180)

# Load the pre-trained VGG16 model
model = VGG16(weights='imagenet')

def chatbot():
    python_executable = sys.executable  # Get the path to the current Python interpreter
    call([python_executable, os.path.join('..', 'main.py')])


def capture_image():
    # Open the webcam
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    ret, frame = cap.read()
    if ret:
        # Save the captured image
        img_path = 'captured_image.jpg'
        cv2.imwrite(img_path, frame)
    cap.release()
    cv2.destroyAllWindows()
    return img_path

def describe_image(img_path):
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    # Predict the scene
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    
    # Create a description from the predictions
    description = ", ".join([f"{desc} with a probability of {prob:.2f}" for _, desc, prob in decoded_predictions])
    return description

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
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
    speak('Say capture to detect the surrounding')
    
    try:
        while True:
            query = take_command().lower()

            if 'capture' in query:
                img_path = capture_image()
                speak('Image captured, analyzing...')
                description = describe_image(img_path)
                speak(f'The image is described as: {description}')
            elif 'exit' in query:
                speak('Exiting program')
                break

    finally:
        chatbot()
