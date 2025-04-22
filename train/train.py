from ultralytics import YOLO

model = YOLO("yolov8s.pt")
model.train(data="train.yaml", epochs=5)