import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 載入資料
df = pd.read_csv("plasticine_psnr_full_table.csv")

# 設定 prefix 分組規則
prefix_groups = {
    "substep": "plasticine_substep",
    "grid_v_damping": "plasticine_grid_v_damping",
    "softening": "plasticine_softening",
    "n_grid": "plasticine_n_grid"
}

# frame 欄位
frame_cols = [f"frame{i}" for i in range(125)]

# 建立輸出資料夾
output_dir = "psnr_boxplots"
os.makedirs(output_dir, exist_ok=True)

# 繪圖
for group_name, prefix in prefix_groups.items():
    group_df = df[df["folder"].str.startswith(prefix)]

    # 將每列展平成 long format
    melted = group_df.melt(id_vars=["folder"], value_vars=frame_cols,
                           var_name="frame", value_name="psnr")

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=melted, x="folder", y="psnr")
    plt.xticks(rotation=45, ha='right')
    plt.title(f"PSNR Distribution per Setting – {group_name}")
    plt.xlabel("Folder (Setting)")
    plt.ylabel("PSNR (dB)")
    plt.tight_layout()

    save_path = os.path.join(output_dir, f"{group_name}_boxplot.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved boxplot: {save_path}")
