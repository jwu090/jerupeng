"""Webcam lifecycle; importing this module never opens a device."""
import cv2


class Camera:
    def __init__(self, settings):
        self.settings = settings
        self.capture = None

    def __enter__(self):
        self.capture = cv2.VideoCapture(self.settings["index"])
        if not self.capture.isOpened():
            self.capture.release()
            raise RuntimeError("Cannot open webcam. Check camera.index and Windows camera permissions.")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.settings["width"])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.settings["height"])
        return self

    def read(self):
        ok, frame = self.capture.read()
        if not ok or frame is None:
            raise RuntimeError("Webcam stopped delivering frames. Close other camera apps and restart.")
        return cv2.flip(frame, 1) if self.settings["mirror"] else frame

    def __exit__(self, *_):
        if self.capture is not None:
            self.capture.release()
