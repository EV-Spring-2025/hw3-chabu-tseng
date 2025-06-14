import os
import json
from copy import deepcopy

BASE_CONFIG_PATH = os.path.expanduser("/tmp2/yctseng/2025spring/ev/hw3-chabu-tseng/config/sand/sand_baseline_config.json")
OUTPUT_DIR = os.path.expanduser("/tmp2/yctseng/2025spring/ev/hw3-chabu-tseng/config/sand")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SWEEP_PARAMETERS = {
    "n_grid": [200, 160, 128, 96, 64, 48],
    "substep_dt": [5e-5, 3e-5, 2e-5, 1e-5, 5e-6],
    "grid_v_damping_scale": [0.1, 0.25, 0.5, 0.75, 0.95, 0.9999],
    "softening": [1e-5, 5e-3, 1e-2, 2e-2, 5e-1]
}

with open(BASE_CONFIG_PATH, "r") as f:
    base_config = json.load(f)

for param, values in SWEEP_PARAMETERS.items():
    for val in values:
        config = deepcopy(base_config)
        config[param] = val

        val_str = str(val).replace('.', 'p').replace('-', 'm')
        filename = f"sand_{param}{val_str}.json"

        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"Saved: {filename}")
