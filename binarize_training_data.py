import os.path
from os import listdir

dirs = ['datasets/train/labels', 'datasets/valid/labels']

for dir in dirs:
    for label_file in listdir(dir):

        if not label_file.endswith('.txt'):
            continue

        print(label_file)

        label_file_path = os.path.join(dir, label_file)

        with open(label_file_path, 'r') as f:
            nls = []

            for l in f.readlines():
                nl = "1" + l[1:]
                nls.append(nl)

        with open(label_file_path, 'w') as f:
            f.writelines(nls)


