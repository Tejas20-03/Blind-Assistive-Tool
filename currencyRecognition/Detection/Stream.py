import cv2
from threading import Thread, Lock
from Detection.config import *

class Stream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.stream.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.lock = Lock()
        
        self.fps = 0
        self.frame_count = 0
        self.start_time = cv2.getTickCount()

    def start(self):
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            grabbed, frame = self.stream.read()
            
            self.frame_count += 1
            if self.frame_count % 30 == 0:
                current_time = cv2.getTickCount()
                self.fps = 30 * cv2.getTickFrequency() / (current_time - self.start_time)
                self.start_time = current_time

            with self.lock:
                self.grabbed = grabbed
                if grabbed:
                    self.frame = frame

    def read(self):
        with self.lock:
            return self.frame

    def get_fps(self):
        return self.fps

    def stop(self):
        self.stopped = True
        if self.stream.isOpened():
            self.stream.release()

    def is_stopped(self):
        return self.stopped

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
