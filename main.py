"""Manual entry point for the preview-only milestone."""
import argparse
import sys
import time
import cv2
from camera import Camera
from config import ROOT, load_config
from hands import HandTracker
from ui.preview import render, should_quit


def main():
    parser = argparse.ArgumentParser(description="Paused webcam hand-tracking preview; no computer control.")
    parser.add_argument("--config", type=str, default=str(ROOT / "config.json"))
    args = parser.parse_args()
    try:
        settings = load_config(args.config)
        with HandTracker(settings["tracking"]) as tracker, Camera(settings["camera"]) as camera:
            while True:
                frame = camera.read()
                result = tracker.detect(frame, time.monotonic_ns() // 1_000_000)
                render(frame, result)
                if should_quit():
                    break
    except (OSError, ValueError, RuntimeError, cv2.error) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
