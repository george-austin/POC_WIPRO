from os import listdir, path
from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator

model_folder = 'train3'
img_folder = 'datasets/test/images'
model = YOLO('runs/detect/train17/weights/best.pt')
#model = YOLO('yolov8n.pt')

for img_path in listdir(img_folder):

    frame = cv2.imread(path.join(img_folder, img_path))
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model.predict(img, verbose=False)

    for r in results:
        annotator = Annotator(frame)

        boxes = r.boxes
        for box in boxes:
            # get box coordinates in (top, left, bottom, right) format
            b = box.xyxy[0]
            c = box.cls
            annotator.box_label(b, model.names[int(c)])

            with open('out.txt', 'a') as f:
                f.write(f'{img_path}|{b}|{model.names[int(c)]}\n')
                print(f'{img_path}|{model.names[int(c)]}')

    frame = annotator.result()
    cv2.imshow('YOLO V8 Detection', frame)
    cv2.waitKey(0)
