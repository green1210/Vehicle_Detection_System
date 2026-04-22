"""
Vehicle Counter Module
======================
This module implements the vehicle counting logic with CSV data storage.
It tracks vehicles crossing a virtual line and stores the data.
"""

import csv
import os
from datetime import datetime
import pandas as pd
import utils


class VehicleCounter:
    """
    Vehicle Counter class to count vehicles crossing a virtual line
    and store the data in CSV format.
    """
    
    def __init__(self, counting_line_y, csv_file_path='output/vehicle_counts.csv'):
        """
        Initialize the vehicle counter
        
        Args:
            counting_line_y: Y-coordinate of the counting line
            csv_file_path: Path to CSV file for storing data
        """
        self.counting_line_y = counting_line_y
        self.csv_file_path = csv_file_path
        
        # Dictionary to track vehicle counts by type
        self.vehicle_counts = {
            'car': 0,
            'motorcycle': 0,
            'bus': 0,
            'truck': 0
        }
        
        # Set to track which vehicle IDs have been counted
        self.counted_vehicle_ids = set()
        
        # Dictionary to track vehicle positions (for line crossing detection)
        # {vehicle_id: 'above' or 'below'}
        self.vehicle_positions = {}
        
        # List to store detailed records
        self.records = []
        
        # Time tracking for per-minute statistics
        self.start_time = datetime.now()
        self.last_minute_count = 0
        
        # Initialize CSV file
        self._initialize_csv()
    
    def _initialize_csv(self):
        """
        Initialize the CSV file with headers if it doesn't exist
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.csv_file_path), exist_ok=True)
        
        # Check if file exists
        file_exists = os.path.isfile(self.csv_file_path)
        
        if not file_exists:
            with open(self.csv_file_path, 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'vehicle_id', 'vehicle_type', 'total_count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
    
    def update(self, tracked_objects):
        """
        Update counter with tracked objects from current frame
        
        Args:
            tracked_objects: Dictionary from tracker {object_id: (centroid, vehicle_type, bbox)}
        
        Returns:
            Tuple (vehicle_counts, newly_counted_ids)
        """
        newly_counted = []
        
        for object_id, (centroid, vehicle_type, bbox) in tracked_objects.items():
            cx, cy = centroid
            
            # Determine current position relative to counting line
            if cy < self.counting_line_y - 10:
                current_position = 'above'
            elif cy > self.counting_line_y + 10:
                current_position = 'below'
            else:
                continue  # In the threshold zone, skip
            
            # Check if this vehicle has been tracked before
            if object_id in self.vehicle_positions:
                previous_position = self.vehicle_positions[object_id]
                
                # Check if vehicle crossed the line (from above to below)
                if previous_position == 'above' and current_position == 'below':
                    # Check if not already counted
                    if object_id not in self.counted_vehicle_ids:
                        # Count the vehicle
                        self._count_vehicle(object_id, vehicle_type)
                        newly_counted.append(object_id)
            
            # Update vehicle position
            self.vehicle_positions[object_id] = current_position
        
        return self.vehicle_counts, newly_counted
    
    def _count_vehicle(self, vehicle_id, vehicle_type):
        """
        Count a vehicle and record the data
        
        Args:
            vehicle_id: Unique ID of the vehicle
            vehicle_type: Type of vehicle
        """
        # Increment count
        if vehicle_type in self.vehicle_counts:
            self.vehicle_counts[vehicle_type] += 1
        else:
            self.vehicle_counts[vehicle_type] = 1
        
        # Mark as counted
        self.counted_vehicle_ids.add(vehicle_id)
        
        # Get timestamp
        timestamp = utils.get_timestamp()
        
        # Calculate total count
        total_count = sum(self.vehicle_counts.values())
        
        # Create record
        record = {
            'timestamp': timestamp,
            'vehicle_id': vehicle_id,
            'vehicle_type': vehicle_type,
            'total_count': total_count
        }
        
        # Add to records list
        self.records.append(record)
        
        # Write to CSV
        self._write_to_csv(record)
        
        print(f"[COUNTED] ID: {vehicle_id}, Type: {vehicle_type}, Total: {total_count}")
    
    def _write_to_csv(self, record):
        """
        Write a vehicle record to CSV file
        
        Args:
            record: Dictionary containing vehicle data
        """
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'vehicle_id', 'vehicle_type', 'total_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(record)
    
    def get_total_count(self):
        """
        Get total count of all vehicles
        
        Returns:
            Integer total count
        """
        return sum(self.vehicle_counts.values())
    
    def get_counts_by_type(self):
        """
        Get vehicle counts by type
        
        Returns:
            Dictionary {vehicle_type: count}
        """
        return self.vehicle_counts.copy()
    
    def get_vehicle_per_minute(self):
        """
        Calculate vehicles per minute
        
        Returns:
            Float: vehicles per minute
        """
        elapsed_time = (datetime.now() - self.start_time).total_seconds() / 60
        if elapsed_time < 0.1:  # Avoid division by zero
            return 0
        return self.get_total_count() / elapsed_time
    
    def load_data(self):
        """
        Load data from CSV file
        
        Returns:
            Pandas DataFrame
        """
        try:
            df = pd.read_csv(self.csv_file_path)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def get_statistics(self):
        """
        Get comprehensive statistics
        
        Returns:
            Dictionary with various statistics
        """
        total = self.get_total_count()
        counts_by_type = self.get_counts_by_type()
        vpm = self.get_vehicle_per_minute()
        
        stats = {
            'total_vehicles': total,
            'vehicles_by_type': counts_by_type,
            'vehicles_per_minute': round(vpm, 2),
            'unique_vehicles': len(self.counted_vehicle_ids),
            'elapsed_time_minutes': round((datetime.now() - self.start_time).total_seconds() / 60, 2)
        }
        
        return stats
    
    def reset_counts(self):
        """
        Reset all counts (useful for testing or new sessions)
        """
        self.vehicle_counts = {
            'car': 0,
            'motorcycle': 0,
            'bus': 0,
            'truck': 0
        }
        self.counted_vehicle_ids.clear()
        self.vehicle_positions.clear()
        self.records.clear()
        self.start_time = datetime.now()
    
    def export_summary(self, output_file='output/summary.txt'):
        """
        Export a summary report to text file
        
        Args:
            output_file: Path to output text file
        """
        stats = self.get_statistics()
        
        with open(output_file, 'w') as f:
            f.write("=" * 50 + "\n")
            f.write("VEHICLE DETECTION & COUNTING SYSTEM - SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Report Generated: {utils.get_timestamp()}\n\n")
            
            f.write(f"Total Vehicles Counted: {stats['total_vehicles']}\n")
            f.write(f"Unique Vehicles Tracked: {stats['unique_vehicles']}\n")
            f.write(f"Elapsed Time: {stats['elapsed_time_minutes']} minutes\n")
            f.write(f"Average Rate: {stats['vehicles_per_minute']} vehicles/minute\n\n")
            
            f.write("Vehicle Distribution by Type:\n")
            f.write("-" * 30 + "\n")
            for vtype, count in stats['vehicles_by_type'].items():
                percentage = (count / stats['total_vehicles'] * 100) if stats['total_vehicles'] > 0 else 0
                f.write(f"  {vtype.capitalize():12s}: {count:4d} ({percentage:5.1f}%)\n")
            
            f.write("\n" + "=" * 50 + "\n")
        
        print(f"Summary exported to {output_file}")


class LineCounter:
    """
    Simple line-based counter for basic counting needs
    """
    
    def __init__(self, line_y):
        """
        Initialize simple line counter
        
        Args:
            line_y: Y-coordinate of counting line
        """
        self.line_y = line_y
        self.counted_ids = set()
        self.positions = {}
        self.count = 0
    
    def check_and_count(self, object_id, cy):
        """
        Check if vehicle crossed line and count it
        
        Args:
            object_id: Vehicle ID
            cy: Y-coordinate of vehicle center
        
        Returns:
            Boolean: True if newly counted
        """
        if object_id in self.counted_ids:
            return False
        
        # Determine position
        if cy < self.line_y - 10:
            position = 'above'
        elif cy > self.line_y + 10:
            position = 'below'
        else:
            return False
        
        # Check for crossing
        if object_id in self.positions:
            prev_pos = self.positions[object_id]
            if prev_pos == 'above' and position == 'below':
                self.counted_ids.add(object_id)
                self.count += 1
                return True
        
        self.positions[object_id] = position
        return False
