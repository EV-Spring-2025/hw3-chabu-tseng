import os
import cv2
import numpy as np
from math import log10
from tqdm import tqdm
import pandas as pd

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    return 20 * log10(255.0 / np.sqrt(mse))

# 路徑設定
baseline_dir = "/tmp2/yctseng/2025spring/ev/hw3-chabu-tseng/output/plasticine/plasticine_baseline_config"
root_dir = "/tmp2/yctseng/2025spring/ev/hw3-chabu-tseng/output/plasticine"
output_csv = "plasticine_psnr_summary.csv"

# 找所有子資料夾
subfolders = [
    f for f in os.listdir(root_dir)
    if os.path.isdir(os.path.join(root_dir, f)) and f != "plasticine_baseline_config"
]

summary = []
all_data = []

for folder in tqdm(subfolders, desc="Processing folders"):
    folder_path = os.path.join(root_dir, folder)
    psnr_list = []

    for i in range(126):
        fname = f"{i:03d}.png"
        baseline_img_path = os.path.join(baseline_dir, fname)
        test_img_path = os.path.join(folder_path, fname)

        if not os.path.isfile(baseline_img_path) or not os.path.isfile(test_img_path):
            continue

        img1 = cv2.imread(baseline_img_path)
        img2 = cv2.imread(test_img_path)

        if img1 is None or img2 is None:
            continue

        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        psnr = calculate_psnr(img1, img2)
        psnr_list.append(psnr)
        all_data.append({
            "folder": folder,
            "frame": i,
            "psnr": psnr
        })

    if psnr_list:
        summary.append({
            "folder": folder,
            "min": np.min(psnr_list),
            "mean": np.mean(psnr_list),
            "max": np.max(psnr_list)
        })

# 輸出 CSV 統計結果
df_summary = pd.DataFrame(summary)
df_summary.to_csv(output_csv, index=False)
print(f"Saved summary to {output_csv}")

