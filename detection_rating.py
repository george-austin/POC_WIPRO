from enum import Enum


class DetectionRating(Enum):
    FALSE_POSITIVE = 1
    TRUE_POSITIVE = 2
    # values below are not used for now
    FALSE_NEGATIVE = 3
    TRUE_NEGATIVE = 4
