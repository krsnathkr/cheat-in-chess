from ultralytics import YOLO

# Use a YOLOv8 model configuration or pretrained weights
model = YOLO("yolov8n.yaml")  # or "yolov8n.pt" to start from pretrained weights

# Train the model
model.train(data="data.yaml", epochs=50, imgsz=640, batch=16)
