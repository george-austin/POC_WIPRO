from PIL import Image
import os

from detection_rating import DetectionRating


class DetectedDamage:
    TRAINING_IMAGES_PATH = "datasets/train/images"
    TRAINING_LABELS_PATH = "datasets/train/labels"

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
        original_image = Image.open(self.image_path)

        # Calculate the bounding box coordinates with a 10px margin
        margin = 10
        left = int(self.x1 * original_image.width) - margin
        upper = int(self.y1 * original_image.height) - margin
        right = int(self.x2 * original_image.width) + margin
        lower = int(self.y2 * original_image.height) + margin

        # Crop the bounding box region
        cropped_image = original_image.crop((left, upper, right, lower))

        # Save the cropped image with a new filename
        base_path, ext = os.path.splitext(os.path.basename(self.image_path))
        new_filename = os.path.join(self.TRAINING_IMAGES_PATH, f"{base_path}_{self.number}.png")
        cropped_image.save(new_filename)

        # Save the detection information
        detection_info = f"{detection_rating.value} {self.x1} {self.y1} {self.x2} {self.y2}"
        label_filename = os.path.join(self.TRAINING_LABELS_PATH, f"{base_path}_{self.number}.txt")
        with open(label_filename, 'a') as label_file:
            # only write coords to file if it is TP, create training label file in any case.
            if detection_rating == DetectionRating.TRUE_POSITIVE:
                label_file.write(detection_info)
