import os.path
from os import listdir

dirs = ['../datasets/train/labels']

for dir in dirs:
    for label_file in listdir(dir):

        if not label_file.endswith('.txt'):
            continue

        print(label_file)

        label_file_path = os.path.join(dir, label_file)

        nls = []

        with open(label_file_path, 'r') as f:

            for l in f.readlines():
                coords = l.split()[1:]

                # Separating x and y coordinates
                x_coords = [float(x) for x in coords[0::2]]
                y_coords = [float(x) for x in coords[1::2]]

                # Finding the center of the polygon
                center_x = sum(x_coords) / len(x_coords)
                center_y = sum(y_coords) / len(y_coords)
                center = (center_x, center_y)

                # Scale factor (for example, 2 to double the size)
                scale_factor = 0.7

                # Scaling each point
                scaled_coords = []
                for x, y in zip(x_coords, y_coords):
                    new_x = (x - center_x) * scale_factor + center_x
                    new_y = (y - center_y) * scale_factor + center_y
                    scaled_coords.extend([new_x, new_y])

                nls.append("1 " + ' '.join([str(x) for x in scaled_coords]))

        with open(label_file_path, 'w') as f:

            for l in nls:
                f.write(l + '\n')
                print(l + '\n')


