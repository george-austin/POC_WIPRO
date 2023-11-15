from os import listdir, remove


train_imgs   = [x.replace('.png', '') for x in listdir('datasets/train/images') if x.endswith('png')]
train_labels = [x.replace('.txt', '') for x in listdir('datasets/train/labels') if x.endswith('txt')]
valid_imgs   = [x.replace('.png', '') for x in listdir('datasets/valid/images') if x.endswith('png')]
valid_labels = [x.replace('.txt', '') for x in listdir('datasets/valid/labels') if x.endswith('txt')]


for x in [x for x in train_labels  if x not in train_imgs ]:
    remove('datasets/train/labels/' + x + '.txt')

for x in [x for x in valid_labels  if x not in valid_imgs ]:
    remove('datasets/valid/labels/' + x + '.txt')