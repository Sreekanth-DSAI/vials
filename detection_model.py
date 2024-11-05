"""
Explanation of the Code:

1. Set up a connection to the PostgreSQL database using SQLAlchemy.
2. Define a SQLAlchemy ORM class `DetectionData` representing the detection data table in the database.
3. Load YOLO models for vial and PFS detection with specific configurations.
4. Implement `predict_and_draw` function to perform object detection and draw bounding boxes on the image.
5. Implement `insert_data` to insert detected data into the PostgreSQL database.
6. Implement `concatenate_images` to combine the original and processed images side by side.
"""

import torch
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from ultralytics import YOLO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

# Database setup: Connect to PostgreSQL database using SQLAlchemy.
DATABASE_URL = "postgresql://dbmasteruser:<lmFpK}PF4u$je+][w=:h4~_!Zz%It]J@ls-8a62cbf5a61df28a063d1a9329e3104b75eefab3.chvkci9uhgu1.ap-south-1.rds.amazonaws.com/Vials"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Create a session for database operations
Base = declarative_base()  # Base class for ORM models

# ORM class representing the detection data table in the database.
class DetectionData(Base):
    __tablename__ = "detection_data2"  # Table name
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    image_name = Column(String(100), index=True)  # Image file name
    model_name = Column(String(100), index=True)  # Model used for detection (Vials or PFS)
    pfs_count = Column(Integer, default=0)  # Number of detected PFS
    vial_count = Column(Integer, default=0)  # Number of detected vials
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp when detection was done

# Create the table in the database if it doesn't already exist.
Base.metadata.create_all(bind=engine)

def get_db():
    """
    Creates and returns a new session for database operations.
    This session is used to interact with the database.
    """
    return SessionLocal()

def insert_data(db, image_name, model_name, pfs_count, vial_count, timestamp):
    """
    Inserts a new record into the detection_data2 table.
    
    Args:
        db: Database session object.
        image_name: Name of the image file.
        model_name: Name of the model used (either "Vials" or "PFS").
        pfs_count: Count of detected PFS.
        vial_count: Count of detected VIALs.
        timestamp: Detection timestamp.
    """
    # Truncate the image name to 30 characters to avoid exceeding column limit
    truncated_image_name = image_name[:30]  
    # Create a new instance of the DetectionData class with the provided details
    db_data = DetectionData(
        image_name=truncated_image_name,
        model_name=model_name,
        pfs_count=pfs_count,
        vial_count=vial_count,
        timestamp=timestamp
    )
    # Add the data to the session and commit it to the database
    db.add(db_data)
    db.commit()

# Load YOLO models for detecting vials and PFS (pre-filled syringes) with specified parameters.
models = {
    "Vials": {
        "model": YOLO("yolov8l(vials)_3k_80.pt"),  # Model file for vials detection
        "conf_threshold": 0.65,  # Confidence threshold for detection
        "iou_threshold": 0.45,  # IoU threshold for filtering overlapping boxes
        "classes": {0: "VIAL"}  # Class dictionary: 0 maps to "VIAL"
    },
    "PFS": {
        "model": YOLO("yolov8l(pfs)_1k_80.pt"),  # Model file for PFS detection
        "conf_threshold": 0.70,  # Confidence threshold for detection
        "iou_threshold": 0.45,  # IoU threshold for filtering overlapping boxes
        "classes": {0: "PFS"}  # Class dictionary: 0 maps to "PFS"
    }
}

def predict_and_draw(image, model_info):
    """
    Performs object detection on the input image using the specified YOLO model and draws bounding boxes.
    
    Args:
        image: Input image (PIL image).
        model_info: Dictionary containing model, confidence threshold, IoU threshold, and class mappings.
    
    Returns:
        img_draw: Image with bounding boxes drawn.
        class_counts: Dictionary containing the count of detected "PFS" and "VIAL".
        timestamp: Timestamp of the detection.
    """
    # Convert the PIL image to OpenCV format (BGR)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # Perform prediction using YOLO model
    results = model_info['model'].predict(
        source=image, 
        conf=model_info['conf_threshold'], 
        iou=model_info['iou_threshold'], 
        verbose=False, 
        max_det=1000, 
        save=False
    )
    
    # Check if no results were detected or if boxes data is empty
    if not results or not results[0].boxes.data.size(0):
        # If no detection, return the original image with an empty count and current timestamp
        return Image.fromarray(np.array(image)), {}, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract labels and coordinates of bounding boxes
    labels, coords = results[0].boxes.data[:, -1], results[0].boxes.data[:, :-1]
    # Convert the image back to PIL format for drawing
    img_draw = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_draw)

    # Initialize class count dictionary
    class_counts = {"PFS": 0, "VIAL": 0}
    
    # Iterate over the detected labels and bounding box coordinates
    for label, coord in sorted(zip(labels, coords), key=lambda x: (x[1][0], x[1][1])):
        # Extract bounding box coordinates and confidence score
        x1, y1, x2, y2, conf = map(int, coord.tolist())
        # Map the label to a class name (PFS or VIAL)
        class_name = model_info['classes'].get(int(label.item()), "Unknown")
        
        # Set the color of the bounding box and dot based on the class
        if class_name == "PFS":
            bbox_color = 'black'  # PFS bounding box color
            dot_color = 'white'  # PFS dot color
        elif class_name == "VIAL":
            bbox_color = 'white'  # VIAL bounding box color
            dot_color = 'black'  # VIAL dot color

        # Draw a rectangle (bounding box) on the image
        draw.rectangle(((x1, y1), (x2, y2)), outline=bbox_color)
        # Draw a small dot at the top-left corner of the bounding box
        draw.ellipse((x1, y1, x1 + 5, y1 + 5), fill=dot_color)

        # Increment the count for the detected class
        if class_name in class_counts:
            class_counts[class_name] += 1

    # Return the processed image, class counts, and detection timestamp
    return img_draw, class_counts, datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def concatenate_images(image1, image2):
    """
    Concatenates two images side by side into a single image.
    
    Args:
        image1: First image (PIL image).
        image2: Second image (PIL image).
    
    Returns:
        concatenated_image: Image with both input images placed side by side.
    """
    # Calculate the total width and maximum height for the combined image
    total_width = image1.width + image2.width
    max_height = max(image1.height, image2.height)
    # Create a new blank image with the calculated dimensions
    concatenated_image = Image.new('RGB', (total_width, max_height))
    # Paste the first and second images side by side
    concatenated_image.paste(image1, (0, 0))
    concatenated_image.paste(image2, (image1.width, 0))
    return concatenated_image  # Return the concatenated image
