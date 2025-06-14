import os
from moviepy import VideoFileClip

input_root = "/tmp2/yctseng/2025spring/ev/hw3-chabu-tseng/output/plasticine"
output_dir = "/tmp2/yctseng/2025spring/ev/hw3-chabu-tseng/resource"

os.makedirs(output_dir, exist_ok=True)

# 遍歷所有子資料夾
for subfolder in os.listdir(input_root):
    subfolder_path = os.path.join(input_root, subfolder)
    if not os.path.isdir(subfolder_path):
        continue

    mp4_path = os.path.join(subfolder_path, "output.mp4")
    if not os.path.isfile(mp4_path):
        print(f"[Skip] No output.mp4 in {subfolder}")
        continue

    output_gif_path = os.path.join(output_dir, f"{subfolder}.gif")

    try:
        print(f"Converting: {mp4_path} → {output_gif_path}")
        clip = VideoFileClip(mp4_path)
        clip.write_gif(output_gif_path, fps=clip.fps)
        clip.close()
    except Exception as e:
        print(f"[Error] Failed to convert {mp4_path}: {e}")

print("✅ All conversions completed.")
