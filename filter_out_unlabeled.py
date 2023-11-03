from os import listdir, remove


train_imgs   = [x.replace('.png', '') for x in listdir('datasets/train/images')]
train_labels = [x.replace('.txt', '') for x in listdir('datasets/train/labels')]
valid_imgs   = [x.replace('.png', '') for x in listdir('datasets/valid/images')]
valid_labels = [x.replace('.txt', '') for x in listdir('datasets/valid/labels')]


print([x for x in train_imgs  if x in valid_imgs ])

