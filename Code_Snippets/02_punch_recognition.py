"""Boxing Canvas — directional movement analysis and punch classification.

The classifier is experimental and uses simple horizontal/vertical
movement heuristics; it is not a trained boxing-action recognition model.
"""

import math


def distance(point_a, point_b):
    """Calculate Euclidean distance between two image coordinates."""
    return math.sqrt(
        (point_b[0] - point_a[0]) ** 2
        + (point_b[1] - point_a[1]) ** 2
    )


def angle_degrees(dx, dy):
    """Convert a frame displacement vector into an angle in degrees."""
    angle = math.degrees(math.atan2(-dy, dx))
    if angle < 0:
        angle += 360
    return angle


def classify_punch(dx, dy):
    """Classify a detected movement using its horizontal/vertical direction."""
    horizontal = abs(dx)
    vertical = abs(dy)

    if vertical > horizontal * 1.25 and dy < 0:
        return "UPPERCUT"

    if horizontal > vertical * 1.35:
        return "HOOK"

    if horizontal >= vertical * 0.5:
        return "JAB / CROSS"

    return "UNKNOWN"


# In the application loop, the classifier is called after the movement
# threshold and cooldown checks have passed.
