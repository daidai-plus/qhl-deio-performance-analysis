#!/usr/bin/env python3
"""Patch Size 消融实验：patch_size=1/3/5/7 对性能的影响"""
import os, sys, argparse, time, csv, re, shutil

PATCH_VALUES = [1, 3, 5, 7]
SOURCE_FILE = "devo/enet.py"
BACKUP_FILE = "devo/enet.py.bak"
BASE_SCRIPT = "script/eval_deio/davis240c.py"
OUTPUT_CSV = "results/ablation_patch/results.csv"

def backup_source():
    if not os.path.exists(BACKUP_FILE):
        shutil.copy2(SOURCE_FILE, BACKUP_FILE)
        print(f"已备份 {SOURCE_FILE}")

def restore_source():
    if os.path.exists(BACKUP_FILE):
        shutil.copy2(BACKUP_FILE, SOURCE_FILE)
        os.remove(BACKUP_FILE)
        print(f"已恢复原始文件")

def modify_patch_size(new_value):
    with open(SOURCE_FILE, 'r') as f:
        content = f.read()
    pattern = r'(def __init__\(self, args, patch_size\s*=\s*)\d+'
    modified, count = re.subn(pattern, rf'\g<1>{new_value}', content)
    if count == 0:
        raise RuntimeError("未找到 patch_size 定义！")
    with open(SOURCE_FILE, 'w') as f:
        f.write(modified)
    print(f"已将 patch_size 修改为 {new_value}")

def run_deio_for_patch(p, args):
    print(f"\n===== 测试 patch_size = {p} =====")
    modify_patch_size(p)
    cmd = [
        "python", BASE_SCRIPT,
        "--inputdir", args.inputdir,
        "--network", args.network,
        "--config", args.config,
        "--val_split", args.val_split,
        "--trials", "1",
        "--stride", str(args.stride),
        "--enable_event",
        "--save_trajectory"
    ]
    start = time.time()
    ret = os.system(" ".join(cmd))
    elapsed = time.time() - start
    return [p, None, elapsed]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputdir', default="/root/autodl-tmp/datasets/davis240c")
    parser.add_argument('--network', default="weights/DEVO.pth")
    parser.add_argument('--config', default="config/default_devo.yaml")
    parser.add_argument('--val_split', default="script/splits/davis240c_val.txt")
    parser.add_argument('--stride', type=int, default=1)
    args = parser.parse_args()

    backup_source()
    results = []
    try:
        for p in PATCH_VALUES:
            results.append(run_deio_for_patch(p, args))
    finally:
        restore_source()
        os.makedirs("results/ablation_patch", exist_ok=True)
        with open(OUTPUT_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Patch_Size", "ATE_RMSE", "Elapsed_sec"])
            writer.writerows(results)
        print(f"\n结果已保存至 {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
