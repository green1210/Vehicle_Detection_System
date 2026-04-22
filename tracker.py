"""
Vehicle Tracker Module
======================
This module implements vehicle tracking across frames using centroid tracking algorithm.
It assigns unique IDs to vehicles and tracks their movement.
"""

import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict
import utils


class VehicleTracker:
    """
    Vehicle Tracker using centroid tracking algorithm
    
    This class tracks vehicles across frames by matching centroids
    and maintaining unique IDs for each vehicle.
    """
    
    def __init__(self, max_disappeared=30, max_distance=50):
        """
        Initialize the tracker
        
        Args:
            max_disappeared: Maximum frames a vehicle can disappear before deregistration
            max_distance: Maximum distance between centroids to consider as same vehicle
        """
        # Counter for next available object ID
        self.next_object_id = 0
        
        # Dictionary to store object ID -> centroid mapping
        self.objects = OrderedDict()
        
        # Dictionary to store object ID -> vehicle type mapping
        self.object_types = OrderedDict()
        
        # Dictionary to store object ID -> bounding box mapping
        self.object_bboxes = OrderedDict()
        
        # Dictionary to track how many frames each object has disappeared
        self.disappeared = OrderedDict()
        
        # Maximum frames before deregistering
        self.max_disappeared = max_disappeared
        
        # Maximum distance for centroid matching
        self.max_distance = max_distance
    
    def register(self, centroid, vehicle_type, bbox):
        """
        Register a new vehicle with a unique ID
        
        Args:
            centroid: (x, y) coordinates of the vehicle center
            vehicle_type: Type of vehicle (car, truck, bus, etc.)
            bbox: Bounding box (x1, y1, x2, y2)
        """
        self.objects[self.next_object_id] = centroid
        self.object_types[self.next_object_id] = vehicle_type
        self.object_bboxes[self.next_object_id] = bbox
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1
    
    def deregister(self, object_id):
        """
        Remove a vehicle from tracking
        
        Args:
            object_id: ID of the vehicle to remove
        """
        del self.objects[object_id]
        del self.object_types[object_id]
        del self.object_bboxes[object_id]
        del self.disappeared[object_id]
    
    def update(self, detections):
        """
        Update tracker with new detections from current frame
        
        Args:
            detections: List of tuples [(bbox, vehicle_type), ...]
                       where bbox = (x1, y1, x2, y2)
        
        Returns:
            Dictionary of tracked objects {object_id: (centroid, vehicle_type, bbox)}
        """
        # If no detections, mark all existing objects as disappeared
        if len(detections) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                
                # Deregister if disappeared for too long
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            return self.get_tracked_objects()
        
        # Initialize array to store input centroids
        input_centroids = np.zeros((len(detections), 2), dtype="int")
        input_types = []
        input_bboxes = []
        
        # Calculate centroids for all detections
        for i, (bbox, vehicle_type) in enumerate(detections):
            cx, cy = utils.get_center_point(bbox)
            input_centroids[i] = (cx, cy)
            input_types.append(vehicle_type)
            input_bboxes.append(bbox)
        
        # If no objects are being tracked yet, register all detections
        if len(self.objects) == 0:
            for i in range(len(input_centroids)):
                self.register(input_centroids[i], input_types[i], input_bboxes[i])
        
        # Otherwise, match existing objects with new detections
        else:
            # Get current tracked object IDs and centroids
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            # Calculate distance between each pair of existing and new centroids
            distances = dist.cdist(np.array(object_centroids), input_centroids)
            
            # Find the minimum distance for each existing object
            rows = distances.min(axis=1).argsort()
            
            # Find the column (input centroid) with minimum distance for each row
            cols = distances.argmin(axis=1)[rows]
            
            # Track which rows and columns we've already examined
            used_rows = set()
            used_cols = set()
            
            # Loop over the combination of (row, col) index tuples
            for (row, col) in zip(rows, cols):
                # Ignore if already examined
                if row in used_rows or col in used_cols:
                    continue
                
                # Check if distance is within threshold
                if distances[row, col] > self.max_distance:
                    continue
                
                # Update the object with new centroid
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.object_types[object_id] = input_types[col]
                self.object_bboxes[object_id] = input_bboxes[col]
                self.disappeared[object_id] = 0
                
                # Mark as examined
                used_rows.add(row)
                used_cols.add(col)
            
            # Calculate which rows and cols we have NOT examined yet
            unused_rows = set(range(0, distances.shape[0])).difference(used_rows)
            unused_cols = set(range(0, distances.shape[1])).difference(used_cols)
            
            # Handle disappeared objects
            if distances.shape[0] >= distances.shape[1]:
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1
                    
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            
            # Register new objects
            else:
                for col in unused_cols:
                    self.register(input_centroids[col], input_types[col], input_bboxes[col])
        
        return self.get_tracked_objects()
    
    def get_tracked_objects(self):
        """
        Get all currently tracked objects
        
        Returns:
            Dictionary {object_id: (centroid, vehicle_type, bbox)}
        """
        tracked = {}
        for object_id in self.objects.keys():
            tracked[object_id] = (
                self.objects[object_id],
                self.object_types[object_id],
                self.object_bboxes[object_id]
            )
        return tracked
    
    def get_object_count(self):
        """
        Get the total number of tracked objects
        
        Returns:
            Integer count
        """
        return len(self.objects)
    
    def get_count_by_type(self):
        """
        Get count of vehicles by type
        
        Returns:
            Dictionary {vehicle_type: count}
        """
        counts = {}
        for vehicle_type in self.object_types.values():
            counts[vehicle_type] = counts.get(vehicle_type, 0) + 1
        return counts
    
    def reset(self):
        """
        Reset the tracker (clear all tracked objects)
        """
        self.next_object_id = 0
        self.objects = OrderedDict()
        self.object_types = OrderedDict()
        self.object_bboxes = OrderedDict()
        self.disappeared = OrderedDict()


class SimpleCentroidTracker:
    """
    Simplified centroid tracker for basic tracking needs
    """
    
    def __init__(self, max_disappeared=20):
        """
        Initialize simple tracker
        
        Args:
            max_disappeared: Maximum frames before deregistration
        """
        self.next_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared
    
    def update(self, centroids):
        """
        Update with list of centroids
        
        Args:
            centroids: List of (x, y) tuples
        
        Returns:
            Dictionary of tracked objects
        """
        if len(centroids) == 0:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    del self.objects[obj_id]
                    del self.disappeared[obj_id]
            return self.objects
        
        if len(self.objects) == 0:
            for centroid in centroids:
                self.objects[self.next_id] = centroid
                self.disappeared[self.next_id] = 0
                self.next_id += 1
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            distances = dist.cdist(np.array(object_centroids), np.array(centroids))
            rows = distances.min(axis=1).argsort()
            cols = distances.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                obj_id = object_ids[row]
                self.objects[obj_id] = centroids[col]
                self.disappeared[obj_id] = 0
                
                used_rows.add(row)
                used_cols.add(col)
            
            unused_rows = set(range(distances.shape[0])).difference(used_rows)
            unused_cols = set(range(distances.shape[1])).difference(used_cols)
            
            for row in unused_rows:
                obj_id = object_ids[row]
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    del self.objects[obj_id]
                    del self.disappeared[obj_id]
            
            for col in unused_cols:
                self.objects[self.next_id] = centroids[col]
                self.disappeared[self.next_id] = 0
                self.next_id += 1
        
        return self.objects
