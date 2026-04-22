"""
Premium Vehicle Detection Dashboard
====================================
Advanced analytics and real-time monitoring with modern premium design.
Features: Real-time metrics, interactive visualizations, anomaly detection,
export capabilities, and comprehensive traffic analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Vehicle Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com',
        'Report a bug': "https://github.com",
        'About': "Vehicle Detection & Analytics Platform"
    }
)

# Professional color scheme
COLORS = {
    'car': '#3498db',
    'bus': '#e74c3c',
    'truck': '#2ecc71',
    'motorcycle': '#f39c12',
    'primary': '#1a1a2e',
    'secondary': '#16213e',
    'accent': '#00d4ff',
    'accent2': '#ff6b9d',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#3498db',
    'light': '#ecf0f1'
}

# Enhanced CSS styling with modern design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap');
    
    * {
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main background - Premium gradient */
    .main {
        background: linear-gradient(180deg, #f0f4f8 0%, #d9e2ec 50%, #c5d9e8 100%);
        padding: 0;
    }
    
    /* Metric styling */
    .stMetric {
        background-color: transparent;
        padding: 0px;
        border-radius: 0px;
        box-shadow: none;
        border-left: none;
    }
    
    /* Modern glassmorphic card style */
    .kpi-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 28px;
        border-radius: 16px;
        margin: 12px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-left: 5px solid #667eea;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        pointer-events: none;
    }
    
    .kpi-card:hover {
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
        transform: translateY(-4px);
        border-left-color: #764ba2;
    }
    
    .kpi-value {
        font-size: 2.5em;
        font-weight: 800;
        margin: 10px 0;
        color: #1a1a2e;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .kpi-label {
        font-size: 0.85em;
        color: #7a8fa3;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .kpi-change {
        font-size: 0.9em;
        font-weight: 600;
        margin-top: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Alert boxes with glass effect */
    .alert-box {
        background: rgba(255, 243, 224, 0.8);
        backdrop-filter: blur(10px);
        border: 2px solid #f39c12;
        padding: 18px;
        border-radius: 12px;
        margin: 12px 0;
        box-shadow: 0 8px 24px rgba(243, 156, 18, 0.12);
    }
    
    .success-box {
        background: rgba(232, 248, 245, 0.8);
        backdrop-filter: blur(10px);
        border: 2px solid #2ecc71;
        padding: 18px;
        border-radius: 12px;
        margin: 12px 0;
        box-shadow: 0 8px 24px rgba(46, 204, 113, 0.12);
    }
    
    .danger-box {
        background: rgba(250, 219, 216, 0.8);
        backdrop-filter: blur(10px);
        border: 2px solid #e74c3c;
        padding: 18px;
        border-radius: 12px;
        margin: 12px 0;
        box-shadow: 0 8px 24px rgba(231, 76, 60, 0.12);
    }
    
    /* Header styling - Premium */
    .header-title {
        color: #1a1a2e;
        font-size: 3.2em;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: -1px;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-subtitle {
        color: #8b9cc7;
        font-size: 1.05em;
        font-weight: 500;
        letter-spacing: 0.3px;
        margin-top: -8px;
    }
    
    /* Section title - Premium */
    .section-title {
        color: #1a1a2e;
        font-size: 1.95em;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 18px;
        padding-bottom: 12px;
        padding-left: 0px;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.5px;
        position: relative;
        display: block;
        width: 100%;
    }
    
    .section-title:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    /* Tab styling */
    .tab-label {
        font-weight: 700;
        font-size: 1.15em;
        padding: 12px 0;
        color: #1a1a2e;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Data table styling - Premium */
    .stDataFrame {
        border-radius: 12px !important;
    }
    
    .dataframe {
        border-radius: 12px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Button styling - Premium */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Divider styling */
    .stHorizontalBlock hr {
        border-color: rgba(0, 0, 0, 0.1) !important;
        margin: 20px 0 !important;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(46, 204, 113, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 8px 32px rgba(46, 204, 113, 0.4) !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect [data-baseweb="base-input"] {
        border-radius: 10px !important;
    }
    
    /* Slider styling */
    .stSlider [data-baseweb="slider"] {
        border-radius: 10px !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #8b9cc7;
        padding: 24px;
        margin-top: 40px;
        border-top: 1px solid rgba(0, 0, 0, 0.08);
        font-size: 0.95em;
    }
    
    /* Chart container */
    .chart-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.6);
        margin: 16px 0;
    }
    </style>
""", unsafe_allow_html=True)


