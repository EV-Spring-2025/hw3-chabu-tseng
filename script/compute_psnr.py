import os
import cv2
import numpy as np
import argparse
from math import log10
from tqdm import tqdm

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    return 20 * log10(255.0 / np.sqrt(mse))

def compute_psnr_folder(folder1, folder2):
    files1 = sorted([f for f in os.listdir(folder1) if f.endswith(".png")])
    files2 = sorted([f for f in os.listdir(folder2) if f.endswith(".png")])

    assert files1 == files2, "Two folders must contain matching PNG filenames."

    psnr_values = []

    for fname in tqdm(files1):
        img1_path = os.path.join(folder1, fname)
        img2_path = os.path.join(folder2, fname)

        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        if img1 is None or img2 is None:
            print(f"Failed to read image: {fname}")
            continue

        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        psnr = calculate_psnr(img1, img2)
        psnr_values.append(psnr)

    average_psnr = sum(psnr_values) / len(psnr_values)
    print(f"\nAverage PSNR: {average_psnr:.2f} dB")
    return psnr_values, average_psnr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute PSNR between two image folders")
    parser.add_argument('--folder_path1', type=str, required=True, help='Path to first image folder (baseline)')
    parser.add_argument('--folder_path2', type=str, required=True, help='Path to second image folder (comparison)')

    args = parser.parse_args()
    compute_psnr_folder(args.folder_path1, args.folder_path2)
