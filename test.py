from os import listdir, path, makedirs
import shutil
from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator

img_folder = 'datasets/test/images'
model = YOLO('runs/detect/own_labels_model/weights/best.pt')
#model = YOLO('yolov8n.pt')

output_folder = 'result'

# Create the output directory if it doesn't exist
makedirs(output_folder, exist_ok=True)

for img_path in listdir(img_folder):

    frame = cv2.imread(path.join(img_folder, img_path))
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model.predict(img, verbose=False)

    for r in results:
        annotator = Annotator(frame)

        boxes = r.boxes

        if len(boxes) > 0:
            output_path = path.join(output_folder, img_path)
            shutil.copy(path.join(img_folder, img_path), output_path)

        for box in boxes:
            # get box coordinates in (top, left, bottom, right) format
            b = box.xyxy[0]
            c = box.cls
            annotator.box_label(b, model.names[int(c)])

            txt_filename = path.join(output_folder, f'{path.splitext(img_path)[0]}.txt')
            with open(txt_filename, 'a') as f:
                f.write(f'{b}|{model.names[int(c)]}\n')
                print(f'{img_path}|{model.names[int(c)]}')

    frame = annotator.result()
    cv2.imshow('YOLO V8 Detection', frame)
    cv2.waitKey(0)
