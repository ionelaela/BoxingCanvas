"""Boxing Canvas — generative artwork engine.

Each recorded movement contributes a directional stroke and particles.
Punch category controls the palette, while the movement score influences
stroke length, thickness, particle count, and spread.
Dependencies: OpenCV, NumPy, math, random, and os.
"""

import cv2
import math
import os
import random
import numpy as np

ART_WIDTH = 1200
ART_HEIGHT = 800


def generate_artwork(punch_history, session_folder):
    canvas = 18 * np.ones(
        (ART_HEIGHT, ART_WIDTH, 3),
        dtype="uint8",
    )

    center_x = ART_WIDTH // 2
    center_y = ART_HEIGHT // 2

    random.seed(len(punch_history) * 137)
    previous_point = None

    for punch in punch_history:
        angle = punch["angle"]
        speed = punch["speed"]
        punch_type = punch["type"]

        intensity = max(0.2, min(speed / 180.0, 1.0))
        length = int(80 + intensity * 320)
        variation = random.uniform(-25, 25)
        radians = math.radians(angle + variation)

        x1, y1 = center_x, center_y
        x2 = int(center_x + math.cos(radians) * length)
        y2 = int(center_y - math.sin(radians) * length)

        if punch_type == "HOOK":
            color = (255, 120, 40)
        elif punch_type == "UPPERCUT":
            color = (80, 180, 255)
        elif punch_type == "JAB / CROSS":
            color = (220, 220, 220)
        else:
            color = (150, 150, 150)

        thickness = max(2, min(int(2 + speed / 18), 12))

        # Draw the movement trajectory.
        cv2.line(
            canvas,
            (x1, y1),
            (x2, y2),
            color,
            thickness,
            cv2.LINE_AA,
        )

        # Scatter particles along the trajectory.
        particle_count = int(8 + intensity * 35)

        for _ in range(particle_count):
            t = random.uniform(0.05, 1.0)
            px = int(x1 + (x2 - x1) * t)
            py = int(y1 + (y2 - y1) * t)

            spread = int(10 + intensity * 70)
            px += random.randint(-spread, spread)
            py += random.randint(-spread, spread)

            radius = random.randint(1, max(2, int(2 + intensity * 6)))

            cv2.circle(
                canvas,
                (px, py),
                radius,
                color,
                -1,
                cv2.LINE_AA,
            )

        # Connect consecutive movement endpoints.
        if previous_point is not None:
            cv2.line(
                canvas,
                previous_point,
                (x2, y2),
                (65, 65, 65),
                1,
                cv2.LINE_AA,
            )

        previous_point = (x2, y2)

    # Add the central visual anchor.
    cv2.circle(
        canvas,
        (center_x, center_y),
        18,
        (245, 245, 245),
        -1,
        cv2.LINE_AA,
    )
    cv2.circle(
        canvas,
        (center_x, center_y),
        35,
        (80, 80, 80),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        canvas,
        "BOXING CANVAS",
        (40, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (230, 230, 230),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        canvas,
        f"PUNCHES: {len(punch_history)}",
        (40, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (180, 180, 180),
        2,
        cv2.LINE_AA,
    )

    artwork_path = os.path.join(session_folder, "artwork.png")
    cv2.imwrite(artwork_path, canvas)
    return artwork_path
