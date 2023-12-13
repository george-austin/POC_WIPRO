import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import subprocess

from detected_damage import DetectedDamage
from detection_rating import DetectionRating


class ImageApp:
    OUTPUT_FOLDER = 'result'
    training_script_path = 'train.py'
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 500
    no_images_left_placeholder = "resources/no-images-placeholder.png"

    def __init__(self, root):
        self.draw = None
        self.root = root
        self.root.title("Auswertung Erkennung Buchschäden")
        self.root.geometry(f"{self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT + 110}")

        self.image_index = 0
        self.image_paths = []
        self.current_image = None
        self.detected_damage_queue = []

        self.canvas = tk.Canvas(root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack()

        self.filename_label = tk.Label(root, text="", fg="gray", font=("Arial", 10))
        self.filename_label.pack()

        self.prev_button = tk.Button(root, text="Previous Image", command=self.prev_image)
        self.prev_button.pack(side="left")
        self.next_button = tk.Button(root, text="Next Image", command=self.next_image)
        self.next_button.pack(side="right")
        self.fp_button = tk.Button(root, text="False Positive",
                                   command=lambda: self.rate_detection(DetectionRating.FALSE_POSITIVE))
        self.fp_button.pack()
        self.tp_button = tk.Button(root, text="True Positive",
                                   command=lambda: self.rate_detection(DetectionRating.TRUE_POSITIVE))
        self.tp_button.pack()
        self.trigger_training_button = tk.Button(root, text="Retrain Model", command=self.start_training)
        self.trigger_training_button.pack()

        self.root.bind("<KeyPress-f>", lambda e: self.rate_detection(DetectionRating.FALSE_POSITIVE))
        self.root.bind("<KeyPress-t>", lambda e: self.rate_detection(DetectionRating.TRUE_POSITIVE))
        self.root.bind("<Left>", lambda e: self.prev_image())
        self.root.bind("<Right>", lambda e: self.next_image())

        # Load images from the 'result' directory at startup
        self.load_images_from_directory()

    def load_images_from_directory(self):
        self.image_paths = [os.path.join(self.OUTPUT_FOLDER, filename) for filename in os.listdir(self.OUTPUT_FOLDER) if
                            filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        self.show_current_image()

    def show_current_image(self):
        if self.image_paths:
            image_path = self.image_paths[self.image_index]
            image = Image.open(image_path)
            width, height = image.size
            image.thumbnail((self.CANVAS_WIDTH, self.CANVAS_HEIGHT))

            # Create an ImageDraw object to draw on the image
            self.draw = ImageDraw.Draw(image)
            self.filename_label.config(text=os.path.basename(image_path))

            if not self.detected_damage_queue:
                self.detected_damage_queue = self.get_detected_damage(image_path, width, height)

            self.draw_damage_info(self.draw, self.detected_damage_queue)

            image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image
            self.current_image = image
        else:
            self.show_placeholder()

    def show_placeholder(self):
        placeholder = Image.open(self.no_images_left_placeholder)
        placeholder.thumbnail((self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        ph = ImageTk.PhotoImage(placeholder)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=ph)
        self.canvas.image = placeholder
        self.current_image = placeholder

    def get_detected_damage(self, image_path, width, height):
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        txt_filename = os.path.join(self.OUTPUT_FOLDER, base_name + ".txt")
        file1 = open(txt_filename, 'r')
        lines = file1.readlines()
        queue = []
        for idLine, line in enumerate(lines):
            queue.append(DetectedDamage(line.strip(), image_path, idLine, width, height))
        return queue

    def draw_damage_info(self, draw, detected_damage_queue):
        for detected_damage in detected_damage_queue:
            draw.rectangle([detected_damage.x1 * self.CANVAS_WIDTH, detected_damage.y1 * self.CANVAS_HEIGHT,
                            detected_damage.x2 * self.CANVAS_WIDTH, detected_damage.y2 * self.CANVAS_HEIGHT],
                           outline="red",
                           width=1)
            if len(detected_damage_queue) > 1:
                font = ImageFont.load_default()
                text = str(detected_damage.number+1) + "."
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_position = (detected_damage.x1 * self.CANVAS_WIDTH - 15,
                                 detected_damage.y1 * self.CANVAS_HEIGHT - 15)
                backdrop_coords = [
                    text_position[0],
                    text_position[1],
                    text_position[0] + text_bbox[2] + 2,
                    text_position[1] + text_bbox[3] + 2
                ]
                draw.rectangle(backdrop_coords, fill="white")
                draw.text(text_position, text, font=font, size=14, fill="red")

    def prev_image(self):
        self.detected_damage_queue = []
        if self.image_paths:
            self.image_index = (self.image_index - 1) % len(self.image_paths)
            self.show_current_image()

    def next_image(self):
        self.detected_damage_queue = []
        if self.image_paths:
            self.image_index = (self.image_index + 1) % len(self.image_paths)
            self.show_current_image()

    def rate_detection(self, detection_rating):
        if self.image_paths:
            detected_damage = self.detected_damage_queue.pop(0)
            detected_damage.save_new_training_data(detection_rating)

            if not self.detected_damage_queue:
                # move image to training in case all detected damage instances were rated.
                detected_damage.save_original_image()
                self.remove_label()
                self.next_image()
            else:
                # reload image with removed bounding box. other detected damage instances are still visible.
                self.show_current_image()

    def remove_label(self):
        image_index = self.image_index % len(self.image_paths)
        image_path = self.image_paths[image_index]
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        txt_filename = os.path.join(self.OUTPUT_FOLDER, base_name + ".txt")
        os.remove(txt_filename)
        self.image_paths.pop(image_index)

        if not self.image_paths:
            self.show_placeholder()

    def remove_image_and_label(self):
        image_index = self.image_index % len(self.image_paths)
        image_path = self.image_paths[image_index]
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        txt_filename = os.path.join(self.OUTPUT_FOLDER, base_name + ".txt")
        os.remove(image_path)
        os.remove(txt_filename)
        self.image_paths.pop(image_index)

        if not self.image_paths:
            self.show_placeholder()

    def start_training(self):
        try:
            # Use subprocess to start the script in a new console
            subprocess.Popen(['start', 'cmd', '/k', 'python', self.training_script_path], shell=True)
            print(f"Started {self.training_script_path} in an independent external console.")
        except Exception as e:
            print(f"Error starting external console: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
