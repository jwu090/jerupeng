# Technica 2026: Webcam Computer Controller

## Purpose

Build an accessibility-focused desktop controller that lets users operate a computer using hand gestures captured by a regular webcam, without touching a mouse or keyboard during normal use. This is hand-based control and requires a visible hand with sufficient movement for the chosen gestures.

## Stack and runtime

- Python 3.12 in a project virtual environment is the recommended development baseline.
- `opencv-python` for webcam capture and preview.
- `mediapipe` for hand landmarks and tracking.
- `pyautogui` for computer actions.
- Run processing locally. A regular webcam is the only required input hardware; no depth camera, wearable, or specialized sensor is required.
- Verify dependency installation on the target OS before pinning versions. Do not assume Python 3.14 compatibility from a broad minimum-version statement.

## Functional requirements

1. Detect swipe left, swipe right, open palm, pinch, point, and thumbs up. Distinguish temporal gestures such as swipes from static poses using timestamped landmarks.
2. Support left/right arrow keys, click, directional scroll, media play/pause, and continuous mouse movement through an action adapter.
3. Store user-editable gesture-to-action bindings in `config.json`. Support disabling bindings and validate action names and parameters before enabling control.
4. Store all detection thresholds, confidence levels, sensitivity, smoothing, hold durations, repeat intervals, and cooldowns in config. Users must be able to tune them without editing Python source.
5. Provide a pause gesture and a configurable global emergency-stop hotkey that works when the preview is unfocused. Emergency stop must bypass gesture recognition and action cooldowns, immediately disable dispatch, clear pending actions, and require explicit reactivation. PyAutoGUI key emission alone is not a global hotkey listener; choose and document an OS listener implementation during development.
6. Clearly display the detected gesture, ACTIVE / PAUSED / STOPPED state, tracking status, and configuration or camera errors. Keep status readable with text as well as color.
7. Start paused. While paused, continue recognition and feedback but dispatch no computer actions except an explicit resume transition. Stop dispatch on tracking loss or camera failure; require deliberate reactivation after a failure.
8. Release any held inputs and camera resources on pause, emergency stop, error, or normal exit. Keep PyAutoGUI's built-in fail-safe enabled as an additional safeguard.

## Initial bindings

These are editable starting defaults, not fixed behavior:

| Gesture | Action |
| --- | --- |
| Swipe left | Left arrow |
| Swipe right | Right arrow |
| Open palm held | Toggle pause/resume |
| Pinch | Click once per pinch/release cycle |
| Point | Move mouse; configurable alternative: directional scroll |
| Thumbs up | Media play/pause |

All action types, including scroll direction and amount, must be available through config even if they are not enabled in the default bindings. A held pause pose must trigger once and require release before toggling again. Safety gestures take priority over normal bindings. Continuous movement uses configurable smoothing and sensitivity; discrete actions use per-action cooldowns and release/rearm rules to prevent repeats.

## Configuration contract

`config.json` contains camera selection and preview settings, gesture bindings, recognition thresholds, movement and scroll sensitivity, smoothing, global and per-action cooldowns, pause hold/rearm timing, tracking-loss timeout, and emergency-stop hotkey. Define units explicitly, using seconds for durations and normalized landmark distances where practical. Reject invalid ranges, unknown actions, conflicting safety bindings, or unusable hotkeys with actionable feedback. Invalid configuration must leave control disabled. Apply edits through an explicit reload or restart and document that behavior; saving edits must preserve them across launches.

## Planned structure

```text
camera.py     # Webcam lifecycle and frame acquisition
hands.py      # MediaPipe initialization and normalized landmark output
gestures.py   # Gesture classification, history, confidence, and rearming
actions.py    # Validated action dispatch, cooldowns, and injectable OS adapter
config.json   # User bindings and all tunable thresholds
ui/           # Preview, readable status, and user controls
main.py       # Configuration loading, lifecycle, safety state, orchestration
```

Keep configuration validation and global hotkey handling in focused helpers as needed. Recognition produces gesture events; it must not call PyAutoGUI. A central state gate controls every action path, including continuous mouse movement and scroll.

## Acceptance criteria

- A regular webcam supplies frames and the preview shows hand-tracking and gesture feedback.
- Each supported gesture is recognized in a deliberate manual demo; thresholds can be adjusted for the user's range of motion.
- Editing a binding in config changes its action after the documented reload/restart, and the setting survives relaunch.
- Sensitivity and cooldown changes measurably alter movement or repeat behavior without code edits.
- Paused, stopped, invalid-config, and tracking-failure states suppress normal actions. Holding a pose does not cause unintended repeated toggles or clicks.
- The global emergency hotkey disables dispatch while another app has focus, and no queued action executes afterward.
- Automated tests use synthetic landmarks, a fake clock, and fake action/hotkey adapters. They never move the real pointer or emit real key presses. Real-device checks are manual and explicitly initiated.

## Out of scope

Accounts, databases, cloud services, mobile apps, and specialized input hardware. No webcam recording or upload is required.
