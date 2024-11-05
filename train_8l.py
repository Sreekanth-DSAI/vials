"""
Explanation of the Code:

1. Import the YOLO model class from the ultralytics library.
2. Build a YOLO model from scratch using the 'yolov8l.yaml' configuration file. This file defines the model architecture.
3. Build a YOLO model from pre-trained weights using the 'yolov8l.pt' file. This loads a model already trained on a dataset.
4. Optionally display the model architecture and other details using the model.info() method.
5. Train the YOLO model using the dataset specified in 'data.yaml', for 60 epochs, with an image size of 640 and batch size of 8.
"""

from ultralytics import YOLO  # Import the YOLO class from the ultralytics library

# Build a YOLO model from scratch using a configuration file
model = YOLO("yolov8l.yaml")  
# 'yolov8l.yaml' contains the architecture and parameters for the YOLOv8 large variant model

# Build a YOLO model from pretrained weights
model = YOLO("yolov8l.pt")  
# 'yolov8l.pt' is a pre-trained model that has been trained on a large dataset 
# This model can be further fine-tuned or used for inference directly

# Display model information (optional step for debugging or reviewing the architecture)
model.info()  # This shows model details such as layers, total parameters, etc.

# Train the model on the dataset specified in data.yaml
results = model.train(data="data.yaml", epochs=60, imgsz=640, batch=8)  
# The model will be trained for 60 epochs with an image size of 640x640 pixels and a batch size of 8
