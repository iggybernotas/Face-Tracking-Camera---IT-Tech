from abc import ABC, abstractmethod
import cv2


class Feature(ABC):
    CONST_CASCADE_CLASSIFIER = ""
    CONST_SCALE_FACTOR = 1.1
    CONST_MIN_NEIGHBORS = 5 # Higher value results in less detections but with higher quality

    @abstractmethod
    def set_cascade(self):
        pass

    @abstractmethod
    def get_detected(self, gray):
        pass


class Face(Feature):
    CONST_CASCADE_CLASSIFIER = "haarcascade_frontalface_default.xml"
    cascade = ""

    def set_cascade(self):
        self.cascade = cv2.CascadeClassifier(self.CONST_CASCADE_CLASSIFIER)

    def get_detected(self, gray):
        faces = self.cascade.detectMultiScale(
            gray,
            self.CONST_SCALE_FACTOR,
            self.CONST_MIN_NEIGHBORS,
        )
        return faces


class Eye(Feature):
    CONST_CASCADE_CLASSIFIER = "haarcascade_eye.xml"
    cascade = ""

    def set_cascade(self):
        self.cascade = cv2.CascadeClassifier(self.CONST_CASCADE_CLASSIFIER)

    def get_detected(self, gray):
        eyes = self.cascade.detectMultiScale(gray)
        return eyes
