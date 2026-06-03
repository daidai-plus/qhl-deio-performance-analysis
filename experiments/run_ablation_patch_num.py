#!/usr/bin/env python3
"""Patch 数量消融：PATCHES_PER_FRAME = 48/96/128/160"""
import os, subprocess, time, csv, re

PATCH_VALUES = [48, 96, 128, 160]
CONFIG_FILE = "config/davis240c.yaml"
BACKUP_FILE = "config/davis240c.yaml.bak"
VAL_SPLIT = "script/splits/davis240c_val.txt"

def backup_config():
    if not os.path.exists(BACKUP_FILE):
        subprocess.run(["cp", CONFIG_FILE, BACKUP_FILE])
        print(f"已备份 {CONFIG_FILE}")

def restore_config():
    subprocess.run(["cp", BACKUP_FILE, CONFIG_FILE])
    os.remove(BACKUP_FILE)
    print("已恢复配置文件")

def modify_patches(num):
    with open(CONFIG_FILE, 'r') as f:
        content = f.read()
    content = re.sub(r'PATCHES_PER_FRAME:\s*\d+', f'PATCHES_PER_FRAME: {num}', content)
    with open(CONFIG_FILE, 'w') as f:
        f.write(content)

def run_experiment(num):
    print(f"\n===== PATCHES_PER_FRAME = {num} =====")
    modify_patches(num)
    cmd = [
        "python", "script/eval_deio/davis240c.py",
        "--inputdir", "/root/autodl-tmp/datasets/davis240c",
        "--val_split", VAL_SPLIT,
        "--config", CONFIG_FILE,
        "--network", "/root/DEIO/weights/DEVO.pth",
        "--enable_event", "--trials", "1", "--save_trajectory", "--plot"
    ]
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start

    # 提取 Sim(3) ATE RMSE
    match = re.search(r'rmse\s+([\d.]+)', result.stdout)
    rmse = float(match.group(1)) if match else None
    print(f"PATCHES={num}: ATE={rmse}, 耗时={elapsed:.0f}s")
    return [num, rmse, elapsed]

# 写入验证集
with open(VAL_SPLIT, 'w') as f:
    f.write("boxes_6dof\n")

backup_config()
results = []
try:
    for p in PATCH_VALUES:
        results.append(run_experiment(p))
finally:
    restore_config()
    os.makedirs("results/ablation_patch_num", exist_ok=True)
    with open("results/ablation_patch_num/results.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["PATCHES_PER_FRAME", "ATE_RMSE", "Elapsed_sec"])
        writer.writerows(results)
    print("\n结果已保存到 results/ablation_patch_num/results.csv")
