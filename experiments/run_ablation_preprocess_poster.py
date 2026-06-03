#!/usr/bin/env python3
"""预处理消融实验（poster_6dof 弱纹理序列，验证去噪和归一化）"""
import os, subprocess, time, csv, re, shutil

CONFIG = "config/davis240c.yaml"
LOAD_UTILS = "utils/load_utils.py"
VAL_SPLIT = "script/splits/davis240c_val.txt"
NETWORK = "/root/DEIO/weights/DEVO.pth"
INPUTDIR = "/root/DEIO/data"
SEQ = "poster_6dof"

MODES = {
    "full":       (True,  "std",  "完整预处理"),
    "no_hotpix":  (False, "std",  "无热像素过滤"),
    "no_norm":    (True,  "none", "无归一化"),
    "minimal":    (False, "none", "仅体素化")
}

def backup(path):
    shutil.copy2(path, path + ".bak")

def restore(path):
    if os.path.exists(path + ".bak"):
        shutil.move(path + ".bak", path)

def modify_hotpixfilter(enable):
    with open(LOAD_UTILS, 'r') as f:
        content = f.read()
    new_val = "True" if enable else "False"
    content = re.sub(r'hotpixfilter\s*=\s*True', f'hotpixfilter = {new_val}', content)
    content = re.sub(r'hotpixfilter\s*=\s*False', f'hotpixfilter = {new_val}', content)
    with open(LOAD_UTILS, 'w') as f:
        f.write(content)

def modify_norm(norm):
    with open(CONFIG, 'r') as f:
        content = f.read()
    content = re.sub(r'NORM:\s*\w+', f'NORM: {norm}', content)
    with open(CONFIG, 'w') as f:
        f.write(content)

def print_current_settings():
    """打印当前 hotpixfilter 和 NORM 的实际值，确保修改生效"""
    with open(LOAD_UTILS, 'r') as f:
        for line in f:
            if 'hotpixfilter' in line:
                print(f"  [当前] {line.strip()}")
    with open(CONFIG, 'r') as f:
        for line in f:
            if line.startswith('NORM:'):
                print(f"  [当前] {line.strip()}")

def run_deio():
    cmd = [
        "python", "script/eval_deio/davis240c.py",
        "--inputdir", INPUTDIR,
        "--val_split", VAL_SPLIT,
        "--config", CONFIG,
        "--network", NETWORK,
        "--enable_event", "--trials", "1", "--save_trajectory"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r'rmse\s+([\d.]+)', result.stdout)
    return float(m.group(1)) if m else None

backup(LOAD_UTILS)
backup(CONFIG)

with open(VAL_SPLIT, 'w') as f:
    f.write(SEQ + "\n")

results = []
try:
    for mode, (hotpix, norm, desc) in MODES.items():
        print(f"\n===== {desc} =====")
        modify_hotpixfilter(hotpix)
        modify_norm(norm)
        print_current_settings()
        start = time.time()
        rmse = run_deio()
        elapsed = time.time() - start
        print(f"  ATE = {rmse:.4f} m, 耗时 = {elapsed:.0f}s")
        results.append([desc, rmse, elapsed])
finally:
    restore(LOAD_UTILS)
    restore(CONFIG)
    os.makedirs("results/ablation_preprocess", exist_ok=True)
    with open("results/ablation_preprocess/results_poster.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Mode", "ATE_RMSE", "Elapsed_sec"])
        writer.writerows(results)
    print("\nposter_6dof 预处理消融结果已保存")
