import tarfile
import os
from pathlib import Path
from tqdm import tqdm

def create_class_shards(src_root, out_dir):
    src_root = Path(src_root)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    classes = [d.name for d in src_root.iterdir() if d.is_dir()]
    print(f"Detected classes: {classes}")

    for cls in classes:
        shard_path = out_dir / f"{cls}.tar"
        class_path = src_root / cls
        
        # Get all images in this class (including subfolders for videos)
        image_files = list(class_path.glob("**/*.jpg"))
        
        print(f"\nArchiving {cls}: {len(image_files)} images...")
        
        with tarfile.open(shard_path, "w") as tar:
            for img_path in tqdm(image_files, desc=f"Building {cls}.tar"):
                # arcname preserves 'Class/Video_ID/Frame.jpg'
                # We use relpath from the root so the 'Class' name is the first folder
                arcname = os.path.relpath(img_path, src_root)
                tar.add(img_path, arcname=arcname)

if __name__ == "__main__":
    create_class_shards(src_root="./ff_samples", out_dir="./ff_shards")