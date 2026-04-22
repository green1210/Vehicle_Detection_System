
import cv2
import numpy as np
from ultralytics import YOLO
import time
import argparse
import sys

# Import custom modules
import utils
from tracker import VehicleTracker
from vehicle_counter import VehicleCounter


class VehicleDetectionSystem:
    """
    Main Vehicle Detection and Counting System
    
    This class orchestrates the entire detection, tracking, and counting pipeline.
    """
    
    def __init__(self, video_source, model_path='yolov8n.pt', confidence=0.3):
        """
        Initialize the vehicle detection system
        
        Args:
            video_source: Path to video file or camera index (0 for webcam)
            model_path: Path to YOLO model weights
            confidence: Confidence threshold for detections
        """
        print("=" * 60)
        print("VEHICLE DETECTION & COUNTING SYSTEM")
        print("=" * 60)
        print(f"\nInitializing system...")
        
        # Load video source
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open video source: {video_source}")
            sys.exit(1)
        
        # Get video properties
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        print(f"Video loaded: {self.frame_width}x{self.frame_height} @ {self.fps} FPS")
        
        # Load YOLO model
        print(f"Loading YOLO model: {model_path}")
        try:
            self.model = YOLO(model_path)
            print("✓ Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Tip: Install ultralytics with: pip install ultralytics")
            sys.exit(1)
        
        self.confidence = confidence
        
        # Initialize tracker
        self.tracker = VehicleTracker(max_disappeared=30, max_distance=80)
        print("✓ Tracker initialized")
        
        # Set counting line at 60% of frame height
        self.counting_line_y = int(self.frame_height * 0.6)
        
        # Initialize counter
        self.counter = VehicleCounter(
            counting_line_y=self.counting_line_y,
            csv_file_path='output/vehicle_counts.csv'
        )
        print("✓ Counter initialized")
        
        # FPS calculation variables
        self.fps_start_time = time.time()
        self.fps_counter = 0
        self.current_fps = 0
        
        # Frame skip for performance (process every Nth frame)
        self.frame_skip = 2
        self.frame_count = 0
        
        print("\n✓ System ready!")
        print("=" * 60)
    
    def detect_vehicles(self, frame):
        """
        Detect vehicles in a frame using YOLO
        
        Args:
            frame: Input frame (numpy array)
        
        Returns:
            List of detections [(bbox, vehicle_type), ...]
        """
        # Run YOLO inference
        results = self.model(frame, conf=self.confidence, verbose=False)
        
        detections = []
        
        # Process results
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Get class ID and check if it's a vehicle
                class_id = int(box.cls[0])
                
                if utils.is_vehicle_class(class_id):
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Get vehicle type
                    vehicle_type = utils.get_vehicle_type(class_id)
                    
                    # Get confidence
                    conf = float(box.conf[0])
                    
                    detections.append(((x1, y1, x2, y2), vehicle_type))
        
        return detections
    
    def process_frame(self, frame):
        """
        Process a single frame through the complete pipeline
        
        Args:
            frame: Input frame
        
        Returns:
            Processed frame with visualizations
        """
        # Detect vehicles
        detections = self.detect_vehicles(frame)
        
        # Update tracker
        tracked_objects = self.tracker.update(detections)
        
        # Update counter
        vehicle_counts, newly_counted = self.counter.update(tracked_objects)
        
        # Draw visualizations
        frame = self._draw_visualizations(frame, tracked_objects, vehicle_counts, newly_counted)
        
        return frame
    
    def _draw_visualizations(self, frame, tracked_objects, vehicle_counts, newly_counted):
        """
        Draw all visualizations on the frame
        
        Args:
            frame: Input frame
            tracked_objects: Dictionary of tracked objects
            vehicle_counts: Dictionary of vehicle counts
            newly_counted: List of newly counted vehicle IDs
        
        Returns:
            Frame with visualizations
        """
        # Draw counting line
        frame = utils.draw_counting_line(frame, self.counting_line_y)
        
        # Draw tracked vehicles
        for object_id, (centroid, vehicle_type, bbox) in tracked_objects.items():
            x1, y1, x2, y2 = bbox
            cx, cy = centroid
            
            # Choose color based on whether vehicle was newly counted
            if object_id in newly_counted:
                color = utils.Colors.YELLOW
            else:
                color = utils.Colors.GREEN
            
            # Draw bounding box
            label = f"ID:{object_id} {vehicle_type}"
            frame = utils.draw_bounding_box(frame, x1, y1, x2, y2, label, color)
            
            # Draw centroid
            cv2.circle(frame, (cx, cy), 4, utils.Colors.CYAN, -1)
        
        # Draw info panel
        frame = utils.display_info_panel(frame, vehicle_counts, self.current_fps)
        
        return frame
    
    def calculate_fps(self):
        """
        Calculate and update FPS
        """
        self.fps_counter += 1
        
        if self.fps_counter >= 10:  # Update every 10 frames
            fps_end_time = time.time()
            elapsed_time = fps_end_time - self.fps_start_time
            self.current_fps = self.fps_counter / elapsed_time
            
            # Reset
            self.fps_counter = 0
            self.fps_start_time = time.time()
    
    def run(self):
        """
        Main processing loop
        """
        print("\nStarting vehicle detection...")
        print("Press 'q' to quit, 's' to save screenshot, 'r' to reset counts")
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("\nEnd of video or error reading frame")
                    break
                
                # Frame skipping for performance
                self.frame_count += 1
                if self.frame_count % self.frame_skip != 0:
                    continue
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Calculate FPS
                self.calculate_fps()
                
                # Display frame
                cv2.imshow('Vehicle Detection & Counting System', processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\nQuitting...")
                    break
                elif key == ord('s'):
                    # Save screenshot
                    screenshot_path = f"output/screenshot_{int(time.time())}.jpg"
                    cv2.imwrite(screenshot_path, processed_frame)
                    print(f"Screenshot saved: {screenshot_path}")
                elif key == ord('r'):
                    # Reset counts
                    self.counter.reset_counts()
                    print("Counts reset!")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        
        finally:
            # Cleanup
            self.cleanup()
    
    def cleanup(self):
        """
        Clean up resources and generate final report
        """
        print("\n" + "=" * 60)
        print("GENERATING FINAL REPORT")
        print("=" * 60)
        
        # Get statistics
        stats = self.counter.get_statistics()
        
        print(f"\nTotal Vehicles Counted: {stats['total_vehicles']}")
        print(f"Vehicles per Minute: {stats['vehicles_per_minute']}")
        print(f"\nVehicle Distribution:")
        for vtype, count in stats['vehicles_by_type'].items():
            percentage = (count / stats['total_vehicles'] * 100) if stats['total_vehicles'] > 0 else 0
            print(f"  {vtype.capitalize():12s}: {count:4d} ({percentage:5.1f}%)")
        
        # Export summary
        self.counter.export_summary('output/summary.txt')
        
        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()
        
        print("\n✓ Data saved to: output/vehicle_counts.csv")
        print("✓ Summary saved to: output/summary.txt")
        print("\nThank you for using Vehicle Detection System!")
        print("=" * 60)


def main():
    """
    Main function with argument parsing
    """
    parser = argparse.ArgumentParser(
        description='Vehicle Detection & Counting System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a video file
  python main.py --source data/traffic_video.mp4
  
  # Use webcam
  python main.py --source 0
  
  # Custom model and confidence
  python main.py --source data/traffic_video.mp4 --model yolov8s.pt --conf 0.4
        """
    )
    
    parser.add_argument(
        '--source',
        type=str,
        default='data/traffic_video.mp4',
        help='Video file path or camera index (default: data/traffic_video.mp4)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='yolov8n.pt',
        help='YOLO model path (default: yolov8n.pt)'
    )
    
    parser.add_argument(
        '--conf',
        type=float,
        default=0.3,
        help='Confidence threshold (default: 0.3)'
    )
    
    args = parser.parse_args()
    
    # Convert camera index if numeric
    try:
        video_source = int(args.source)
    except ValueError:
        video_source = args.source
    
    # Create and run system
    system = VehicleDetectionSystem(
        video_source=video_source,
        model_path=args.model,
        confidence=args.conf
    )
    
    system.run()


if __name__ == "__main__":
    main()
