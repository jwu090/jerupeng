# Technica 2026: Webcam Controller

Current milestone: local webcam preview with MediaPipe hand landmarks and a
permanent **PAUSED** status. Gesture classification, action mappings, global
emergency stop, and mouse/keyboard control are planned in `SPEC.md` and are not
implemented yet. This preview never imports PyAutoGUI or emits input.

## Setup (Windows PowerShell, Python 3.12)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup_model.py
.\.venv\Scripts\python.exe main.py
```

The model setup downloads Google's Hand Landmarker model once into `models/`.
The preview then processes frames locally without uploading or recording them.
Model source and API guide:
https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python

Hold a hand in view to see its landmarks. Press Q or Escape with the preview
focused, or close its window, to exit. Control stays paused throughout.

## Settings

Edit `config.json` and restart the preview. Camera index selects a webcam;
width/height are requested pixel dimensions (the device may choose another
supported resolution), and mirror flips the preview horizontally. Tracking
confidence values range from 0 to 1; higher values require stronger confidence.
`num_hands` sets the maximum hand count. `model_path` is relative to the repo
root unless absolute. Future gesture/action thresholds will also live here.

If the camera will not open, check Windows camera privacy permissions, close
other camera apps, or try another camera index. For a missing-model error, run
`setup_model.py`. Errors print `STOPPED` in the terminal and release resources.

## Automated checks

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q camera.py config.py hands.py main.py setup_model.py ui
```

Automated checks must not start the live preview or control real input. Webcam
quality, landmark accuracy, window behavior, and camera-error recovery need
manual verification. See `AGENTS.md` for development rules.
