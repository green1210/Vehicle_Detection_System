# Installation & Testing Guide

## 🎯 Complete Installation & Testing Instructions

This guide will help you set up and test the Vehicle Detection System from scratch.

---

## 📋 Prerequisites Check

Before starting, verify you have:

1. **Python 3.8 or higher**
   ```bash
   python --version
   # Should show: Python 3.8.x or higher
   ```

2. **pip (Python package manager)**
   ```bash
   pip --version
   # Should show: pip x.x.x
   ```

3. **At least 2GB free disk space**
4. **Internet connection** (for downloading dependencies and model)

---

## 🔧 Installation Steps

### Step 1: Navigate to Project Directory

**Windows:**
```bash
cd c:\Users\manik\Downloads\Vec\Vehicle_Detection_Project
```

**Linux/Mac:**
```bash
cd ~/Downloads/Vehicle_Detection_Project
```

### Step 2: Create Virtual Environment (Recommended)

This keeps dependencies isolated from your system Python.

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your prompt
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your prompt
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Expected output:**
```
Collecting opencv-python>=4.8.0
Collecting numpy>=1.24.0
Collecting pandas>=2.0.0
Collecting matplotlib>=3.7.0
Collecting ultralytics>=8.0.0
Collecting scipy>=1.10.0
Collecting Pillow>=9.5.0
...
Successfully installed opencv-python-4.8.x numpy-1.24.x ...
```

This may take 2-5 minutes depending on your internet speed.

### Step 4: Verify Installation

```bash
# Test OpenCV
python -c "import cv2; print(f'OpenCV {cv2.__version__} installed ✓')"

# Test Ultralytics (YOLOv8)
python -c "from ultralytics import YOLO; print('YOLOv8 installed ✓')"

# Test Pandas
python -c "import pandas as pd; print(f'Pandas {pd.__version__} installed ✓')"

# Test Matplotlib
python -c "import matplotlib; print(f'Matplotlib {matplotlib.__version__} installed ✓')"
```

If all commands run without errors, you're ready! ✅

---

## 📹 Getting Test Video

### Option 1: Download from Pexels (Recommended)

1. **Visit:** https://www.pexels.com/search/videos/traffic/

2. **Search for:** "highway traffic"

3. **Recommended videos:**
   - "Busy Highway Traffic" by Taryn Elliott
   - "Cars on Highway" by Kelly L
   - "Traffic Flow" by Mikhail Nilov

4. **Download:**
   - Click on a video
   - Click "Free Download"
   - Choose "Full HD 1920x1080" or "HD 1280x720"

5. **Save as:**
   - Save to: `Vehicle_Detection_Project/data/`
   - Rename to: `traffic_video.mp4`

### Option 2: Download from Pixabay

1. **Visit:** https://pixabay.com/videos/search/traffic/
2. Download any traffic video
3. Save as `data/traffic_video.mp4`

### Option 3: Use Webcam

If you don't have a video, you can use your webcam:
```bash
python main.py --source 0
```

---

## 🧪 Testing the System

### Test 1: Verify Project Structure

```bash
# Windows
dir /s

# Linux/Mac
ls -R
```

You should see:
```
Vehicle_Detection_Project/
├── main.py
├── tracker.py
├── vehicle_counter.py
├── utils.py
├── visualization.py
├── requirements.txt
├── README.md
├── data/
│   ├── README.md
│   └── traffic_video.mp4  ← Your video here
└── output/  ← Will be created automatically
```

### Test 2: Run Detection System

```bash
python main.py
```

**What to expect:**

1. **Initialization (5-10 seconds):**
   ```
   ============================================================
   VEHICLE DETECTION & COUNTING SYSTEM
   ============================================================
   
   Initializing system...
   Video loaded: 1920x1080 @ 30 FPS
   Loading YOLO model: yolov8n.pt
   Downloading yolov8n.pt...  ← First run only
   ✓ Model loaded successfully
   ✓ Tracker initialized
   ✓ Counter initialized
   
   ✓ System ready!
   ============================================================
   ```

2. **Processing (continuous):**
   ```
   Starting vehicle detection...
   Press 'q' to quit, 's' to save screenshot, 'r' to reset counts
   
   [COUNTED] ID: 1, Type: car, Total: 1
   [COUNTED] ID: 3, Type: truck, Total: 2
   [COUNTED] ID: 5, Type: car, Total: 3
   ...
   ```

3. **Video Window:**
   - A window showing the video
   - Bounding boxes around vehicles
   - Counting line (red horizontal line)
   - Info panel (top-left corner)
   - FPS counter (top-right corner)

4. **Press 'Q' to quit:**
   ```
   Quitting...
   
   ============================================================
   GENERATING FINAL REPORT
   ============================================================
   
   Total Vehicles Counted: 45
   Vehicles per Minute: 15.2
   
   Vehicle Distribution:
     Car         :   30 (66.7%)
     Truck       :   10 (22.2%)
     Motorcycle  :    3 ( 6.7%)
     Bus         :    2 ( 4.4%)
   
   ✓ Data saved to: output/vehicle_counts.csv
   ✓ Summary saved to: output/summary.txt
   
   Thank you for using Vehicle Detection System!
   ============================================================
   ```

