from PIL import Image
import os

from detection_rating import DetectionRating


class DetectedDamage:
    TRAINING_IMAGES_PATH = "datasets/train/images"
    TRAINING_LABELS_PATH = "datasets/train/labels"

    # margin so only part of the image is labeled and some of the background is visible for training purposes
    CROP_MARGIN = 10

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

        left, lower, right, upper = self.calculate_bounding_box_coords(original_image)

        # Crop the bounding box region
        cropped_image = original_image.crop((left, upper, right, lower))

        base_path, ext = os.path.splitext(os.path.basename(self.image_path))
        width, height = self.save_cropped_image(cropped_image, base_path)

        self.save_cropped_label_file(base_path, detection_rating, width, height)

    def save_cropped_label_file(self, base_path, detection_rating, width, height):
        detection_info = f"{detection_rating.value} {self.CROP_MARGIN} {self.CROP_MARGIN} {width - self.CROP_MARGIN} {height - self.CROP_MARGIN}"
        label_filename = os.path.join(self.TRAINING_LABELS_PATH, f"{base_path}_{self.number}.txt")
        with open(label_filename, 'a') as label_file:
            # only write coords to file if it is TP, create training label file in any case.
            if detection_rating == DetectionRating.TRUE_POSITIVE:
                label_file.write(detection_info)

    def save_cropped_image(self, cropped_image, base_path):
        new_filename = os.path.join(self.TRAINING_IMAGES_PATH, f"{base_path}_{self.number}.png")
        cropped_image.save(new_filename)
        return cropped_image.size

    def calculate_bounding_box_coords(self, original_image):
        left = int(self.x1 * original_image.width) - self.CROP_MARGIN
        upper = int(self.y1 * original_image.height) - self.CROP_MARGIN
        right = int(self.x2 * original_image.width) + self.CROP_MARGIN
        lower = int(self.y2 * original_image.height) + self.CROP_MARGIN
        return left, lower, right, upper
