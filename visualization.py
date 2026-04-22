"""
Visualization & Analytics Module
=================================
This module provides data analysis and visualization capabilities
for the vehicle detection system using Matplotlib and Pandas.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os


class VehicleAnalytics:
    """
    Vehicle Analytics class for data analysis and visualization
    """
    
    def __init__(self, csv_file_path='output/vehicle_counts.csv'):
        """
        Initialize analytics module
        
        Args:
            csv_file_path: Path to CSV data file
        """
        self.csv_file_path = csv_file_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """
        Load data from CSV file
        """
        try:
            if not os.path.exists(self.csv_file_path):
                print(f"Warning: File not found: {self.csv_file_path}")
                self.df = pd.DataFrame()
                return
            
            self.df = pd.read_csv(self.csv_file_path)
            
            # Convert timestamp to datetime
            if 'timestamp' in self.df.columns:
                self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            
            print(f"✓ Loaded {len(self.df)} records from {self.csv_file_path}")
        
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame()
    
    def get_summary_statistics(self):
        """
        Get summary statistics from the data
        
        Returns:
            Dictionary with statistics
        """
        if self.df.empty:
            return {}
        
        stats = {
            'total_vehicles': len(self.df),
            'vehicle_types': self.df['vehicle_type'].value_counts().to_dict(),
            'start_time': self.df['timestamp'].min(),
            'end_time': self.df['timestamp'].max(),
        }
        
        # Calculate duration
        if 'timestamp' in self.df.columns and len(self.df) > 0:
            duration = (stats['end_time'] - stats['start_time']).total_seconds() / 60
            stats['duration_minutes'] = round(duration, 2)
            stats['vehicles_per_minute'] = round(len(self.df) / duration, 2) if duration > 0 else 0
        
        return stats
    
    def print_summary(self):
        """
        Print a formatted summary of the data
        """
        stats = self.get_summary_statistics()
        
        if not stats:
            print("No data available for analysis")
            return
        
        print("\n" + "=" * 60)
        print("VEHICLE DETECTION ANALYTICS - SUMMARY")
        print("=" * 60)
        
        print(f"\nTotal Vehicles Detected: {stats['total_vehicles']}")
        print(f"Duration: {stats.get('duration_minutes', 0):.2f} minutes")
        print(f"Average Rate: {stats.get('vehicles_per_minute', 0):.2f} vehicles/minute")
        
        print("\nVehicle Distribution by Type:")
        print("-" * 40)
        for vtype, count in stats['vehicle_types'].items():
            percentage = (count / stats['total_vehicles']) * 100
            print(f"  {vtype.capitalize():12s}: {count:4d} ({percentage:5.1f}%)")
        
        print("\n" + "=" * 60)
    
    def plot_vehicle_counts_over_time(self, output_path='output/vehicle_count_timeline.png'):
        """
        Plot cumulative vehicle count over time
        
        Args:
            output_path: Path to save the plot
        """
        if self.df.empty:
            print("No data to plot")
            return
        
        plt.figure(figsize=(12, 6))
        
        # Plot cumulative count
        plt.plot(self.df['timestamp'], self.df['total_count'], 
                linewidth=2, color='#2E86AB', marker='o', markersize=4)
        
        plt.xlabel('Time', fontsize=12, fontweight='bold')
        plt.ylabel('Cumulative Vehicle Count', fontsize=12, fontweight='bold')
        plt.title('Vehicle Count Over Time', fontsize=14, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
        plt.close()
    
    def plot_vehicle_type_distribution(self, output_path='output/vehicle_type_distribution.png'):
        """
        Plot vehicle type distribution as pie chart and bar chart
        
        Args:
            output_path: Path to save the plot
        """
        if self.df.empty:
            print("No data to plot")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Count vehicles by type
        type_counts = self.df['vehicle_type'].value_counts()
        
        # Define colors for different vehicle types
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        # Pie chart
        wedges, texts, autotexts = ax1.pie(type_counts.values, 
                                            labels=type_counts.index,
                                            autopct='%1.1f%%',
                                            colors=colors,
                                            startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})
        
        ax1.set_title('Vehicle Type Distribution (Percentage)', 
                     fontsize=13, fontweight='bold', pad=15)
        
        # Bar chart
        bars = ax2.bar(type_counts.index, type_counts.values, color=colors, alpha=0.8)
        ax2.set_xlabel('Vehicle Type', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax2.set_title('Vehicle Type Distribution (Count)', 
                     fontsize=13, fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
        plt.close()
    
    def plot_vehicles_per_minute(self, output_path='output/vehicles_per_minute.png'):
        """
        Plot vehicles detected per minute
        
        Args:
            output_path: Path to save the plot
        """
        if self.df.empty or 'timestamp' not in self.df.columns:
            print("No timestamp data available")
            return
        
        # Group by minute
        self.df['minute'] = self.df['timestamp'].dt.floor('T')
        vehicles_per_minute = self.df.groupby('minute').size()
        
        plt.figure(figsize=(12, 6))
        
        # Create bar plot
        bars = plt.bar(range(len(vehicles_per_minute)), vehicles_per_minute.values, 
                      color='#6C5CE7', alpha=0.8, edgecolor='black', linewidth=1.2)
        
        # Highlight maximum
        max_idx = vehicles_per_minute.values.argmax()
        bars[max_idx].set_color('#FF6B6B')
        
        plt.xlabel('Time (Minutes)', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Vehicles', fontsize=12, fontweight='bold')
        plt.title('Traffic Volume per Minute', fontsize=14, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # Add average line
        avg_value = vehicles_per_minute.mean()
        plt.axhline(y=avg_value, color='red', linestyle='--', 
                   linewidth=2, label=f'Average: {avg_value:.1f}')
        
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
        plt.close()
    
    def plot_hourly_distribution(self, output_path='output/hourly_distribution.png'):
        """
        Plot vehicle distribution by hour of day
        
        Args:
            output_path: Path to save the plot
        """
        if self.df.empty or 'timestamp' not in self.df.columns:
            print("No timestamp data available")
            return
        
        # Extract hour
        self.df['hour'] = self.df['timestamp'].dt.hour
        hourly_counts = self.df.groupby('hour').size()
        
        plt.figure(figsize=(12, 6))
        
        plt.plot(hourly_counts.index, hourly_counts.values, 
                marker='o', markersize=8, linewidth=2.5, 
                color='#00B894', markerfacecolor='#FF7675')
        
        plt.xlabel('Hour of Day', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Vehicles', fontsize=12, fontweight='bold')
        plt.title('Vehicle Distribution by Hour', fontsize=14, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.xticks(range(24))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
        plt.close()
    
    def plot_comprehensive_dashboard(self, output_path='output/comprehensive_dashboard.png'):
        """
        Create a comprehensive dashboard with multiple plots
        
        Args:
            output_path: Path to save the dashboard
        """
        if self.df.empty:
            print("No data to plot")
            return
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Cumulative count over time
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(self.df['timestamp'], self.df['total_count'], 
                linewidth=2.5, color='#2E86AB', marker='o', markersize=3)
        ax1.set_xlabel('Time', fontweight='bold')
        ax1.set_ylabel('Cumulative Count', fontweight='bold')
        ax1.set_title('1. Vehicle Count Timeline', fontweight='bold', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Vehicle type pie chart
        ax2 = fig.add_subplot(gs[1, 0])
        type_counts = self.df['vehicle_type'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        ax2.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax2.set_title('2. Vehicle Type Distribution', fontweight='bold', fontsize=12)
        
        # 3. Vehicle type bar chart
        ax3 = fig.add_subplot(gs[1, 1])
        bars = ax3.bar(type_counts.index, type_counts.values, color=colors, alpha=0.8)
        ax3.set_xlabel('Vehicle Type', fontweight='bold')
        ax3.set_ylabel('Count', fontweight='bold')
        ax3.set_title('3. Vehicle Counts by Type', fontweight='bold', fontsize=12)
        ax3.grid(True, alpha=0.3, axis='y')
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Vehicles per minute
        if 'minute' not in self.df.columns:
            self.df['minute'] = self.df['timestamp'].dt.floor('T')
        vehicles_per_minute = self.df.groupby('minute').size()
        
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.bar(range(len(vehicles_per_minute)), vehicles_per_minute.values,
               color='#6C5CE7', alpha=0.8)
        avg_vpm = vehicles_per_minute.mean()
        ax4.axhline(y=avg_vpm, color='red', linestyle='--', linewidth=2,
                   label=f'Avg: {avg_vpm:.1f}')
        ax4.set_xlabel('Time (Minutes)', fontweight='bold')
        ax4.set_ylabel('Vehicle Count', fontweight='bold')
        ax4.set_title('4. Traffic Volume per Minute', fontweight='bold', fontsize=12)
        ax4.grid(True, alpha=0.3, axis='y')
        ax4.legend()
        
        # 5. Statistics table
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.axis('off')
        
        stats = self.get_summary_statistics()
        stats_text = [
            ['Metric', 'Value'],
            ['Total Vehicles', f"{stats.get('total_vehicles', 0)}"],
            ['Duration (min)', f"{stats.get('duration_minutes', 0):.2f}"],
            ['Vehicles/min', f"{stats.get('vehicles_per_minute', 0):.2f}"],
        ]
        
        for vtype, count in stats.get('vehicle_types', {}).items():
            stats_text.append([f'{vtype.capitalize()}', f'{count}'])
        
        table = ax5.table(cellText=stats_text, cellLoc='left',
                         bbox=[0, 0, 1, 1], colWidths=[0.6, 0.4])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Style header row
        for i in range(2):
            table[(0, i)].set_facecolor('#3498db')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(stats_text)):
            for j in range(2):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#ecf0f1')
        
        ax5.set_title('5. Summary Statistics', fontweight='bold', fontsize=12, pad=20)
        
        # Main title
        fig.suptitle('Vehicle Detection System - Comprehensive Analytics Dashboard', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved comprehensive dashboard: {output_path}")
        plt.close()
    
    def generate_all_plots(self):
        """
        Generate all visualization plots
        """
        print("\n" + "=" * 60)
        print("GENERATING VISUALIZATIONS")
        print("=" * 60 + "\n")
        
        if self.df.empty:
            print("No data available for visualization")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Generate all plots
        self.plot_vehicle_counts_over_time()
        self.plot_vehicle_type_distribution()
        self.plot_vehicles_per_minute()
        
        if 'timestamp' in self.df.columns:
            self.plot_hourly_distribution()
        
        self.plot_comprehensive_dashboard()
        
        print("\n✓ All visualizations generated successfully!")
        print("=" * 60)


def main():
    """
    Main function to run analytics and generate visualizations
    """
    print("\n" + "=" * 60)
    print("VEHICLE DETECTION SYSTEM - DATA ANALYTICS")
    print("=" * 60)
    
    # Initialize analytics
    analytics = VehicleAnalytics('output/vehicle_counts.csv')
    
    # Print summary
    analytics.print_summary()
    
    # Generate visualizations
    analytics.generate_all_plots()
    
    print("\n✓ Analysis complete! Check the 'output' folder for results.")


if __name__ == "__main__":
    main()
