# DEIO 性能分析与实验复现

本仓库是本科毕业设计《基于深度学习的事件惯性里程计性能分析与研究》的实验代码。

## 实验清单

| 实验 | 脚本 | 说明 |
|------|------|------|
| 体素层数消融 | `run_ablation_b.py` | B=5/10/15/20 |
| IMU 融合消融 | `run_ablation_imu.py` | DEIO vs DEVO |
| Patch Size 消融 | `run_ablation_patch.py` | patch_size=1/3/5/7 |
| 预处理消融 | `run_ablation_preprocess.py` | 完整/无热像素/无增强/无预处理 |

## 项目结构
```bash
~/DEIO/
├── experiments/ # 实验脚本目录
│ ├── run_ablation_b.py # 体素层数消融
│ ├── run_ablation_patch.py # Patch Size 消融
│ ├── run_ablation_imu.py # IMU 约束消融
│ ├── run_ablation_preprocess.py # 输入表征消融
│ └── README.md # 本文件
├── results/ # 结果输出目录
│ ├── ablation_b/
│ ├── ablation_patch/
│ ├── ablation_imu/
│ └── ablation_preprocess/
├── config/
│ └── default_devo.yaml # 基准配置
└── datasets/ → /root/autodl-tmp/datasets/ # 数据盘软链接
```
## 运行方式

```bash
conda activate deio
cd ~/DEIO
python experiments/run_ablation_b.py
python experiments/run_ablation_imu.py
python experiments/run_ablation_patch.py
python experiments/run_ablation_preprocess.py

## 环境配置
Python 3.10, PyTorch 2.3.1, CUDA 11.8

GTSAM 4.2a7 (源码编译 + Python 绑定)

evo 评估工具

##作者
GitHub: daidai-plus
```
