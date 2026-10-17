"""Explicit one-time download of Google's hand landmark model, never webcam data."""
from pathlib import Path
from urllib.request import urlopen
from config import load_config

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"


def main():
    target = Path(load_config()["tracking"]["model_path"])
    if target.is_file():
        print(f"Model already exists: {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".download")
    try:
        with urlopen(MODEL_URL, timeout=60) as response:
            temporary.write_bytes(response.read())
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Downloaded model: {target}")


if __name__ == "__main__":
    main()
