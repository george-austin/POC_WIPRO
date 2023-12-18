import os
from os import listdir, remove

script_directory = os.path.dirname(os.path.abspath(__file__))

train_path = os.path.normpath(os.path.join(script_directory, '..', 'datasets', 'train'))
valid_path = os.path.normpath(os.path.join(script_directory, '..', 'datasets', 'valid'))

train_imgs   = [x.replace('.png', '') for x in listdir(os.path.join(train_path, 'images')) if x.endswith('png')]
train_labels = [x.replace('.txt', '') for x in listdir(os.path.join(train_path, 'labels')) if x.endswith('txt')]
valid_imgs   = [x.replace('.png', '') for x in listdir(os.path.join(valid_path, 'images')) if x.endswith('png')]
valid_labels = [x.replace('.txt', '') for x in listdir(os.path.join(valid_path, 'labels')) if x.endswith('txt')]


for x in [x for x in train_labels  if x not in train_imgs ]:
    remove('../datasets/train/labels/' + x + '.txt')

#for x in [x for x in valid_labels  if x not in valid_imgs ]:
#    remove('../datasets/valid/labels' + x + '.txt')