class AdvancedAnalytics:
    """Enhanced analytics with caching and performance optimization"""
    
    def __init__(self, csv_file_path='output/vehicle_counts.csv'):
        self.csv_file_path = csv_file_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and preprocess data"""
        try:
            if os.path.exists(self.csv_file_path):
                self.df = pd.read_csv(self.csv_file_path)
                self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
                self.df = self.df.sort_values('timestamp')
                self.df['vehicle_type'] = self.df['vehicle_type'].str.lower()
            else:
                self.df = pd.DataFrame()
        except Exception as e:
            self.df = pd.DataFrame()
    
    def get_summary_stats(self):
        """Get comprehensive summary statistics"""
        if self.df.empty:
            return {
                'total_vehicles': 0,
                'vehicle_types': {},
                'start_time': None,
                'end_time': None,
                'duration_hours': 0,
                'duration_minutes': 0,
                'vehicles_per_hour': 0,
                'vehicles_per_minute': 0,
                'trend': 'stable'
            }
        
        stats = {
            'total_vehicles': len(self.df),
            'vehicle_types': self.df['vehicle_type'].value_counts().to_dict(),
            'start_time': self.df['timestamp'].min(),
            'end_time': self.df['timestamp'].max(),
        }
        
        duration_mins = (stats['end_time'] - stats['start_time']).total_seconds() / 60
        stats['duration_minutes'] = round(duration_mins, 1) if duration_mins > 0 else 0
        stats['duration_hours'] = round(duration_mins / 60, 2) if duration_mins > 0 else 0
        stats['vehicles_per_minute'] = round(len(self.df) / max(duration_mins, 1), 2)
        stats['vehicles_per_hour'] = round(len(self.df) / max(stats['duration_hours'], 1), 0)
        
        # Calculate trend
        if len(self.df) > 10:
            first_half = len(self.df[:len(self.df)//2])
            second_half = len(self.df[len(self.df)//2:])
            if second_half > first_half * 1.1:
                stats['trend'] = 'increasing'
            elif second_half < first_half * 0.9:
                stats['trend'] = 'decreasing'
            else:
                stats['trend'] = 'stable'
        
        return stats
    
    def get_peak_hours(self, top_n=5):
        """Get peak traffic hours"""
        if self.df.empty:
            return pd.DataFrame()
        
        df_copy = self.df.copy()
        df_copy['hour'] = df_copy['timestamp'].dt.floor('1h')
        hourly = df_copy.groupby('hour').size().reset_index(name='count')
        return hourly.nlargest(top_n, 'count')
    
    def get_anomalies(self, sensitivity=1.5):
        """Detect anomalous traffic patterns"""
        if self.df.empty:
            return []
        
        df_copy = self.df.copy()
        df_copy['minute'] = df_copy['timestamp'].dt.floor('1min')
        minute_counts = df_copy.groupby('minute').size().reset_index(name='count')
        
        mean = minute_counts['count'].mean()
        std = minute_counts['count'].std()
        threshold = mean + (sensitivity * std)
        
        anomalies = minute_counts[minute_counts['count'] > threshold]
        return anomalies
    
    def get_heatmap_data(self):
        """Get hourly data for heatmap visualization"""
        if self.df.empty:
            return pd.DataFrame()
        
        df_copy = self.df.copy()
        df_copy['hour'] = df_copy['timestamp'].dt.hour
        df_copy['date'] = df_copy['timestamp'].dt.date
        
        heatmap_data = df_copy.groupby(['date', 'hour']).size().reset_index(name='count')
        return heatmap_data.pivot_table(index='hour', columns='date', values='count', fill_value=0)
    
    def get_vehicles_timeline(self):
        """Get minute-by-minute vehicle counts"""
        if self.df.empty:
            return pd.DataFrame()
        
        df_copy = self.df.copy()
        df_copy['minute'] = df_copy['timestamp'].dt.floor('1min')
        return df_copy.groupby('minute').size().reset_index(name='count').sort_values('minute')
    
    def get_type_by_hour(self):
        """Get vehicle type distribution by hour"""
        if self.df.empty:
            return pd.DataFrame()
        
        df_copy = self.df.copy()
        df_copy['hour'] = df_copy['timestamp'].dt.floor('1h')
        return df_copy.groupby(['hour', 'vehicle_type']).size().reset_index(name='count')
    
    def get_statistics_by_type(self):
        """Get detailed statistics for each vehicle type"""
        if self.df.empty:
            return {}
        
        stats = {}
        for vtype in self.df['vehicle_type'].unique():
            subset = self.df[self.df['vehicle_type'] == vtype]
            stats[vtype] = {
                'count': len(subset),
                'percentage': round(len(subset) / len(self.df) * 100, 1),
                'first_detected': subset['timestamp'].min(),
                'last_detected': subset['timestamp'].max()
            }
        return stats
    
    def generate_report(self):
        """Generate comprehensive text report"""
        stats = self.get_summary_stats()
        if stats['total_vehicles'] == 0:
            return "No data available to generate report."
        
        report = f"""
