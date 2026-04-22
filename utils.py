"""
Utility Functions for Vehicle Detection System
================================================
This module contains helper functions for the vehicle detection and counting system.
"""

import cv2
import numpy as np
from datetime import datetime


class Colors:
    """Color codes for consistent visualization"""
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    YELLOW = (0, 255, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    CYAN = (255, 255, 0)
    MAGENTA = (255, 0, 255)


def draw_bounding_box(frame, x1, y1, x2, y2, label, color=Colors.GREEN, thickness=2):
    """
    Draw a bounding box with label on the frame
    
    Args:
        frame: Input frame (numpy array)
        x1, y1: Top-left corner coordinates
        x2, y2: Bottom-right corner coordinates
        label: Text label to display
        color: Box color (BGR tuple)
        thickness: Line thickness
    
    Returns:
        Modified frame with bounding box
    """
    # Draw rectangle
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
    
    # Calculate label size and position
    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    label_w, label_h = label_size
    
    # Draw label background
    cv2.rectangle(frame, 
                  (int(x1), int(y1) - label_h - 10), 
                  (int(x1) + label_w, int(y1)), 
                  color, -1)
    
    # Put label text
    cv2.putText(frame, label, (int(x1), int(y1) - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, Colors.WHITE, 2)
    
    return frame


def draw_counting_line(frame, line_position, color=Colors.RED, thickness=3):
    """
    Draw a virtual counting line on the frame
    
    Args:
        frame: Input frame
        line_position: Y-coordinate for horizontal line or X-coordinate for vertical line
        color: Line color
        thickness: Line thickness
    
    Returns:
        Modified frame with counting line
    """
    height, width = frame.shape[:2]
    
    # Draw horizontal counting line
    cv2.line(frame, (0, line_position), (width, line_position), color, thickness)
    
    # Add label
    cv2.putText(frame, "COUNTING LINE", (width // 2 - 100, line_position - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    
    return frame


def display_info_panel(frame, vehicle_counts, fps=0):
    """
    Display an information panel with vehicle counts
    
    Args:
        frame: Input frame
        vehicle_counts: Dictionary with vehicle types and counts
        fps: Frames per second
    
    Returns:
        Modified frame with info panel
    """
    height, width = frame.shape[:2]
    
    # Create semi-transparent overlay
    overlay = frame.copy()
    panel_height = 200
    cv2.rectangle(overlay, (10, 10), (350, panel_height), Colors.BLACK, -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Display title
    y_offset = 40
    cv2.putText(frame, "VEHICLE DETECTION SYSTEM", (20, y_offset), 
                cv2.FONT_HERSHEY_DUPLEX, 0.7, Colors.CYAN, 2)
    
    y_offset += 35
    cv2.line(frame, (20, y_offset), (340, y_offset), Colors.CYAN, 2)
    
    # Display vehicle counts
    y_offset += 30
    for vehicle_type, count in vehicle_counts.items():
        cv2.putText(frame, f"{vehicle_type.capitalize()}: {count}", 
                    (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, Colors.GREEN, 2)
        y_offset += 25
    
    # Display total
    total = sum(vehicle_counts.values())
    y_offset += 5
    cv2.putText(frame, f"TOTAL: {total}", (20, y_offset), 
                cv2.FONT_HERSHEY_DUPLEX, 0.7, Colors.YELLOW, 2)
    
    # Display FPS
    cv2.putText(frame, f"FPS: {fps:.1f}", (width - 150, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, Colors.WHITE, 2)
    
    return frame


def get_center_point(bbox):
    """
    Calculate the center point of a bounding box
    
    Args:
        bbox: Tuple (x1, y1, x2, y2)
    
    Returns:
        Tuple (cx, cy) - center coordinates
    """
    x1, y1, x2, y2 = bbox
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)
    return cx, cy


def calculate_iou(box1, box2):
    """
    Calculate Intersection over Union (IoU) between two bounding boxes
    
    Args:
        box1: Tuple (x1, y1, x2, y2)
        box2: Tuple (x1, y1, x2, y2)
    
    Returns:
        IoU value (0 to 1)
    """
    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2
    
    # Calculate intersection area
    x_left = max(x1_1, x1_2)
    y_top = max(y1_1, y1_2)
    x_right = min(x2_1, x2_2)
    y_bottom = min(y2_1, y2_2)
    
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    
    # Calculate union area
    box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
    box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
    union_area = box1_area + box2_area - intersection_area
    
    iou = intersection_area / union_area if union_area > 0 else 0
    return iou


def get_timestamp():
    """
    Get current timestamp in a readable format
    
    Returns:
        String timestamp
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def resize_frame(frame, width=None, height=None):
    """
    Resize frame while maintaining aspect ratio
    
    Args:
        frame: Input frame
        width: Target width (optional)
        height: Target height (optional)
    
    Returns:
        Resized frame
    """
    if width is None and height is None:
        return frame
    
    h, w = frame.shape[:2]
    
    if width is not None:
        aspect = width / w
        new_height = int(h * aspect)
        return cv2.resize(frame, (width, new_height), interpolation=cv2.INTER_AREA)
    else:
        aspect = height / h
        new_width = int(w * aspect)
        return cv2.resize(frame, (new_width, height), interpolation=cv2.INTER_AREA)


def is_point_below_line(point, line_y, offset=10):
    """
    Check if a point is below the counting line
    
    Args:
        point: Tuple (x, y)
        line_y: Y-coordinate of the line
        offset: Tolerance offset
    
    Returns:
        Boolean
    """
    return point[1] > (line_y + offset)


def is_point_above_line(point, line_y, offset=10):
    """
    Check if a point is above the counting line
    
    Args:
        point: Tuple (x, y)
        line_y: Y-coordinate of the line
        offset: Tolerance offset
    
    Returns:
        Boolean
    """
    return point[1] < (line_y - offset)


# Vehicle class mapping for COCO dataset (used by YOLO)
VEHICLE_CLASSES = {
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck'
}


def get_vehicle_type(class_id):
    """
    Get vehicle type from class ID
    
    Args:
        class_id: COCO dataset class ID
    
    Returns:
        Vehicle type string or None
    """
    return VEHICLE_CLASSES.get(class_id, None)


def is_vehicle_class(class_id):
    """
    Check if the detected class is a vehicle
    
    Args:
        class_id: COCO dataset class ID
    
    Returns:
        Boolean
    """
    return class_id in VEHICLE_CLASSES
