from ultralytics import YOLO
from datetime import datetime


def log(msg):
    print(datetime.now(), f'***** {msg} *****')


log('START')
log('LOADING MODEL')
model = YOLO('yolov8n.pt')
log('MODEL LOADED')

log('START TRAIN')
model.train(data='data.yaml', epochs=300)
log('END TRAIN')
log('END')
