import math
import os
import time
import pickle
import pyttsx3
import cv2
from imutils.video import FPS
from Detection.config import *
from Detection.Stream import Stream

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

class Detector:
    def __init__(self):
        self.cache = None
        self.featureExtractor = cv2.ORB_create()
        self.featureExtractorSupport = cv2.xfeatures2d.BEBLID_create(0.80)
        self.videoCapture = None
        self.frame = None
        self.maxMatchingsData = None
        self.maxMatchings = 0
        self.detectedCurrency = None
        self.maxMatching = None
        self.kp = None
        self.des = None
        self.matchesSummary = {}
        
        index_params = dict(algorithm=6,
                          table_number=6,
                          key_size=12,
                          multi_probe_level=1)
        search_params = dict(checks=50)
        self.matcher = cv2.FlannBasedMatcher(index_params, search_params)
        
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

    def __serialize_keypoints(self, keypoints):
        return [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in keypoints]

    def __deserialize_keypoints(self, keypoints_data):
        return [cv2.KeyPoint(x=data[0][0], y=data[0][1], size=data[1], angle=data[2],
                            response=data[3], octave=data[4], class_id=data[5]) for data in keypoints_data]

    def start(self):
        if os.path.exists(CACHE_FILE):
            speak('Loading cached currency features')
            with open(CACHE_FILE, 'rb') as f:
                cached_data = pickle.load(f)
                self.cache = {}
                for currency, samples in cached_data.items():
                    self.cache[currency] = []
                    for sample in samples:
                        keypoints_data = sample[1][0]
                        keypoints = self.__deserialize_keypoints(keypoints_data)
                        self.cache[currency].append([sample[0], (keypoints, sample[1][1])])
        else:
            speak('Currency Detection Started Sampling')
            self.getSampleData()
            cache_data = {}
            for currency, samples in self.cache.items():
                cache_data[currency] = []
                for sample in samples:
                    keypoints_data = self.__serialize_keypoints(sample[1][0])
                    cache_data[currency].append([sample[0], (keypoints_data, sample[1][1])])
            with open(CACHE_FILE, 'wb') as f:
                pickle.dump(cache_data, f)
            speak('Currency Detection Done Sampling')
            
        self.videoCapture = Stream(src=0).start()
        self.fps = FPS().start()
        time.sleep(2)  # Allow camera to initialize

    def getSampleData(self):
        self.cache = {}
        for currencyValue in os.listdir(BASE_DIR):
            data = []
            for currencySampleImageName in os.listdir(BASE_DIR + os.sep + currencyValue):
                currencyTrainImagePath = BASE_DIR + os.sep + currencyValue + os.sep + currencySampleImageName
                currencyTrainImage = cv2.imread(currencyTrainImagePath, cv2.IMREAD_GRAYSCALE)
                self.__getFeatures(currencyTrainImage)
                data.append([currencyTrainImage, (self.kp, self.des)])
            self.cache[currencyValue] = data

    def __getFeatures(self, image):
        self.image = image
        keypoints = self.featureExtractor.detect(self.image, None)
        self.kp, self.des = self.featureExtractor.compute(self.image, keypoints)

    def __filterFalsePositives(self, foundMatchings):
        if not foundMatchings:
            return []
        good = []
        try:
            for m, n in foundMatchings:
                if m.distance < 0.7 * n.distance:
                    good.append(m)
        except ValueError:
            pass
        return good

    def __getMatchingPoints(self, queryImageDes, trainImageDes):
        if queryImageDes is None or len(queryImageDes) == 0 or trainImageDes is None or len(trainImageDes) == 0:
            return []
        try:
            return self.__filterFalsePositives(self.matcher.knnMatch(queryImageDes, trainImageDes, k=2))
        except cv2.error:
            return []

    def __buildHomographyInputData(self):
        if not (self.maxMatchingsData is None):
            queryImageData = self.maxMatchingsData[1]
            self.queryImageKeypoints = queryImageData[1][0]
            self.matches = self.maxMatchingsData[0]
            self.queryImageShape = queryImageData[0].shape

    def __guessCurrency(self):
        try:
            self.maxMatchingsCurrency = 0
            self.maxMatchings = 0
            self.detectedCurrency = 0
            self.maxMatching = 0

            self.__getFeatures(self.frame)

            for currencyValue, images in self.cache.items():
                totalMatches = 0
                for imageData in images:
                    matches = self.__getMatchingPoints(imageData[1][1], self.des)
                    countMatches = len(matches)

                    if countMatches > self.maxMatchings:
                        self.maxMatchings = countMatches
                        self.maxMatchingsCurrency = currencyValue
                        self.maxMatchingsData = (matches, imageData)

                    totalMatches += countMatches
                    self.matchesSummary[currencyValue] = totalMatches

            self.__buildHomographyInputData()
            if not (self.maxMatchingsCurrency is None) and self.maxMatchings > MIN_MATCH_COUNT:
                self.detectedCurrency = self.maxMatchingsCurrency
                self.maxMatching = self.maxMatchings
                
        except Exception as error:
            pass

    def detect(self):
        frame = self.videoCapture.read()
        if frame is not None:
            self.frame = frame
            self.color_frame = self.frame.copy()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.__guessCurrency()
            
            if self.detectedCurrency:
                cv2.putText(self.color_frame, f"Currency: {self.detectedCurrency} Rupees", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, TEXT_COLOR, FONT_THICKNESS)
                cv2.putText(self.color_frame, f"Confidence: {self.maxMatching}", 
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, TEXT_COLOR, FONT_THICKNESS)
            
            cv2.imshow(WINDOW_NAME, self.color_frame)
            cv2.waitKey(1)
            self.fps.update()
            return True
        return False

    def stop(self):
        self.fps.stop()
        self.videoCapture.stop()
        cv2.destroyAllWindows()