### Test 3: Check Output Files

```bash
# Windows
dir output

# Linux/Mac
ls -la output/
```

You should see:
```
output/
├── vehicle_counts.csv  ← Raw data
└── summary.txt         ← Text report
```

**View CSV file:**
```bash
# Windows
type output\vehicle_counts.csv

# Linux/Mac
cat output/vehicle_counts.csv
```

Expected format:
```csv
timestamp,vehicle_id,vehicle_type,total_count
2026-03-12 10:15:30,1,car,1
2026-03-12 10:15:35,3,truck,2
2026-03-12 10:15:40,5,car,3
```

### Test 4: Generate Visualizations

```bash
python visualization.py
```

**Expected output:**
```
============================================================
VEHICLE DETECTION SYSTEM - DATA ANALYTICS
============================================================

✓ Loaded 45 records from output/vehicle_counts.csv

============================================================
VEHICLE DETECTION ANALYTICS - SUMMARY
============================================================

Total Vehicles Detected: 45
Duration: 3.15 minutes
Average Rate: 14.29 vehicles/minute

Vehicle Distribution by Type:
----------------------------------------
  Car         :   30 (66.7%)
  Truck       :   10 (22.2%)
  Motorcycle  :    3 ( 6.7%)
  Bus         :    2 ( 4.4%)

============================================================

============================================================
GENERATING VISUALIZATIONS
============================================================

✓ Saved: output/vehicle_count_timeline.png
✓ Saved: output/vehicle_type_distribution.png
✓ Saved: output/vehicles_per_minute.png
✓ Saved: output/hourly_distribution.png
✓ Saved: output/comprehensive_dashboard.png

✓ All visualizations generated successfully!
============================================================

✓ Analysis complete! Check the 'output' folder for results.
```

**Check the graphs:**
```bash
# Windows - open output folder
explorer output

# Linux
xdg-open output/

# Mac
open output/
```

You should see 5 PNG files with beautiful graphs! 📊

### Test 5: Launch Interactive Dashboard

```bash
streamlit run dashboard.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

**What to see in the dashboard:**

1. **Dashboard automatically opens** in your default browser
2. **Sidebar Navigation:**
   - Overview - KPI metrics and vehicle summary
   - Analytics - Charts and visualizations
   - Peak Hours - Top traffic times
   - Anomalies - Unusual patterns
   - Detection Data - Raw records table

3. **Overview Tab Features:**
   - Total Vehicles counter
   - Analysis Duration
   - Detection Rate (vehicles/hour)
   - Traffic Trend indicator
   - Vehicle Type Summary table

**Close the dashboard:**
- Close the browser tab or press `Ctrl+C` in the terminal

---

## ✅ Success Criteria

Your installation is successful if:

1. ✅ No errors during `pip install`
2. ✅ All verification commands pass
3. ✅ `python main.py` runs without errors
4. ✅ Video window shows with detections
5. ✅ CSV file is created in `output/`
6. ✅ `python visualization.py` creates graphs
7. ✅ All 5 PNG files are generated

---

## 🐛 Troubleshooting

### Issue 1: "Python not found"

**Solution:**
```bash
# Windows: Check if Python is in PATH
where python

# Linux/Mac
which python3

# If not found, reinstall Python and add to PATH
```

### Issue 2: "pip install fails"

**Solutions:**

**Try upgrading pip:**
```bash
python -m pip install --upgrade pip
```

**Try installing one by one:**
```bash
pip install opencv-python
pip install numpy
pip install pandas
pip install matplotlib
pip install ultralytics
pip install scipy
```

**Use conda (alternative):**
```bash
conda install opencv numpy pandas matplotlib scipy
pip install ultralytics
```

### Issue 3: "ImportError: DLL load failed" (Windows)

**Solution:**
```bash
# Install Visual C++ Redistributable
# Download from Microsoft:
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### Issue 4: "Video file not found"

**Solution:**
```bash
# Check if video exists
# Windows
dir data\traffic_video.mp4

# Linux/Mac
ls -l data/traffic_video.mp4

# If not found, download and place in data/ folder
```

### Issue 5: "Model download fails"

**Solution 1 - Manual download:**
```bash
# Install ultralytics first
pip install ultralytics

# Download model manually
python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt')"
```

**Solution 2 - Use different model:**
```bash
# Try YOLOv8s instead
python main.py --model yolov8s.pt
```

### Issue 6: "Low FPS / Slow performance"

**Solutions:**

**Reduce frame processing:**
Edit `main.py`, change line:
```python
self.frame_skip = 2  # Change to 3 or 4
```

**Use smaller video:**
```bash
# Resize video with FFmpeg
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4
```

