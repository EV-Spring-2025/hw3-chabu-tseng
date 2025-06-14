import pandas as pd
import matplotlib.pyplot as plt
import os

# 載入資料
df = pd.read_csv("plasticine_psnr_full_table.csv")

# 設定要分組的 prefix
groups = {
    "substep": "plasticine_substep",
    "grid_v_damping": "plasticine_grid_v_damping",
    "softening": "plasticine_softening",
    "n_grid": "plasticine_n_grid"
}

# frame 欄位名稱
frame_cols = [f"frame{i}" for i in range(125)]

# 輸出圖的資料夾
output_dir = "psnr_lineplots"
os.makedirs(output_dir, exist_ok=True)

# 為每組畫圖
for group_name, prefix in groups.items():
    group_df = df[df["folder"].str.startswith(prefix)]

    plt.figure(figsize=(12, 6))

    for _, row in group_df.iterrows():
        plt.plot(range(len(frame_cols)), row[frame_cols], label=row["folder"], linewidth=1)

    plt.title(f"Frame-wise PSNR Comparison – {group_name}")
    plt.xlabel("Frame")
    plt.ylabel("PSNR (dB)")
    plt.legend(fontsize="small", loc="lower right")
    plt.tight_layout()

    # 儲存圖
    plot_path = os.path.join(output_dir, f"{group_name}_psnr_lineplot.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved plot: {plot_path}")
