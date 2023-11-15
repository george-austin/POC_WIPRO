from enum import Enum


class DetectionRating(Enum):
    FALSE_POSITIVE = 0
    TRUE_POSITIVE = 1
    # values below are not used for now
    FALSE_NEGATIVE = 2
    TRUE_NEGATIVE = 3
