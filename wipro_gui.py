import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw

class ImageApp:
    output_folder = 'result'

    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")

        self.image_index = 0
        self.image_paths = []
        self.current_image = None

        self.canvas = tk.Canvas(root, width=800, height=500)
        self.canvas.pack()

        self.prev_button = tk.Button(root, text="Previous Image", command=self.prev_image)
        self.prev_button.pack()
        self.next_button = tk.Button(root, text="Next Image", command=self.next_image)
        self.next_button.pack()
        self.fp_button = tk.Button(root, text="False Positive", command=self.false_positive)
        self.fp_button.pack()
        self.tp_button = tk.Button(root, text="True Positive", command=self.true_positive)
        self.tp_button.pack()

        self.root.bind("<KeyPress-f>", self.false_positive)
        self.root.bind("<KeyPress-t>", self.true_positive)

        # Load images from the 'result' directory at startup
        self.load_images_from_directory()

    def load_images_from_directory(self):
        self.image_paths = [os.path.join(self.output_folder, filename) for filename in os.listdir(self.output_folder) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        self.show_current_image()

    def show_current_image(self):
        if self.image_paths:
            image_path = self.image_paths[self.image_index]
            image = Image.open(image_path)
            image.thumbnail((800, 500))

            # Create an ImageDraw object to draw on the image
            draw = ImageDraw.Draw(image)

            # Draw a red square at (100, 100) with a size of 100x100 pixels TODO: take output for image as input, include coordinates from there
            square_size = 100
            draw.rectangle([100, 100, 100 + square_size, 100 + square_size], outline="red", width=3)

            image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image
            self.current_image = image

    def prev_image(self):
        if self.image_paths:
            self.image_index = (self.image_index - 1) % len(self.image_paths)
            self.show_current_image()

    def next_image(self):
        if self.image_paths:
            self.image_index = (self.image_index + 1) % len(self.image_paths)
            self.show_current_image()

    def false_positive(self):
        # TODO: isolate detected region, move file into training directory and mark it as "background" or sth, then generate text file to train then go to next image
        return
    def true_positive(self):
        # TODO: isolate detected region, move file into training directory then generate text file to train then go to next image
        return

    def save_text_file(self, event):
        if self.current_image:
            image_path = self.image_paths[self.image_index]
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            txt_filename = os.path.join(self.output_folder, base_name + ".txt")
            with open(txt_filename, "w") as file:
                file.write("Text related to " + base_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
