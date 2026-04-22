# Data Folder Instructions

## 📁 Purpose

This folder contains input video files for the Vehicle Detection System.

## 🎥 Required Files

Place your traffic video file here with the name:
- **traffic_video.mp4**

Or use any name and specify it when running:
```bash
python main.py --source data/your_video_name.mp4
```

## 📥 Where to Get Traffic Videos

### Free Video Sources (No Copyright):

1. **Pexels** (Recommended)
   - URL: https://www.pexels.com/search/videos/traffic/
   - License: Free to use, no attribution required
   - Quality: High (HD/4K available)
   - Search: "traffic highway cars road"

2. **Pixabay**
   - URL: https://pixabay.com/videos/search/traffic/
   - License: Free to use
   - Quality: Good (HD available)
   - Search: "traffic vehicles street"

3. **Videvo**
   - URL: https://www.videvo.net/stock-video-footage/traffic/
   - License: Check each video (many are free)
   - Quality: Varies

### Recommended Video Characteristics:

✅ **Duration:** 2-10 minutes  
✅ **Resolution:** 720p or 1080p  
✅ **Format:** MP4, AVI, MOV  
✅ **Frame Rate:** 25-30 FPS  
✅ **Angle:** Elevated view (looking down at traffic)  
✅ **Lighting:** Good daylight or well-lit night  
✅ **Content:** Clear view of multiple vehicles

### Sample Search Terms:

- "highway traffic aerial"
- "road vehicles top view"
- "traffic intersection"
- "busy street cars"
- "motorway traffic flow"

## 📹 Recording Your Own Video

You can also record your own traffic footage:

1. **Camera Position:**
   - Elevated (bridge, building, hill)
   - Looking down at road (30-60° angle)
   - Stable (mount or tripod)

2. **Settings:**
   - Resolution: 1280x720 or 1920x1080
   - Frame rate: 30 FPS
   - Format: MP4 (H.264 codec)

3. **Location:**
   - Safe and legal vantage point
   - Clear view of traffic
   - Good lighting

4. **Duration:**
   - 2-5 minutes sufficient for testing
   - Longer for better analytics

## 🔧 File Format Support

Supported video formats:
- MP4 (Recommended)
- AVI
- MOV
- MKV
- WebM

**Note:** If you encounter codec issues, convert to MP4 using:
```bash
# Using FFmpeg
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
```

## 📊 Expected Performance

| Video Resolution | Processing Speed | Recommended For |
|------------------|------------------|-----------------|
| 640x480 | Very Fast (40+ FPS) | Testing |
| 1280x720 | Fast (25-30 FPS) | Regular use |
| 1920x1080 | Medium (20-25 FPS) | Best quality |
| 3840x2160 | Slow (5-10 FPS) | GPU only |

## ✅ Quick Test

After placing your video:

```bash
# Test if video is readable
python -c "import cv2; cap = cv2.VideoCapture('data/traffic_video.mp4'); print('✓ Video OK' if cap.isOpened() else '✗ Video Error')"
```

## 🚫 Important Notes

1. **Copyright:** Only use royalty-free or your own videos
2. **Privacy:** Blur license plates if sharing publicly
3. **Size:** Keep files under 500MB for easy processing
4. **Backup:** Keep original files before processing

## 📝 Current Files

(This folder is currently empty. Add your video files here.)

---

**Ready to add your first video?** 🎬

1. Download a traffic video from Pexels
2. Rename it to `traffic_video.mp4`
3. Place it in this folder
4. Run: `python main.py`

**That's it!** 🚀
