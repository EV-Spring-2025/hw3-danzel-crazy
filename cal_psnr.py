import os
import cv2
import json
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from tqdm import tqdm

# === CONFIG ===
baseline_folder = "/tmp2/danzel/hw3-danzel-crazy/PhysGaussian/output/plasticine/n_grid_50"  # <-- set your baseline folder path here
output_root = "/tmp2/danzel/hw3-danzel-crazy/PhysGaussian/output/plasticine"               # <-- contains subfolders to compare
save_json_path = "psnr_results.json"

# === CONFIG FOR JELLY ===
baseline_folder_jelly = "/tmp2/danzel/hw3-danzel-crazy/PhysGaussian/output/jelly/baseline"  # <-- set your baseline folder path here
output_root_jelly = "/tmp2/danzel/hw3-danzel-crazy/PhysGaussian/output/jelly"               # <-- contains subfolders to compare
save_json_path_jelly = "psnr_results.json"


# === INIT ===

def calculate_psnr(output_root, baseline_folder, save_json_path):
    """Calculate PSNR for images in subfolders compared to a baseline folder."""
    results = {}

    # === GET SUBFOLDERS EXCEPT BASELINE ===
    subfolders = [
        f for f in os.listdir(output_root)
        if os.path.isdir(os.path.join(output_root, f)) and f != os.path.basename(baseline_folder)
    ]

    # === COMPARE EACH SUBFOLDER WITH BASELINE ===
    for sub in subfolders:
        subfolder_path = os.path.join(output_root, sub)
        psnr_list = []
        if sub != "grid_v_0.7":
            print(f"Skipping {sub} as it is not 'grid_v_1.0'")
            continue  # Skip if the subfolder is not 'grid_v_1.0'

        for filename in tqdm(sorted(os.listdir(baseline_folder))):
            if filename.endswith(".mp4"):
                continue  # Skip any mp4 files, just in case baseline has one too
            
                

            base_img_path = os.path.join(baseline_folder, filename)
            comp_img_path = os.path.join(subfolder_path, filename)

            if not os.path.exists(comp_img_path) or comp_img_path.endswith(".mp4"):
                continue  # Skip if image is missing or is a video file

            base_img = cv2.imread(base_img_path)
            comp_img = cv2.imread(comp_img_path)

            if base_img is None or comp_img is None or base_img.shape != comp_img.shape:
                continue

            score = psnr(base_img, comp_img, data_range=255)
            psnr_list.append(score)

        if psnr_list:
            results[sub] = round(np.mean(psnr_list), 4)
        else:
            results[sub] = None  # or skip this key
    
    # === SAVE TO JSON ===
    json_path = os.path.join(output_root, save_json_path)
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Saved PSNR results to {json_path}")
    
# === RUN FOR PLASTICINE ===
calculate_psnr(output_root, baseline_folder, save_json_path)
# === RUN FOR JELLY ===
calculate_psnr(output_root_jelly, baseline_folder_jelly, save_json_path_jelly)







