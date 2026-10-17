"""MediaPipe Tasks hand tracking without OS input side effects."""
from pathlib import Path
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:
    def __init__(self, settings):
        model = Path(settings["model_path"])
        if not model.is_file():
            raise FileNotFoundError(f"Missing model: {model}. Run python setup_model.py first.")
        self.options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=str(model)),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=settings["num_hands"],
            min_hand_detection_confidence=settings["min_hand_detection_confidence"],
            min_hand_presence_confidence=settings["min_hand_presence_confidence"],
            min_tracking_confidence=settings["min_tracking_confidence"],
        )
        self.last_timestamp = -1
        self.detector = None

    def __enter__(self):
        self.detector = vision.HandLandmarker.create_from_options(self.options)
        return self

    def detect(self, frame, timestamp_ms):
        timestamp_ms = max(timestamp_ms, self.last_timestamp + 1)
        self.last_timestamp = timestamp_ms
        image = mp.Image(image_format=mp.ImageFormat.SRGB,
                         data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return self.detector.detect_for_video(image, timestamp_ms)

    def __exit__(self, *_):
        if self.detector is not None:
            self.detector.close()
