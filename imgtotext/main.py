import cv2
import pyttsx3
import speech_recognition as sr
import pytesseract

# Text-to-speech engine setup
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 180)

def capture_image():
    # Open the webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        # Save the captured image
        img_path = 'captured_image.jpg'
        cv2.imwrite(img_path, frame)
    cap.release()
    cv2.destroyAllWindows()
    return img_path

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

def read_text_from_image(img_path):
    # Read the image
    img = cv2.imread(img_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Perform morphological operations to enhance text regions
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilate = cv2.dilate(thresh, kernel, iterations=1)

    # Extract text using Tesseract OCR
    text = pytesseract.image_to_string(dilate)

    return text

if __name__ == "__main__":
    speak('Welcome to Beyond Vision')
    speak('Guided by Innovation, Driven by Independence')
    
    while True:
        query = take_command().lower()

        if 'read content' in query:
            img_path = capture_image()
            speak('Image captured, analyzing...')
            text = read_text_from_image(img_path)
            speak('The text in the document is:')
            speak(text)
        elif 'exit' in query:
            speak('Exiting program')
            break

    speak("Program exited successfully")
