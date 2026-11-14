"""Boxing Canvas — hand tracking and movement measurement.

Selected excerpt from the webcam processing pipeline.
Dependencies: OpenCV and MediaPipe Tasks. The Hand Landmarker model file
must be available at the path supplied to create_hand_landmarker().
"""

import time
import cv2
import mediapipe as mp


def create_hand_landmarker(model_path: str):
    """Create a video-mode detector configured to track up to two hands."""
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=2,
    )
    return mp.tasks.vision.HandLandmarker.create_from_options(options)


def detect_hand_positions(landmarker, frame, timestamp_ms: int):
    """Return the frame and the pixel coordinates of each index fingertip."""
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb,
    )
    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    positions = {}
    for hand_index, hand_landmarks in enumerate(result.hand_landmarks):
        # MediaPipe landmark 8 represents the index fingertip.
        index_tip = hand_landmarks[8]
        x = int(index_tip.x * width)
        y = int(index_tip.y * height)
        positions[hand_index] = (x, y)

        cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

    return frame, positions


def measure_movement(previous_position, current_position):
    """Measure frame-to-frame displacement in image pixels."""
    dx = current_position[0] - previous_position[0]
    dy = current_position[1] - previous_position[1]
    displacement = (dx**2 + dy**2) ** 0.5
    return dx, dy, displacement


# In the main loop, timestamp_ms is derived from elapsed program time:
# timestamp_ms = int((time.time() - program_start) * 1000)
# The returned displacement is a pixel-based movement score, not km/h.
