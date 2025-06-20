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

# 設定路徑
baseline_dir = "/tmp2/yctseng/2025spring/ev/hw3-chabu-tseng/output/plasticine/plasticine_baseline_config"
root_dir = "/tmp2/yctseng/2025spring/ev/hw3-chabu-tseng/output/plasticine"
output_csv = "plasticine_psnr_full_table.csv"

# 找出子資料夾（排除 baseline）
subfolders = [
    f for f in os.listdir(root_dir)
    if os.path.isdir(os.path.join(root_dir, f)) and f != "plasticine_baseline_config"
]

rows = []

for folder in tqdm(subfolders, desc="Processing folders"):
    folder_path = os.path.join(root_dir, folder)
    psnr_list = []

    for i in range(125):
        fname = f"{i:04d}.png"
        baseline_img_path = os.path.join(baseline_dir, fname)
        test_img_path = os.path.join(folder_path, fname)

        if not os.path.isfile(baseline_img_path) or not os.path.isfile(test_img_path):
            psnr_list.append(np.nan)
            continue

        img1 = cv2.imread(baseline_img_path)
        img2 = cv2.imread(test_img_path)

        if img1 is None or img2 is None:
            psnr_list.append(np.nan)
            continue

        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        psnr = calculate_psnr(img1, img2)
        psnr_list.append(psnr)

    valid_psnrs = [v for v in psnr_list if not np.isnan(v)]

    row = {
        "folder": folder,
        "min": np.min(valid_psnrs),
        "q1": np.percentile(valid_psnrs, 25),
        "mean": np.mean(valid_psnrs),
        "q3": np.percentile(valid_psnrs, 75),
        "max": np.max(valid_psnrs),
    }

    # 加入 frame-wise psnr：frame0 ~ frame125
    for i in range(len(psnr_list)):
        row[f"frame{i}"] = psnr_list[i]

    rows.append(row)

# 儲存成 CSV
df = pd.DataFrame(rows)
df.to_csv(output_csv, index=False)
print(f"Saved PSNR table to {output_csv}")
