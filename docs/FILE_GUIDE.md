# 当前项目文件指南

[README](../README.md)负责安装/入口，[交付说明](FINAL_DELIVERY.md)负责生成与提交。完整Git分支的`PROJECT_FILES.json`覆盖受版本管理文件的大小、用途和哈希；精选提交ZIP使用其自身的`SUBMISSION_MANIFEST.json`。

## 目录分工

| 路径 | 职责 |
|---|---|
| `main.py` | 随机公开YCB物体的基线抓取/放置；完整任务加`--task place`。 |
| `clutter_main.py` | 三/五动态邻物、障碍、局部候选及有限恢复。 |
| `exploration_main.py` | 14条件的扩展实验入口，默认无界面。 |
| `challenge_main.py`、`sensing_main.py` | 障碍/合成感知研究入口，供历史协议复现。 |
| `demo_viewer.py` | 当前交互演示选择器；Windows用`OPEN_DEMO.cmd`启动。 |
| `robot_manipulation/` | 共用物理、感知、抓取、规划、控制、恢复和结果验证。 |
| `exploration/` | 真flex/hinge、程序形状、相关点云误差、力调节和执行故障恢复。 |
| `assets/` | pinned模型、纹理和原许可证；锁文件按精确字节校验。 |
| `tests/` | 49项物理/状态隔离/候选/机制/证据拒绝回归。 |
| `docs/validation/` | 唯一正式证据及必要开发记录，包含失败。 |
| `docs/images/` | 报告/分析所需原始截图与数据图。 |
| `docs/final_report/` | 自包含LaTeX、图表、数据表和编译说明。 |
| `docs/final_video/` | 当前讲稿、SRT、镜头CSV、显式cue和审片记录。 |
| `deliverables/editing_materials/` | 15段原速视频与索引/哈希。 |
| `deliverables/EE5110_5min_reviewed_preview.mp4` | 当前唯一5分钟审片视频，没有口播音轨。 |
| `output/pdf/` | 唯一最终10页报告。 |
| `outputs/`、`output/packages/` | 被忽略的临时运行/缓存/编译结果与按需ZIP。 |

## 机器人主干模块

| 模块 | 职责 |
|---|---|
| `config.py`、`transforms.py` | 物理门槛/参数与明确的`T_A_B`坐标约定。 |
| `environment.py`、`dataset.py` | 工作台、YCB/Panda资产、随机初始化、动力学步进。 |
| `perception.py`、`depth_sensing.py`、`active_sensing.py` | 已知几何接口、受损射线观测、模板拟合和有界采样。 |
| `grasp.py`、`local_grasps.py` | 原始候选及最多16个局部倾斜/偏移候选。 |
| `planning.py`、`search.py` | 阻尼IK、离散碰撞检查和有界RRT-Connect。 |
| `obstacle_planning.py`、`robust_obstacles.py`、`clutter_planning.py` | 绕障、持物预测、对称朝向和杂乱任务预检。 |
| `clutter.py` | 同时动态邻物、障碍与场景安全指标。 |
| `control.py`、`feedback.py`、`recovery.py` | 执行器轨迹、接触反馈、失联停止、同场景有限重试。 |
| `pipeline.py`、`evaluation.py` | 完整任务顺序、独立物理成功门槛及日志。 |
| `video.py`、`visualization.py` | 实际物理状态的录像/截图。 |

`exploration/`的`workcell.py/crowding.py`定义扩展场景；`sensing.py`实现点云观察器；`manipulation.py`实现接触调节和安全重试；`runner.py/protocol.py/provenance.py`负责条件、执行及源指纹。完整机制边界见[代码审读](CODE_REVIEW_ZH.md)。

## 脚本

| 脚本/系列 | 用途 |
|---|---|
| `setup_assets.py`、`setup_ycb.py`、`download.py` | 校验/补下载固定版本模型，有限重试。 |
| `benchmark_completion.py`、`benchmark_exploration.py` | 当前180次/126次正式协议的新运行；输出新目录。 |
| 其他`benchmark_*.py` | 可靠性、障碍、感知和v2历史研究的实验驱动。 |
| `check_completion_evidence.py`、`check_exploration_evidence.py` | 当前两套冻结证据审计。 |
| 其他`check_*evidence.py`及`check_obstacle_reliability.py` | 历史证据；使用相应`--source-ref`，CI列出了确切标签。 |
| `build_final_report.py` | 生成当前图表/表格、调用LaTeX并检查10页；可导出源码ZIP。 |
| `build_exploration_figures.py` | 从正式统计和开发轨迹重建力/应变/铰接/点云分析图。 |
| `build_final_video_materials.py` | 验证源片和显式cue，生成当前讲稿/SRT/CSV及审片视频。 |
| `prepare_editing_materials.py` | 默认校验15段原速素材；`--prepare-baseline`录制基础可视化，`--export-recordings`显式导出新源片，`--archive`按需打包。 |
| `record_*_demo.py` | 需要新镜头时重新运行物理演示，结果写入`outputs/`。 |
| `package_submission.py` | 当前3.1格式，显式选择视频，将ZIP生成到`output/packages/`。 |
| `verify_submission.py` | ZIP CRC/SHA、独立解压模型/证据审计及dense/soft/recovery实际运行。 |
| `build_file_inventory.py` | 暂存区文件索引；下载后用`--verify-files`核对精确内容。 |

已移除八个旧报告生成器和旧PDF；需要历史版时检出对应Git标签或提交。没有修改历史记录或冻结引擎。

## 记录怎样读

- `protocol.json`声明设计、条件、门槛和种子；JSONL每行一个完整结果，保留失败和每次尝试。
- `summary_*.json`汇总同一次运行；`comparison.json`为审计重算的配对比较，不是新样本。
- CSV是简化索引或开发状态/力/应变/关节时间序列，以列名单位为准。
- `docs/validation/v3.0.0/demo/`等开发演示不进入正式分母。
- 某些历史验证JSON中的报告/ZIP/录制源路径指当时快照，不要求在精简工作树重复保存；对应历史文件从Git读取。
