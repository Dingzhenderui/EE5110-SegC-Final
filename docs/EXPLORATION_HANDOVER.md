# 拓展实验运行与边界

当前入口：`exploration_main.py --case NAME`，默认无界面。观看交互演示用`demo_viewer.py`。唯一报告见[综合报告](../output/pdf/EE5110_Final_Report.pdf)，运行/打包见[交付说明](FINAL_DELIVERY.md)。

| 研究方向 | case | 正式结果 |
|---|---|---|
| 强杂乱/遮挡 | `crowding_single` / `crowding_active` | 5/6 / 3/6 |
| 真软体 | `soft_fixed` / `soft_adaptive` | 2/6 / 6/6 |
| 被动铰接件 | `articulated` | 6/6 |
| 未见程序形状 | `novel_prior` / `novel_points` | 11/12 / 11/12 |
| 接触反馈 | `force_fixed` / `force_adaptive` | 10/12 / 12/12 |
| 指定闭合故障恢复 | `recovery_single` / `recovery_retry` | 0/6 / 6/6 |
| 受损点云 | `sensor_single` / `sensor_raw_fusion` / `sensor_robust` | 6/12 / 1/12 / 9/12 |

```powershell
.venv\Scripts\python exploration_main.py --case soft_adaptive --trials 1 --seed 43 --require-all-success
.venv\Scripts\python exploration_main.py --case recovery_retry --trials 1 --seed 43 --require-all-success
.venv\Scripts\python scripts/benchmark_exploration.py --output outputs/new_exploration
.venv\Scripts\python scripts/check_exploration_evidence.py
```

重新采样必须使用新目录，完整保留失败，不覆盖`docs/validation/v3.0.0`。正式根种子20261026、14条件共126次；开发演示根种子43不进入正式分母。180次候选消融是另一独立研究，位于`docs/validation/v2.1.0`。

- 软体为27顶点/24变形自由度的真实flex；规划对当前形状采用刚性搬运近似。反馈组平均峰值应变3.67%→4.90%，不能说减小变形。
- 铰接任务是被动关节整件搬运，不是主动开盖。
- 点云抓取估计无目标CAD或实例标签，但依赖已知桌面/标定/固定工作区提示；规划与搬运仍使用仿真几何。
- 感知损坏为合成误差，不是真实玻璃折射；采样不推进真实相机时间。
- 恢复的第一次闭合真实执行58mm开口故障，目标40mm；一次初始化、第二次成功不代表任意自然故障都能恢复。
- 强杂乱至少一个视角低可见，其他视角仍可能完全可见；主动观察5/6→3/6退化照实保留。
- 每条件只有6或12次，七项比较经多重校正后均未达0.05，不能宣称普遍显著提升。

原始逐次记录、协议、比较和开发轨迹保留在`docs/validation/`，不再在`outputs/`复制一份。历史专题PDF和ZIP通过Git历史查看。