VEHICLE DETECTION ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

SUMMARY STATISTICS
{'-'*50}
Total Vehicles Detected: {stats['total_vehicles']}
Analysis Duration: {stats['duration_hours']:.1f} hours ({stats['duration_minutes']:.0f} minutes)
Average Detection Rate: {stats['vehicles_per_hour']:.0f} vehicles/hour
Peak Rate: {stats['vehicles_per_minute']} vehicles/minute

VEHICLE TYPE BREAKDOWN
{'-'*50}
"""
        
        type_stats = self.get_statistics_by_type()
        for vtype, data in sorted(type_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            report += f"{vtype.capitalize()}: {data['count']} ({data['percentage']}%)\n"
        
        report += f"\nTRAFFIC TREND: {stats['trend'].upper()}\n"
        
        # Peak hours
        peak_hours = self.get_peak_hours(3)
        if not peak_hours.empty:
            report += f"\nTOP PEAK HOURS\n{'-'*50}\n"
            for idx, row in peak_hours.iterrows():
                report += f"{row['hour'].strftime('%H:%M')} - {int(row['count'])} vehicles\n"
        
        return report




def render_kpi_metrics(analytics):
    """Render KPI metrics with enhanced visual design and status indicators"""
    stats = analytics.get_summary_stats()
    
    # Create 4 column layout for KPIs
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    # KPI 1: Total Vehicles
    with col1:
        st.markdown("""
            <div class='kpi-card'>
                <div class='kpi-label'>Total Vehicles</div>
                <div class='kpi-value'>""" + f"{stats['total_vehicles']:,}" + """</div>
                <div class='kpi-change' style='color: #3498db;'>🚗 Vehicles Detected</div>
            </div>
        """, unsafe_allow_html=True)
    
    # KPI 2: Duration
    with col2:
        st.markdown(f"""
            <div class='kpi-card' style='border-left-color: #e74c3c;'>
                <div class='kpi-label'>Analysis Duration</div>
                <div class='kpi-value'>{stats['duration_hours']:.1f}h</div>
                <div class='kpi-change' style='color: #e74c3c;'>⏱️ {stats['duration_minutes']:.0f} minutes</div>
            </div>
        """, unsafe_allow_html=True)
    
    # KPI 3: Detection Rate
    with col3:
        st.markdown(f"""
            <div class='kpi-card' style='border-left-color: #2ecc71;'>
                <div class='kpi-label'>Detection Rate</div>
                <div class='kpi-value'>{stats['vehicles_per_hour']:.0f}</div>
                <div class='kpi-change' style='color: #2ecc71;'>📈 vehicles/hour</div>
            </div>
        """, unsafe_allow_html=True)
    
    # KPI 4: Traffic Trend
    with col4:
        trend_color = '#2ecc71' if stats['trend'] == 'increasing' else '#f39c12' if stats['trend'] == 'stable' else '#e74c3c'
        trend_icon = '📈' if stats['trend'] == 'increasing' else '→' if stats['trend'] == 'stable' else '📉'
        st.markdown(f"""
            <div class='kpi-card' style='border-left-color: {trend_color};'>
                <div class='kpi-label'>Traffic Trend</div>
                <div class='kpi-value'>{stats['trend'].capitalize()}</div>
                <div class='kpi-change' style='color: {trend_color};'>{trend_icon} Pattern Status</div>
            </div>
        """, unsafe_allow_html=True)


def render_quick_stats(analytics):
    """Render vehicle type summary and additional statistics with enhanced design"""
    stats = analytics.get_summary_stats()
    type_stats = analytics.get_statistics_by_type()
    
    
    st.markdown("""
    <div style='margin-top: 28px; margin-bottom: 18px;'>
        <h3 style='color: #1a1a2; font-size: 1.95em; font-weight: 700; margin: 0; padding: 0;'>
            🚗 Vehicle Type Summary
        </h3>
        <div style='width: 60px; height: 4px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 2px; margin-top: 8px;'></div>
    </div>
    """, unsafe_allow_html=True)
    
    if type_stats:
        # Create summary table with enhanced styling
        summary_data = []
        for vtype, data in sorted(type_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            duration_mins = (data['last_detected'] - data['first_detected']).total_seconds() / 60
            summary_data.append({
                'Type': f"**{vtype.capitalize()}**",
                'Count': f"**{data['count']}**",
                'Share': f"{data['percentage']}%",
                'First': data['first_detected'].strftime('%H:%M:%S'),
                'Last': data['last_detected'].strftime('%H:%M:%S'),
                'Duration': f"{duration_mins:.0f}m"
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, hide_index=True, width='stretch', height=250)
    else:
        st.info("📊 No vehicle type data available yet")
    
    # Additional Statistics Section
    st.markdown("""
    <div style='margin-top: 28px; margin-bottom: 18px;'>
        <h3 style='color: #1a1a2; font-size: 1.95em; font-weight: 700; margin: 0; padding: 0;'>
            📊 Traffic Statistics
        </h3>
        <div style='width: 60px; height: 4px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 2px; margin-top: 8px;'></div>
    </div>
    """, unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3 = st.columns(3, gap="medium")
    
    with stat_col1:
        avg_interval = stats['duration_minutes'] / max(stats['total_vehicles'], 1)
        st.markdown(f"""
            <div class='kpi-card' style='border-left-color: #3498db;'>
                <div class='kpi-label'>Avg Interval</div>
                <div class='kpi-value'>{avg_interval:.1f}s</div>
                <div class='kpi-change' style='color: #3498db;'>⏰ Between detections</div>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f"""
            <div class='kpi-card' style='border-left-color: #e74c3c;'>
                <div class='kpi-label'>Peak Rate</div>
                <div class='kpi-value'>{stats['vehicles_per_minute']:.2f}</div>
                <div class='kpi-change' style='color: #e74c3c;'>⚡ /minute</div>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown(f"""
            <div class='kpi-card' style='border-left-color: #2ecc71;'>
                <div class='kpi-label'>Analysis Period</div>
                <div class='kpi-value'>{stats['duration_minutes']:.0f}m</div>
                <div class='kpi-change' style='color: #2ecc71;'>📅 Total duration</div>
            </div>
        """, unsafe_allow_html=True)


def render_advanced_charts(analytics):
    """Render advanced analytical charts with enhanced styling"""
    st.markdown("<div class='section-title'>📈 Advanced Analytics</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Timeline", "🎯 Distribution", "🔥 Heatmap", "📉 Type Trends"])
    
    # Tab 1: Timeline
    with tab1:
        timeline_data = analytics.get_vehicles_timeline()
        if not timeline_data.empty:
            fig, ax = plt.subplots(figsize=(14, 6.5), facecolor='white', edgecolor='none')
            
            # Enhanced gradient fill
            ax.fill_between(timeline_data['minute'], timeline_data['count'], alpha=0.25, color='#667eea', label='Vehicle Count')
            
            # Premium line styling
            ax.plot(timeline_data['minute'], timeline_data['count'], linewidth=3.5, color='#667eea', 
                   marker='o', markersize=6, markerfacecolor='#764ba2', markeredgewidth=2.5, markeredgecolor='#667eea', zorder=3)
            
            ax.set_title('Real-Time Vehicle Detection Timeline', fontsize=16, fontweight='bold', color='#1a1a2e', pad=20)
            ax.set_xlabel('Time', fontsize=12, fontweight='bold', color='#1a1a2e')
            ax.set_ylabel('Vehicle Count', fontsize=12, fontweight='bold', color='#1a1a2e')
            ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.8, color='#667eea')
            ax.set_facecolor('#fafbfc')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#e0e0e0')
            ax.spines['bottom'].set_color('#e0e0e0')
            ax.legend(fontsize=11, loc='upper left', framealpha=0.95, edgecolor='#e0e0e0')
            plt.xticks(rotation=45, fontsize=10, color='#7a8fa3')
            plt.yticks(fontsize=10, color='#7a8fa3')
            fig.patch.set_alpha(0.98)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("📊 No timeline data available")
    
    # Tab 2: Type Distribution
    with tab2:
        stats = analytics.get_summary_stats()
        if stats['vehicle_types']:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Pie Chart Distribution**")
                fig, ax = plt.subplots(figsize=(8, 6.5), facecolor='white', edgecolor='none')
                colors_list = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
                wedges, texts, autotexts = ax.pie(
                    stats['vehicle_types'].values(), 
                    labels=[v.capitalize() for v in stats['vehicle_types'].keys()],
                    autopct='%1.1f%%',
                    colors=colors_list[:len(stats['vehicle_types'])],
                    startangle=90,
                    textprops={'fontsize': 11, 'weight': 'bold', 'color': '#1a1a2e'},
                    wedgeprops={'edgecolor': 'white', 'linewidth': 3}
                )
                ax.set_title('Vehicle Type Distribution', fontsize=14, fontweight='bold', color='#1a1a2e', pad=20)
                fig.patch.set_alpha(0.98)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Bar Chart Comparison**")
                fig, ax = plt.subplots(figsize=(8, 6.5), facecolor='white', edgecolor='none')
                vehicle_types = stats['vehicle_types']
                vehicle_names = [v.capitalize() for v in vehicle_types.keys()]
                vehicle_counts = list(vehicle_types.values())
                bars = ax.barh(vehicle_names, vehicle_counts, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'][:len(vehicle_types)], 
                             edgecolor='#667eea', linewidth=2, height=0.6)
                ax.set_title('Vehicle Count by Type', fontsize=14, fontweight='bold', color='#1a1a2e', pad=20)
                ax.set_xlabel('Count', fontsize=11, fontweight='bold', color='#1a1a2e')
                ax.set_facecolor('#fafbfc')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#e0e0e0')
                ax.spines['bottom'].set_color('#e0e0e0')
                
                # Add value labels
                for bar, count in zip(bars, vehicle_counts):
                    width = bar.get_width()
                    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{int(count)}', 
                           ha='left', va='center', fontsize=11, fontweight='bold', color='#1a1a2e')
                
                fig.patch.set_alpha(0.98)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
        else:
            st.info("🎯 No vehicle type data available")
    
    # Tab 3: Heatmap
    with tab3:
        heatmap_data = analytics.get_heatmap_data()
        if not heatmap_data.empty and heatmap_data.shape[0] > 0:
            fig, ax = plt.subplots(figsize=(14, 6.5), facecolor='white', edgecolor='none')
            sns.heatmap(heatmap_data, cmap='RdYlGn_r', annot=True, fmt='g', cbar_kws={'label': 'Vehicle Count'}, 
                       ax=ax, linewidths=1, linecolor='white', cbar=True, square=False)
            ax.set_title('Traffic Heatmap - Vehicles by Hour and Date', fontsize=14, fontweight='bold', color='#1a1a2e', pad=20)
            ax.set_ylabel('Hour of Day', fontsize=11, fontweight='bold', color='#1a1a2e')
            ax.set_xlabel('Date', fontsize=11, fontweight='bold', color='#1a1a2e')
            ax.set_facecolor('#fafbfc')
            plt.xticks(rotation=45, fontsize=9, color='#7a8fa3')
            plt.yticks(fontsize=9, color='#7a8fa3')
            fig.patch.set_alpha(0.98)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("🔥 Not enough data for heatmap visualization (requires multiple hours/days)")
    
    # Tab 4: Type Over Time
    with tab4:
        type_by_hour = analytics.get_type_by_hour()
        if not type_by_hour.empty:
            fig, ax = plt.subplots(figsize=(14, 6.5), facecolor='white', edgecolor='none')
            
            colors_map = {'car': '#3498db', 'bus': '#e74c3c', 'truck': '#2ecc71', 'motorcycle': '#f39c12'}
            
            for vtype in type_by_hour['vehicle_type'].unique():
                data = type_by_hour[type_by_hour['vehicle_type'] == vtype]
                ax.plot(data['hour'], data['count'], marker='o', linewidth=3, label=vtype.capitalize(), 
                       color=colors_map.get(vtype, '#667eea'), markersize=8, markeredgewidth=2, markeredgecolor='white', zorder=3)
            
            ax.set_title('Vehicle Type Trends Over Time', fontsize=14, fontweight='bold', color='#1a1a2e', pad=20)
            ax.set_xlabel('Time', fontsize=11, fontweight='bold', color='#1a1a2e')
            ax.set_ylabel('Count', fontsize=11, fontweight='bold', color='#1a1a2e')
            ax.legend(loc='best', fontsize=11, framealpha=0.95, edgecolor='#e0e0e0')
            ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.8, color='#667eea')
            ax.set_facecolor('#fafbfc')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#e0e0e0')
            ax.spines['bottom'].set_color('#e0e0e0')
            plt.xticks(rotation=45, fontsize=10, color='#7a8fa3')
            plt.yticks(fontsize=10, color='#7a8fa3')
            fig.patch.set_alpha(0.98)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("📉 No type-by-hour data available")


def render_peak_hours(analytics):
    """Render peak hours analysis with enhanced visualization"""
    st.markdown("<div class='section-title'>⏰ Peak Hours Analysis</div>", unsafe_allow_html=True)
    
    peak_hours = analytics.get_peak_hours(10)
    
    if not peak_hours.empty:
        col1, col2 = st.columns([2.5, 1.5])
        
        with col1:
            fig, ax = plt.subplots(figsize=(12, 6.5), facecolor='white', edgecolor='none')
            bars = ax.bar(range(len(peak_hours)), peak_hours['count'].values, color='#667eea', 
                         edgecolor='#764ba2', linewidth=2.5, alpha=0.85, width=0.7)
            ax.set_title('Top 10 Peak Traffic Hours', fontsize=14, fontweight='bold', color='#1a1a2e', pad=20)
            ax.set_ylabel('Vehicle Count', fontsize=11, fontweight='bold', color='#1a1a2e')
            ax.set_xlabel('Time Window', fontsize=11, fontweight='bold', color='#1a1a2e')
            ax.set_xticks(range(len(peak_hours)))
            ax.set_xticklabels([h.strftime('%H:%M') for h in peak_hours['hour']], rotation=45, fontsize=10, color='#7a8fa3')
            ax.set_facecolor('#fafbfc')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#e0e0e0')
            ax.spines['bottom'].set_color('#e0e0e0')
            ax.grid(axis='y', alpha=0.15, linestyle='--', linewidth=0.8, color='#667eea')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1a1a2e')
            
            fig.patch.set_alpha(0.98)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Peak Hours Table")
            display_df = peak_hours.copy()
            display_df['hour'] = display_df['hour'].dt.strftime('%H:%M')
            display_df.columns = ['⏰ Time', '🚗 Vehicles']
            st.dataframe(display_df, hide_index=True, width='stretch')
    else:
        st.info("⏰ No peak hours data available")


def render_anomalies(analytics):
    """Render anomaly detection with enhanced visual alerts"""
    st.markdown("<div class='section-title'>⚠️ Traffic Anomalies</div>", unsafe_allow_html=True)
    
    anomalies = analytics.get_anomalies(sensitivity=1.5)
    
    if not anomalies.empty and len(anomalies) > 0:
        st.markdown(f"""
            <div class='danger-box'>
                <strong>🔔 ALERT: {len(anomalies)} Anomalies Detected</strong><br>
                Unusual traffic patterns found in the detection data.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Anomaly Details")
        display_df = anomalies.copy()
        display_df['minute'] = display_df['minute'].dt.strftime('%Y-%m-%d %H:%M:%S')
        display_df.columns = ['Timestamp', 'Vehicle Count']
        st.dataframe(display_df, hide_index=True, use_container_width=True)
    else:
        st.markdown("""
            <div class='success-box'>
                <strong>✅ All Clear</strong><br>
                No anomalies detected - Normal traffic patterns observed.
            </div>
        """, unsafe_allow_html=True)


