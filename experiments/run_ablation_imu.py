#!/usr/bin/env python3
"""IMU 消融实验：DEIO vs DEVO"""
import os, sys, argparse, time, csv

BASE_SCRIPT = "script/eval_deio/davis240c.py"
OUTPUT_CSV = "results/ablation_imu/results.csv"
MODES = [("DEIO_IMU_On", "True"), ("DEVO_IMU_Off", "False")]

def run_mode(name, imu_flag, args):
    print(f"\n===== 测试模式: {name} =====")
    cmd = [
        "python", BASE_SCRIPT,
        "--inputdir", args.inputdir,
        "--network", args.network,
        "--config", args.config,
        "--val_split", args.val_split,
        "--trials", "1", "--stride", str(args.stride),
        "--enable_event", "--save_trajectory",
        "--opts", f"ENALBE_IMU {imu_flag}"
    ]
    start = time.time()
    os.system(" ".join(cmd))
    elapsed = time.time() - start
    return [name, None, None, elapsed]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputdir', default="/root/autodl-tmp/datasets/davis240c")
    parser.add_argument('--network', default="weights/DEVO.pth")
    parser.add_argument('--config', default="config/default_devo.yaml")
    parser.add_argument('--val_split', default="script/splits/davis240c_val.txt")
    parser.add_argument('--stride', type=int, default=1)
    args = parser.parse_args()
    results = [run_mode(name, flag, args) for name, flag in MODES]
    os.makedirs("results/ablation_imu", exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Mode", "ATE_RMSE", "Scale_Drift_%", "Elapsed_sec"])
        writer.writerows(results)
    print(f"\n结果已保存至 {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
