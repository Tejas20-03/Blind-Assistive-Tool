import cv2
from threading import Thread, Lock

class Stream:
    def __init__(self, src=0):
        # Initialize the video camera stream and read the first frame from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        # Initialize the variable used to indicate if the thread should be stopped
        self.stopped = False
        self.lock = Lock()

    def start(self):
        # Start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep looping infinitely until the thread is stopped
        while True:
            # If the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # Otherwise, read the next frame from the stream
            grabbed, frame = self.stream.read()
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        # Return the frame most recently read
        with self.lock:
            return self.frame

    def stop(self):
        # Indicate that the thread should be stopped and release the stream resource
        self.stopped = True
        self.stream.release()