**Lower confidence:**
```bash
python main.py --conf 0.4
```

### Issue 7: "Too many false detections"

**Solution:**
```bash
# Increase confidence threshold
python main.py --conf 0.5  # or 0.6
```

### Issue 8: "Webcam not working"

**Solutions:**

**Try different camera index:**
```bash
python main.py --source 0  # Default
python main.py --source 1  # Alternative camera
```

**Check camera permissions:**
- Windows: Settings → Privacy → Camera
- Mac: System Preferences → Security & Privacy → Camera
- Linux: Check device: `ls /dev/video*`

### Issue 9: "No graphs generated"

**Solution:**
```bash
# Check if CSV exists
ls output/vehicle_counts.csv

# If CSV is empty or doesn't exist:
# 1. Run main.py first and let it count some vehicles
# 2. Then run visualization.py

# Install matplotlib backend
pip install pyqt5
```

### Issue 10: "Memory error"

**Solutions:**

**Reduce video size:**
```python
# Edit main.py, add after video loading:
frame = cv2.resize(frame, (1280, 720))
```

**Close other applications:**
- Free up RAM
- Close browser tabs
- Close other programs

---

## 🔍 Verification Checklist

Run through this checklist step by step:

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] pip working
- [ ] Virtual environment created
- [ ] Virtual environment activated

### Dependencies
- [ ] requirements.txt installed
- [ ] OpenCV import successful
- [ ] Ultralytics import successful
- [ ] Pandas import successful
- [ ] Matplotlib import successful

### Project Files
- [ ] All Python files present
- [ ] Data folder exists
- [ ] README.md readable
- [ ] requirements.txt readable

### Test Video
- [ ] Video downloaded
- [ ] Video placed in data/ folder
- [ ] Video renamed to traffic_video.mp4
- [ ] Video playable

### Run Tests
- [ ] main.py runs without errors
- [ ] Video window appears
- [ ] Detections visible
- [ ] Counting line visible
- [ ] Vehicles being counted
- [ ] Console showing count messages

### Output Files
- [ ] output/ folder created
- [ ] vehicle_counts.csv created
- [ ] CSV has data (not empty)
- [ ] summary.txt created

### Visualizations
- [ ] visualization.py runs
- [ ] 5 PNG files created
- [ ] Graphs look correct
- [ ] Dashboard shows data

---

## 📊 Performance Expectations

### Normal Performance

**Hardware: Intel i5/Ryzen 5, 8GB RAM, No GPU**
- Detection FPS: 20-30
- Detection time: 35-45ms per frame
- Memory usage: ~500MB
- CPU usage: 60-80%

**With GPU (CUDA-capable):**
- Detection FPS: 60-80
- Detection time: 10-15ms per frame
- Memory usage: ~800MB
- GPU usage: 50-70%

### If Your Performance is Lower

**10-15 FPS:**
- Still usable, but slower
- Try `frame_skip = 3` in main.py
- Or reduce video resolution

**< 10 FPS:**
- Too slow for real-time
- Definitely increase `frame_skip`
- Use smaller video (720p instead of 1080p)
- Consider YOLOv8n (nano) instead of larger models

---

## 🎓 Learning Path

Now that you have it working:

### Week 1: Understanding
- [ ] Read README.md
- [ ] Read STEP_BY_STEP_EXPLANATION.md
- [ ] Run with different videos
- [ ] Experiment with parameters

### Week 2: Customization
- [ ] Change counting line position
- [ ] Adjust confidence thresholds
- [ ] Modify colors and labels
- [ ] Try different YOLO models

### Week 3: Enhancement
- [ ] Add new features
- [ ] Improve accuracy
- [ ] Optimize performance
- [ ] Create custom visualizations

### Week 4: Presentation
- [ ] Prepare demo
- [ ] Create slides
- [ ] Practice explanation
- [ ] Document results

---

## 🎉 Congratulations!

If you've completed all tests successfully, you now have a fully working Vehicle Detection & Counting System!

### Next Steps:
1. ✅ Test with multiple videos
2. ✅ Explore the code
3. ✅ Read the documentation
4. ✅ Customize for your needs
5. ✅ Prepare your presentation!

---

## 📞 Still Having Issues?

### Resources:
1. **Check documentation:**
   - README.md
   - PROJECT_REPORT.md
   - STEP_BY_STEP_EXPLANATION.md

2. **Review code comments:**
   - Every function is documented
   - Inline comments explain logic

3. **Common solutions:**
   - Restart computer
   - Reinstall dependencies
   - Use different video
   - Try webcam instead

4. **Library documentation:**
   - OpenCV: https://docs.opencv.org/
   - Ultralytics: https://docs.ultralytics.com/
   - Pandas: https://pandas.pydata.org/docs/
   - Matplotlib: https://matplotlib.org/stable/

---

**System Status:** Ready for Use! ✅

**Good luck with your internship project!** 🚀