def render_data_table(analytics):
    """Render advanced data table with enhanced filtering and export"""
    st.markdown("<div class='section-title'>📋 Detailed Detection Records</div>", unsafe_allow_html=True)
    
    if analytics.df.empty:
        st.warning("⚠️ No data available")
        return
    
    # Filtering options with better layout
    st.markdown("#### Filters & Options")
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        vehicle_type_filter = st.multiselect(
            "🚗 Vehicle Type",
            options=sorted(analytics.df['vehicle_type'].unique()),
            default=sorted(analytics.df['vehicle_type'].unique()),
            key="vehicle_type_filter"
        )
    
    with col2:
        rows_to_show = st.slider("📊 Show Records", 5, min(100, len(analytics.df)), 25)
    
    with col3:
        st.write("")  # Spacer
        if st.button("📥 Download CSV", use_container_width=True):
            csv = analytics.df.to_csv(index=False)
            st.download_button(
                label="📥 Click to Download",
                data=csv,
                file_name=f"vehicle_detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="csv_download"
            )
    
    with col4:
        st.write("")  # Spacer
        if st.button("📄 Generate Report", use_container_width=True):
            report = analytics.generate_report()
            st.text_area("📄 Analysis Report", value=report, height=300, disabled=True, key="report_text")
    
    st.divider()
    
    # Apply filters
    filtered_df = analytics.df[analytics.df['vehicle_type'].isin(vehicle_type_filter)].copy()
    display_df = filtered_df.tail(rows_to_show).copy()
    display_df['timestamp'] = display_df['timestamp'].astype(str)
    
    # Display statistics
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total Records", len(filtered_df))
    with col_stat2:
        st.metric("Displayed", len(display_df))
    with col_stat3:
        st.metric("Vehicle Types", len(vehicle_type_filter))
    
    # Data table
    st.markdown("#### Records Table")
    st.dataframe(display_df, width='stretch', hide_index=True, height=400)


