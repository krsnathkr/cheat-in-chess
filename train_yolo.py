from ultralytics import YOLO

model = YOLO("yolov8n.yaml")

model.train(data="data.yaml", epochs=50, imgsz=640, batch=16)
