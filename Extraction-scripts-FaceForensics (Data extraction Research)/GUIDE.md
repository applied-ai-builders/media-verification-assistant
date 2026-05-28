# FaceForensics++ Frame Extraction & Sharding Pipeline

This guide explains how to use the two scripts in this directory to extract frames from FaceForensics++ videos and organize them into shards.

## Overview

The pipeline consists of two stages:

1. **Frame Extraction** (`extractor.py`) - Extract individual frames from MP4 videos
2. **Frame Sharding** (`sharding.py`) - Organize extracted frames into tar archives

---

## Required Folder Structure

Before running the scripts, ensure your directory structure looks like this:

```
.
├── extractor.py
├── sharding.py
├── deepfake_dataset/                    # Input video files (must exist)
│   └── FaceForensics++_C23/
│       ├── DeepFakeDetection/           # Video files (.mp4)
│       ├── Deepfakes/                   # Video files (.mp4)
│       ├── Face2Face/                   # Video files (.mp4)
│       ├── FaceShifter/                 # Video files (.mp4)
│       ├── FaceSwap/                    # Video files (.mp4)
│       ├── NeuralTextures/              # Video files (.mp4)
│       └── original/                    # Video files (.mp4)
├── ff_samples/                          # Output: Extracted frames (created by extractor.py)
│   ├── DeepFakeDetection/
│   ├── Deepfakes/
│   ├── Face2Face/
│   ├── FaceShifter/
│   ├── FaceSwap/
│   ├── NeuralTextures/
│   └── original/
└── ff_shards/                           # Output: Tar archives (created by sharding.py)
    ├── DeepFakeDetection.tar
    ├── Deepfakes.tar
    ├── Face2Face.tar
    ├── FaceShifter.tar
    ├── FaceSwap.tar
    ├── NeuralTextures.tar
    └── original.tar
```

---

## Prerequisites

Install required Python packages:

```bash
pip install opencv-python numpy tqdm
```

---

## Step-by-Step Usage

### Step 1: Extract Frames from Videos

```bash
python extractor.py
```

**What this does:**
- Scans the `deepfake_dataset/FaceForensics++_C23/` directory for all `.mp4` files
- Extracts frames at a **2 FPS sample rate** (adjustable in the code)
- Saves extracted frames as compressed JPG files (quality=90) to `ff_samples/`
- Organizes frames by class and then by video name

**Configuration options** (edit in `extractor.py`):
- `sample_rate=2`: Number of frames to extract per second (2 means 1 frame every 0.5 seconds)
- `quality=90`: JPEG compression quality (0-100, higher = better quality, larger file size)

**Output structure per class:**
```
ff_samples/DeepFakeDetection/
├── video_001/
│   ├── video_001_f0.jpg
│   ├── video_001_f15.jpg
│   ├── video_001_f30.jpg
│   └── ...
├── video_002/
│   ├── video_002_f0.jpg
│   └── ...
└── video_003/
    └── ...
```

**Performance tips:**
- Uses multiprocessing for parallel video extraction
- Automatically skips corrupt videos
- Progress bar shows real-time extraction status

---

### Step 2: Create Frame Shards

After frame extraction completes, create tar archives:

```bash
python sharding.py
```

**What this does:**
- Reads all extracted frames from `ff_samples/`
- Creates a single `.tar` file for each class
- Preserves the internal directory structure (class → video → frames)
- Saves shards to `ff_shards/`

**Output files:**
```
ff_shards/
├── DeepFakeDetection.tar    (~5-20 GB each, depending on class)
├── Deepfakes.tar
├── Face2Face.tar
├── FaceShifter.tar
├── FaceSwap.tar
├── NeuralTextures.tar
└── original.tar
```

**Notes:**
- Each tar file preserves the internal folder structure for easy extraction
- Tar format is uncompressed to avoid CPU overhead
- Progress bar shows archive creation progress

---

## Complete Workflow Example

### 1. Verify folder structure
```bash
ls -la deepfake_dataset/FaceForensics++_C23/
# Should show: DeepFakeDetection, Deepfakes, Face2Face, FaceShifter, FaceSwap, NeuralTextures, original
```

### 2. Run frame extraction
```bash
python extractor.py
# This will take 1-2 hours depending on your CPU and number of videos
```

### 3. Check extracted frames
```bash
ls ff_samples/
du -sh ff_samples/  # Check total size
```

### 4. Create shards
```bash
python sharding.py
# This will take 30 minutes to 2 hours depending on total frame count
```

### 5. Verify shards
```bash
ls -lh ff_shards/
du -sh ff_shards/  # Check total shard size
```

---

## Troubleshooting

### Issue: "No module named 'cv2'"
```bash
pip install opencv-python
```

### Issue: Extraction is very slow
- Check CPU usage: `top` or `htop` on Linux/Mac
- Reduce number of parallel workers (edit `ProcessPoolExecutor()` in `extractor.py`)
- Move `ff_samples/` to faster storage if using network drives

### Issue: Out of disk space
- Enable tar compression in `sharding.py`:
  ```python
  with tarfile.open(shard_path, "w:gz") as tar:  # Compressed tar
  ```
  This reduces file size by ~40% but increases creation time

---

## Performance Metrics

Typical processing times on a modern system:

| Stage | Input | Output Size | Time |
|-------|-------|-------------|------|
| Extraction | Full FaceForensics++ (7 classes) | ~150-200 GB frames | 2-4 hours |
| Sharding | 150-200 GB frames | ~120-180 GB tars | 1-2 hours |

---

## Advanced Options

### Adjusting Frame Extraction Rate

Edit `extractor.py` line with `sample_rate`:
```python
worker_func = partial(extract_frames_from_video, output_root=output_dir, sample_rate=1)
# sample_rate=1: 1 frame per second
# sample_rate=2: 2 frames per second (default)
# sample_rate=4: 4 frames per second (more storage needed)
```

### Adjusting JPEG Quality

Edit `extractor.py` line with `IMWRITE_JPEG_QUALITY`:
```python
cv2.imwrite(str(file_path), image, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
# 75 = medium quality (smaller files)
# 90 = high quality (larger files, default)
# 95 = very high quality (largest files)
```

### Using Compressed Tar Files

Edit `sharding.py` to compress shards:
```python
with tarfile.open(shard_path, "w:gz") as tar:  # Gzip compression
# or "w:bz2" for bzip2 compression (slower but better compression)
```

---

## Expected Output

After completing all steps, you'll have:

1. **Local frame extraction** (~150-200 GB):
   - `ff_samples/` with 7 subdirectories (one per class)
   - Each containing extracted JPG frames organized by video

2. **Local tar shards** (~120-180 GB):
   - `ff_shards/` with 7 `.tar` files (one per class)
   - Each tar file contains all frames for that class

---

## License & Attribution

This pipeline processes FaceForensics++ dataset. Please ensure compliance with FaceForensics++ research use policies and appropriate citation.

---

## Questions or Issues?

- Check script variable definitions for configuration options
- Enable verbose output by adding `print()` statements
- Monitor progress with the provided `tqdm` progress bars