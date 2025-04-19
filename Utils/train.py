from ultralytics import YOLO

model = YOLO("yolov8s.pt")
model.train(data="../train/train.yaml", epochs=5)