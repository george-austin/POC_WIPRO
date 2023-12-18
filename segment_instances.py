import os
import cv2

dirs = ['datasets/train/labels', 'datasets/valid/labels']

for dir in dirs:
    for label_file in os.listdir(dir):

        if not label_file.endswith('.txt'):
            continue

        label_file_path = os.path.join(dir, label_file)
        img_file_path = os.path.join(dir.replace('labels', 'images'), label_file.replace('txt', 'png'))
        image = cv2.imread(img_file_path)

        with open(label_file_path, 'r') as f:
            for idx, l in enumerate(f.readlines()):
                print(label_file_path)
                obj_class = l.split()[0]
                print(obj_class)

                if obj_class == "3":
                    print('skipping schmutz')
                    continue

                coords = l.split()[1:]
                x_coords = [float(x) for x in coords[0::2]]
                y_coords = [float(x) for x in coords[1::2]]

                x_min = min(x_coords)
                x_max = max(x_coords)
                y_min = min(y_coords)
                y_max = max(y_coords)
                image_height, image_width, _ = image.shape

                tl = (int(image_width * x_min), int(image_height * y_min))
                br = (int(image_width * x_max), int(image_height * y_max))

                tl_expanded = (int(image_width * x_min * 0.9), int(image_height * y_min * 0.9))
                br_expanded = (int(image_width * x_max * 1.1), int(image_height * y_max * 1.1))

                # Crop and save the expanded area
                cropped_image = image[tl_expanded[1]:br_expanded[1], tl_expanded[0]:br_expanded[0]]
                cropped_img_path = img_file_path.replace('.png', f'_cropped_{idx}.png')
                cv2.imwrite(cropped_img_path, cropped_image)

                # Calculate new coordinates for original rectangle in the cropped image
                new_tl = (tl[0] - tl_expanded[0], tl[1] - tl_expanded[1])
                new_br = (br[0] - tl_expanded[0], br[1] - tl_expanded[1])
                new_image_height, new_image_width, _ = cropped_image.shape

                # Normalize these coordinates for YOLO format
                x_center = (new_tl[0] + new_br[0]) / 2 / new_image_width
                y_center = (new_tl[1] + new_br[1]) / 2 / new_image_height
                width = (new_br[0] - new_tl[0]) / new_image_width
                height = (new_br[1] - new_tl[1]) / new_image_height

                # Save new YOLO label
                new_label_file_path = label_file_path.replace('.txt', f'_cropped_{idx}.txt')
                with open(new_label_file_path, 'w') as new_label_file:
                    new_label_file.write(f'{obj_class} {x_center} {y_center} {width} {height}\n')

        os.remove(img_file_path)
        os.remove(label_file_path)
