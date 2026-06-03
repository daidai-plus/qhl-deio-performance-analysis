#!/usr/bin/env python3
"""DEIO 毕设实验 - 全部结果汇总与图表生成"""
import numpy as np, os, csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

# ==================== 实验数据 ====================
# 三系统 ATE
ate_data = {
    "Traditional VIO": {"dynamic_6dof": 0.324, "poster_6dof": 0.350, "boxes_6dof": 0.310},
    "DEVO":            {"dynamic_6dof": 0.062, "poster_6dof": 0.538, "boxes_6dof": 0.755},
    "DEIO":            {"dynamic_6dof": 0.035, "poster_6dof": 0.063, "boxes_6dof": 0.064}
}
# 三系统 RPE
rpe_data = {
    "Traditional VIO": {"dynamic_6dof": 0.100, "poster_6dof": 0.120, "boxes_6dof": 0.110},
    "DEVO":            {"dynamic_6dof": 0.027, "poster_6dof": 0.081, "boxes_6dof": 0.108},
    "DEIO":            {"dynamic_6dof": 0.033, "poster_6dof": 0.031, "boxes_6dof": 0.033}
}
# Patch Size 消融（三序列）
patch_size_data = {
    "dynamic_6dof": [0.0353, 0.0350, 0.0388, 0.0402],
    "poster_6dof":  [0.0518, 0.0826, 0.0634, 0.0669],
    "boxes_6dof":   [0.0450, 0.0420, 0.0460, 0.0500]
}
patch_sizes = [1, 3, 5, 7]
# Patch 数量消融（三序列）
patch_nums = [48, 96, 128, 160]
patch_num_data = {
    "dynamic_6dof": [0.070, 0.069, 0.071, 0.077],
    "poster_6dof":  [0.062, 0.054, 0.059, 0.064],
    "boxes_6dof":   [0.092, 0.069, 0.064, 0.076]
}
# 预处理消融（双序列）
preprocess_modes = ['Full', 'No HotPix', 'No Norm', 'Voxel Only']
preprocess_data = {
    "dynamic_6dof": [0.0358, 0.0348, 0.0361, 0.0343],
    "poster_6dof":  [0.0518, 0.0826, 0.0634, 0.0669]
}
# 模块耗时
timing_modules = ['Input Build', 'Frontend Inference', 'IMU Preint.', 'Backend Opt.', 'Logging']
timing_values = [2, 59, 1, 20, 3]
timing_colors = ['#99ff99', '#66b3ff', '#ffff99', '#ffcc99', '#c2c2f0']

def save_csv(filename, headers, rows):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, filename), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(headers); w.writerows(rows)

def plot_ate_comparison():
    scenes = ['dynamic_6dof', 'poster_6dof', 'boxes_6dof']
    x = range(len(scenes)); w = 0.25
    fig, ax = plt.subplots(figsize=(12,7))
    ax.bar([i-w for i in x], [ate_data["Traditional VIO"][s] for s in scenes], w, label='Traditional VIO', color='gray')
    ax.bar(x, [ate_data["DEVO"][s] for s in scenes], w, label='DEVO', color='tab:orange')
    ax.bar([i+w for i in x], [ate_data["DEIO"][s] for s in scenes], w, label='DEIO', color='tab:blue')
    ax.set_ylabel('ATE RMSE (m)'); ax.set_title('Three-system ATE Comparison')
    ax.set_xticks(x); ax.set_xticklabels(scenes); ax.legend()
    for bars in ax.containers:
        for bar in bars: ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01, f'{bar.get_height():.3f}', ha='center', fontsize=8, fontweight='bold')
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_DIR, 'final_ate_comparison.png'), dpi=200)

def plot_rpe_comparison():
    scenes = ['dynamic_6dof', 'poster_6dof', 'boxes_6dof']
    x = range(len(scenes)); w = 0.25
    fig, ax = plt.subplots(figsize=(12,7))
    ax.bar([i-w for i in x], [rpe_data["Traditional VIO"][s] for s in scenes], w, label='Traditional VIO', color='gray')
    ax.bar(x, [rpe_data["DEVO"][s] for s in scenes], w, label='DEVO', color='tab:orange')
    ax.bar([i+w for i in x], [rpe_data["DEIO"][s] for s in scenes], w, label='DEIO', color='tab:blue')
    ax.set_ylabel('RPE RMSE (m)'); ax.set_title('Three-system RPE Comparison')
    ax.set_xticks(x); ax.set_xticklabels(scenes); ax.legend()
    for bars in ax.containers:
        for bar in bars: ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.002, f'{bar.get_height():.3f}', ha='center', fontsize=8, fontweight='bold')
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_DIR, 'final_rpe_comparison.png'), dpi=200)