def render_sidebar_controls(csv_path_value='output/vehicle_counts.csv'):
    """Render sidebar controls with navigation"""
    
    # Navigation
    st.sidebar.markdown("### Navigation")
    
    nav_options = ["Overview", "Analytics", "Peak Hours", "Anomalies", "Detection Data"]
    
    selected = st.sidebar.radio(
        "Select Section",
        nav_options,
        index=nav_options.index(st.session_state.get('selected_tab', 'Overview'))
    )
    
    st.session_state.selected_tab = selected
    
    return csv_path_value


def main():
    """Main dashboard application with modern premium design"""
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'selected_tab' not in st.session_state:
        st.session_state.selected_tab = 'Overview'
    
    # Enhanced Header with gradient
    header_col1, header_col2 = st.columns([4, 1])
    
    with header_col1:
        st.markdown("<div class='header-title'>🚗 Vehicle Analytics Dashboard</div>", unsafe_allow_html=True)
        st.markdown("<div class='header-subtitle'>Real-time traffic analysis and detection system • Powered by YOLOv8</div>", unsafe_allow_html=True)
    
    with header_col2:
        st.write("")
        if st.button("Refresh Data", use_container_width=True, key="refresh_btn"):
            st.rerun()
    
    st.divider()
    
    # Render sidebar and get csv path
    csv_path = render_sidebar_controls()
    
    # Load analytics with the csv path
    analytics = AdvancedAnalytics(csv_path)
    
    # Check if data exists
    if analytics.df.empty:
        st.error("❌ No data found in database")
        st.warning(
            "Please run the vehicle detection system first:\n\n"
            "```bash\npython main.py -v <video_path>\n```\n\n"
            "Then refresh this dashboard."
        )
        return
    
    # Display selected tab based on sidebar navigation
    if st.session_state.selected_tab == 'Overview':
        render_kpi_metrics(analytics)
        st.divider()
        render_quick_stats(analytics)
    
    elif st.session_state.selected_tab == 'Analytics':
        render_advanced_charts(analytics)
    
    elif st.session_state.selected_tab == 'Peak Hours':
        render_peak_hours(analytics)
    
    elif st.session_state.selected_tab == 'Anomalies':
        render_anomalies(analytics)
    
    elif st.session_state.selected_tab == 'Detection Data':
        render_data_table(analytics)
    
    # Enhanced Footer
    st.divider()
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    
    with col_f1:
        last_update = analytics.df['timestamp'].max() if not analytics.df.empty else None
        if last_update:
            st.caption(f"📅 Last Updated: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col_f2:
        st.markdown(
            "<div style='text-align: center; color: #999; font-size: 0.9em;'>"
            "<p style='margin: 0;'>🚗 Vehicle Detection Dashboard | 📊 Advanced Analytics | ⚡ Real-Time Monitoring |  </p>"
            "</div>",
            unsafe_allow_html=True
        )
    
    with col_f3:
        st.caption(f"🛠️ Powered by Streamlit & YOLOv8")


if __name__ == "__main__":
    main()
