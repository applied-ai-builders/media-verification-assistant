import os
import cv2
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from tqdm import tqdm
from functools import partial

def extract_frames_from_video(video_path, output_root, sample_rate=2):
    """
    video_path: Path to the .mp4
    output_root: Where to save the images
    sample_rate: Frames to extract per second of video
    """
    try:
        vidcap = cv2.VideoCapture(str(video_path))
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        if fps == 0: return # Skip corrupt videos
        
        # Calculate the interval (e.g., if 30fps and we want 2fps, interval is 15)
        interval = max(1, round(fps / sample_rate))
        
        # Create a specific folder for this video's frames
        video_name = video_path.stem
        output_dir = Path(output_root) / video_name
        output_dir.mkdir(parents=True, exist_ok=True)

        count = 0
        saved_count = 0
        success = True
        while success:
            success, image = vidcap.read()
            if success and count % interval == 0:
                # Save as JPG (compressed) to save space
                file_path = output_dir / f"{video_name}_f{count}.jpg"
                cv2.imwrite(str(file_path), image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                saved_count += 1
            count += 1
        vidcap.release()
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
        
def run_extraction():
    # Assuming your videos are organized like this:
    # deepfake_dataset/
    #   ├── FaceForensics++_C23/
    #   │   ├── DeepFakeDetection/
    #   │   ├── FaceSwap/
    #   │   └── original/

  base_dir=Path('deepfake_dataset/FaceForensics++_C23')
    # Check the directory structure
  classes = ['DeepFakeDetection',
  'FaceSwap',
  'original',
  'Deepfakes',
  'Face2Face',
  'NeuralTextures',
  'FaceShifter']

  for cls in classes:
      video_dir=base_dir / cls
      output_dir=Path('./ff_samples') / cls
      output_dir.mkdir(parents=True, exist_ok=True)
      video_files = list(video_dir.glob('*.mp4'))
      print(f"Class: {cls} | Videos found: {len(video_files)}")
      
      worker_func = partial(extract_frames_from_video, output_root=output_dir, sample_rate=2)
      
      with ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(worker_func, video_files), total=len(video_files), desc=f"Processing {cls}")) 
        
if __name__ == "__main__":
    run_extraction()