def plot_patch_size():
    fig, ax = plt.subplots(figsize=(10,6))
    for seq, vals in patch_size_data.items():
        ax.plot(patch_sizes, vals, 'o-', linewidth=2, markersize=8, label=seq)
    ax.set_xlabel('Patch Size'); ax.set_ylabel('ATE RMSE (m)')
    ax.set_title('Patch Size Ablation'); ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_DIR, 'patch_size_all_seq.png'), dpi=150)

def plot_patch_num():
    fig, ax = plt.subplots(figsize=(10,6))
    for seq, vals in patch_num_data.items():
        ax.plot(patch_nums, vals, 'o-', linewidth=2, markersize=8, label=seq)
    ax.set_xlabel('Number of Patches'); ax.set_ylabel('ATE RMSE (m)')
    ax.set_title('Patch Number Ablation'); ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_DIR, 'patch_num_all_seq.png'), dpi=150)

def plot_preprocess():
    x = range(len(preprocess_modes)); w = 0.35
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar([i-w/2 for i in x], preprocess_data["dynamic_6dof"], w, label='dynamic_6dof', color='tab:blue')
    ax.bar([i+w/2 for i in x], preprocess_data["poster_6dof"], w, label='poster_6dof', color='tab:orange')
    ax.set_ylabel('ATE RMSE (m)'); ax.set_title('Preprocessing Ablation')
    ax.set_xticks(x); ax.set_xticklabels(preprocess_modes); ax.legend()
    for bars in ax.containers:
        for bar in bars: ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.001, f'{bar.get_height():.4f}', ha='center', fontsize=9, fontweight='bold')
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_DIR, 'preprocess_comparison.png'), dpi=150)

def plot_timing_pie():
    fig, ax = plt.subplots(figsize=(10,8))
    wedges, _ = ax.pie(timing_values, labels=None, colors=timing_colors, startangle=90,
                        pctdistance=0.7, wedgeprops=dict(width=0.4, edgecolor='white'))
    total = sum(timing_values)
    for i, (wedge, t) in enumerate(zip(wedges, timing_values)):
        ang = (wedge.theta2 - wedge.theta1)/2. + wedge.theta1
        rad = np.deg2rad(ang)
        x, y = 1.5*np.cos(rad), 1.5*np.sin(rad)
        pct = t/total*100
        ax.annotate(f'{timing_modules[i]}\n({t}s, {pct:.1f}%)', xy=(np.cos(rad), np.sin(rad)),
                     xytext=(x,y), ha='left' if x>0 else 'right', fontsize=11, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.9),
                     arrowprops=dict(arrowstyle='-', color='gray', lw=1.5))
    ax.set_title('DEIO Module Time Distribution (dynamic_6dof, 1269 frames)', fontsize=14, fontweight='bold')
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_DIR, 'module_timing_pie.png'), dpi=200)

def plot_robustness():
    scenes = ['dynamic_6dof\n(high speed)', 'boxes_6dof\n(standard)', 'poster_6dof\n(weak texture)']
    ate = [0.035, 0.064, 0.063]
    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(range(3), ate, color=['tab:blue','tab:green','tab:orange'], width=0.5)
    ax.set_ylabel('ATE RMSE (m)'); ax.set_title('DEIO Robustness Across Three Scenes')
    ax.set_xticks(range(3)); ax.set_xticklabels(scenes)
    for i,v in enumerate(ate): ax.text(i, v+0.001, f'{v:.3f}m', ha='center', fontweight='bold')
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_DIR, 'robustness.png'), dpi=150)

if __name__ == '__main__':
    print("Generating all summary charts...")
    plot_ate_comparison();    print("  ATE comparison done")
    plot_rpe_comparison();    print("  RPE comparison done")
    plot_patch_size();        print("  Patch Size done")
    plot_patch_num();         print("  Patch Number done")
    plot_preprocess();        print("  Preprocessing done")
    plot_timing_pie();        print("  Timing pie done")
    plot_robustness();        print("  Robustness done")
    print("All charts saved to results/")
