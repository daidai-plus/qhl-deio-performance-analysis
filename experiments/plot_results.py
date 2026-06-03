#!/usr/bin/env python3
"""实验结果可视化：生成消融曲线和对比图"""
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def plot_ablation_b(csv_path="results/ablation_b/results.csv"):
    """体素层数-ATE/FPS双轴曲线"""
    if not os.path.exists(csv_path):
        print(f"文件不存在: {csv_path}")
        return
    
    b_vals, ate_vals, fps_vals = [], [], []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            b_vals.append(int(row['Nbins']))
            ate_vals.append(float(row['ATE_RMSE']) if row['ATE_RMSE'] else np.nan)
            fps_vals.append(float(row['Elapsed_sec']) if row['Elapsed_sec'] else np.nan)
    
    fig, ax1 = plt.subplots(figsize=(8,5))
    ax1.set_xlabel('体素层数 B')
    ax1.set_ylabel('ATE RMSE (m)', color='tab:blue')
    ax1.plot(b_vals, ate_vals, 'b-o', label='ATE')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('耗时 (s)', color='tab:red')
    ax2.plot(b_vals, fps_vals, 'r-s', label='耗时')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    plt.title('体素层数对精度和速度的影响')
    fig.tight_layout()
    os.makedirs('results/ablation_b', exist_ok=True)
    plt.savefig('results/ablation_b/ablation_b_curve.png', dpi=150)
    print('体素层数曲线已保存到 results/ablation_b/ablation_b_curve.png')

def plot_imu_ablation(csv_path="results/ablation_imu/results.csv"):
    """IMU消融对比柱状图"""
    if not os.path.exists(csv_path):
        print(f"文件不存在: {csv_path}")
        return
    
    modes, ate_vals = [], []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            modes.append(row['Mode'])
            ate_vals.append(float(row['ATE_RMSE']) if row['ATE_RMSE'] else 0)
    
    plt.figure(figsize=(6,5))
    colors = ['tab:blue', 'tab:orange']
    plt.bar(modes, ate_vals, color=colors)
    plt.ylabel('ATE RMSE (m)')
    plt.title('IMU融合消融：DEIO vs DEVO')
    for i, v in enumerate(ate_vals):
        plt.text(i, v + 0.01, f'{v:.3f}m', ha='center', fontweight='bold')
    os.makedirs('results/ablation_imu', exist_ok=True)
    plt.savefig('results/ablation_imu/imu_ablation_bar.png', dpi=150)
    print('IMU消融图已保存到 results/ablation_imu/imu_ablation_bar.png')

def plot_all():
    """生成所有图表"""
    print("生成可视化图表...")
    plot_ablation_b()
    plot_imu_ablation()
    print("完成！")

if __name__ == "__main__":
    plot_all()
