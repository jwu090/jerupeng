"""Load and validate preview settings before opening hardware."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_config(path=ROOT / "config.json"):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        camera, tracking = data["camera"], data["tracking"]
        for key in ("index", "width", "height"):
            value = camera[key]
            if type(value) is not int or value < (0 if key == "index" else 1):
                raise ValueError(f"camera.{key} must be a valid integer")
        if type(camera["mirror"]) is not bool:
            raise ValueError("camera.mirror must be true or false")
        if type(tracking["num_hands"]) is not int or tracking["num_hands"] < 1:
            raise ValueError("tracking.num_hands must be a positive integer")
        for key in ("min_hand_detection_confidence", "min_hand_presence_confidence", "min_tracking_confidence"):
            value = tracking[key]
            if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"tracking.{key} must be between 0 and 1")
        model = tracking["model_path"]
        if not isinstance(model, str) or not model.strip():
            raise ValueError("tracking.model_path must be a nonempty path")
        tracking["model_path"] = str((ROOT / model).resolve())
        return data
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid preview configuration: {exc}") from exc
