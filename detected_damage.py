from detection_rating import DetectionRating


class DetectedDamage:
    def __init__(self, detected_string, image_path, number, width, height):
        # Split the string into coordinates and damage type
        coordinates, damage_type = detected_string.split('|')

        # remove leading tensor([ and trailing ]) from coords
        coordinates = coordinates.replace('tensor([', '').replace('])', '')
        # Extract individual coordinates
        x1, y1, x2, y2 = map(float, coordinates.split(','))

        self.x1, self.x2 = (x1 / width, x2 / width)
        self.y1, self.y2 = (y1 / height, y2 / height)
        self.damage_type = damage_type.strip()
        self.image_path = image_path
        self.number = number

    def save_new_training_data(self, detection_rating):
        damage = detection_rating == DetectionRating.TRUE_POSITIVE
        # TODO:segment bounding box from image with 10px margin and save FP in datasets/train/image_path_base_number.png
        #  with an empty label file of same name save TP with label file in correct format
