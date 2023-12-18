import os.path
from os import listdir

script_directory = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.normpath(os.path.join(script_directory, '..', 'datasets', 'train', 'labels'))
valid_path = os.path.normpath(os.path.join(script_directory, '..', 'datasets', 'valid', 'labels'))

dirs = [dataset_path, valid_path]

for dir in dirs:
    for label_file in listdir(dir):

        if not label_file.endswith('.txt'):
            continue

        print(label_file)

        label_file_path = os.path.join(dir, label_file)

        with open(label_file_path, 'r') as f:
            nls = []

            for l in f.readlines():
                nl = "0" + l[1:]
                nls.append(nl)

        with open(label_file_path, 'w') as f:
            f.writelines(nls)


