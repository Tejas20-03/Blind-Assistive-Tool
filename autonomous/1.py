import numpy as np
import cv2
import pyttsx3 


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

testmode = 1  

def make_chunks(EdgeArray, size_of_chunk):
    chunks = []
    for i in range(0, len(EdgeArray), size_of_chunk):
        chunks.append(EdgeArray[i:i + size_of_chunk])
    return chunks

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    StepSize = 5
    last_command = ""  

    while True:
        _, frame = cap.read()
        if frame is None:
            break
        
        original_frame = frame.copy()
        img_edgerep = frame.copy()
        img_contour = frame.copy()
        img_navigation = frame.copy()

        blur = cv2.bilateralFilter(img_edgerep, 9, 40, 40)
        edges = cv2.Canny(blur, 50, 150)

        img_edgerep_h = img_edgerep.shape[0] - 1
        img_edgerep_w = img_edgerep.shape[1] - 1

        EdgeArray = []

        for j in range(0, img_edgerep_w, StepSize):
            pixel = (j, 0)
            for i in range(img_edgerep_h - 5, 0, -1):
                if edges.item(i, j) == 255:
                    pixel = (j, i)
                    break
            EdgeArray.append(pixel)

        for x in range(len(EdgeArray) - 1):
            cv2.line(img_edgerep, EdgeArray[x], EdgeArray[x + 1], (0, 255, 0), 1)

        for x in range(len(EdgeArray)):
            cv2.line(img_edgerep, (x * StepSize, img_edgerep_h), EdgeArray[x], (0, 255, 0), 1)

        blurred_frame = cv2.bilateralFilter(img_contour, 9, 75, 75)
        gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img_edgerep, contours, -1, (0, 0, 255), 3)

        number_of_chunks = 3
        size_of_chunk = int(len(EdgeArray) / number_of_chunks)
        chunks = make_chunks(EdgeArray, size_of_chunk)
        avg_of_chunk = []

        for i in range(len(chunks) - 1):
            x_vals = []
            y_vals = []
            for (x, y) in chunks[i]:
                x_vals.append(x)
                y_vals.append(y)
            avg_x = int(np.average(x_vals))
            avg_y = int(np.average(y_vals))
            avg_of_chunk.append([avg_y, avg_x])
            cv2.line(frame, (int(img_edgerep_w / 2), img_edgerep_h), (avg_x, avg_y), (255, 0, 0), 2)

        forwardEdge = avg_of_chunk[1]
        cv2.line(frame, (int(img_edgerep_w / 2), img_edgerep_h), (forwardEdge[1], forwardEdge[0]), (0, 255, 0), 3)

        if forwardEdge[0] > 250:
            farthest_point = min(avg_of_chunk)
            if farthest_point[1] < 310:
                direction = "Move left"
            else:
                direction = "Move right"
        else:
            direction = "Move forward"

        if direction != last_command:
            speak(direction)
            last_command = direction 

        if testmode == 1:
            cv2.imshow("Original_Frame", original_frame)
            cv2.imshow("Edge_separation", img_edgerep)
            font = cv2.FONT_HERSHEY_SIMPLEX
            navigation = cv2.putText(frame, direction, (275, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Navigation", navigation)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
