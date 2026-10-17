# Agent instructions

## Scope

Follow `SPEC.md` for this local, webcam-based accessibility controller. Use Python, OpenCV, MediaPipe, and PyAutoGUI. Recommend Python 3.12 in a virtual environment and verify dependency compatibility before pinning versions.

## Implementation rules

- Keep modules separate: camera capture in `camera.py`, hand tracking in `hands.py`, recognition in `gestures.py`, OS action dispatch in `actions.py`, feedback in `ui/`, and orchestration in `main.py`.
- Never call PyAutoGUI from camera, tracking, recognition, or UI code. Route every computer action through the central safety state gate and action adapter.
- Put all thresholds and tunable values in `config.json`, including confidence, sensitivity, smoothing, timing, cooldowns, and gesture mappings. Document units and validate ranges; do not hide behavioral thresholds in Python code.
- Make small, focused changes. Avoid unrelated refactors or new services. Keep the specification and configuration documentation aligned with behavior.
- Start paused, preserve the pause gesture and global emergency stop, and retain PyAutoGUI's fail-safe. Errors must disable action dispatch.
- Do not add accounts, databases, cloud services, or mobile apps.

## Testing rules

- Never run actions that control the real mouse or keyboard during automated tests. This includes clicks, scrolls, movement, key presses, hotkeys, and held inputs.
- Inject fake action adapters and mock all OS input calls before executing action code. Imports must not start capture, register global listeners, or dispatch actions.
- Test recognition with synthetic landmarks, cooldowns with a fake clock, and safety transitions with fake camera/hotkey events. Include paused/stopped suppression and release/rearm behavior.
- Do not launch the live controller as an automated smoke test. Real webcam, global hotkey, and input-control checks require an explicitly initiated manual session.
- Report the checks performed and any unverified behavior. Documentation-only edits need review and diff checks, not live input tests.
