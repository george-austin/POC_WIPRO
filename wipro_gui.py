import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")

        self.image_index = 0
        self.image_paths = []
        self.current_image = None

        self.load_button = tk.Button(root, text="Load Images", command=self.load_images)
        self.load_button.pack()

        self.canvas = tk.Canvas(root, width=800, height=500)
        self.canvas.pack()

        self.prev_button = tk.Button(root, text="Previous Image", command=self.prev_image)
        self.prev_button.pack()
        self.next_button = tk.Button(root, text="Next Image", command=self.next_image)
        self.next_button.pack()

        self.root.bind("<KeyPress-f>", self.save_text_file)

    def load_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        self.image_index = 0
        self.show_current_image()

    def show_current_image(self):
        if self.image_paths:
            image_path = self.image_paths[self.image_index]
            image = Image.open(image_path)
            image.thumbnail((800, 500))
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

    def save_text_file(self, event):
        if self.current_image:
            image_path = self.image_paths[self.image_index]
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            txt_filename = base_name + ".txt"
            with open(txt_filename, "w") as file:
                file.write("Text related to " + base_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
