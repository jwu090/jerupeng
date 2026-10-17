"""Render landmarks and a permanently paused preview status."""
import cv2

TITLE = "Technica 2026 - Hand tracking preview"
CONNECTIONS = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6),
               (6, 7), (7, 8), (5, 9), (9, 10), (10, 11), (11, 12),
               (9, 13), (13, 14), (14, 15), (15, 16), (13, 17),
               (0, 17), (17, 18), (18, 19), (19, 20)]


def render(frame, result):
    height, width = frame.shape[:2]
    for hand in result.hand_landmarks:
        points = [(max(0, min(width - 1, round(p.x * width))),
                   max(0, min(height - 1, round(p.y * height)))) for p in hand]
        for start, end in CONNECTIONS:
            cv2.line(frame, points[start], points[end], (80, 220, 90), 2)
        for point in points:
            cv2.circle(frame, point, 4, (255, 210, 80), -1)
    status = f"Tracking: {len(result.hand_landmarks)} hand(s)"
    lines = ["PAUSED - preview only; computer control disabled", status,
             "Gesture: not implemented yet", "Q / Esc or close window to quit"]
    cv2.rectangle(frame, (0, 0), (width, 118), (20, 20, 20), -1)
    for index, line in enumerate(lines):
        cv2.putText(frame, line, (12, 25 + index * 27), cv2.FONT_HERSHEY_SIMPLEX,
                    0.55, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow(TITLE, frame)


def should_quit():
    key = cv2.waitKey(1) & 0xFF
    return key in (27, ord("q"), ord("Q")) or cv2.getWindowProperty(TITLE, cv2.WND_PROP_VISIBLE) < 1
