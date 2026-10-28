# EE5110 Segment C：机器人自主抓放

MuJoCo 3.15.0 / Python 3.12 / Franka Panda。项目包含公开YCB物体的完整抓放基线，以及杂乱、软体/铰接、未见形状、接触反馈、恢复和受损感知实验。

## 从这里开始

| 目的 | 文件 |
|---|---|
| 看最终英文报告（10页） | [EE5110_Final_Report.pdf](output/pdf/EE5110_Final_Report.pdf) |
| 看5分钟审片版（无口播） | [EE5110_5min_reviewed_preview.mp4](deliverables/EE5110_5min_reviewed_preview.mp4) |
| 录音、字幕与镜头表 | [英文讲稿](docs/final_video/NARRATION_EN.md)、[剪辑指南](docs/final_video/EDITING_GUIDE_ZH.md) |
| 修改报告 / 上传Overleaf | [LaTeX源码](docs/final_report/README.md) |
| 查看15段原速素材 | [editing_materials](deliverables/editing_materials/00_README.md) |
| 运行全部探索条件 | [实验条件与边界](docs/EXPLORATION_HANDOVER.md) |
| 了解源码与目录 | [文件指南](docs/FILE_GUIDE.md)、[代码审读](docs/CODE_REVIEW_ZH.md) |
| 生成/核验提交包 | [交付说明](docs/FINAL_DELIVERY.md) |

## 安装与运行

在项目根目录打开PowerShell：

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts/setup_assets.py
.venv\Scripts\python scripts/setup_ycb.py
.\OPEN_DEMO.cmd
```

已有环境时直接启动菜单。窗口支持暂停、旋转、平移和缩放；更详细的控制见[演示指南](docs/DEMO_EDITING_GUIDE.md)。模型与许可证已提供，setup优先校验已有文件。Linux使用`.venv/bin/python`执行相同Python入口。

```powershell
# 六种公开数据集物体的平衡随机完整抓放
.venv\Scripts\python main.py --headless --balanced --task place --trials 6 --seed 43
# 五个动态干扰物中的抓放
.venv\Scripts\python clutter_main.py --headless --scene dense --object foam_brick --trials 1 --seed 45
# 扩展单例；14种case见实验指南
.venv\Scripts\python exploration_main.py --case soft_adaptive --trials 1 --seed 43
```

## 检查与重新生成

```powershell
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python scripts/check_completion_evidence.py
.venv\Scripts\python scripts/check_exploration_evidence.py
.venv\Scripts\python scripts/build_file_inventory.py --verify-files
```

安装`requirements-video.txt`后可用`python scripts/prepare_editing_materials.py`校验并完整解码15段素材，用`python scripts/build_final_video_materials.py --render-preview`重新剪辑。报告构建需要`requirements-report.txt`和LaTeX引擎，见[源码说明](docs/final_report/README.md)。

## 文件保留规则

| 目录 | 内容与约定 |
|---|---|
| `robot_manipulation/`、`exploration/` | 仿真、感知、抓取、规划、控制和验证；冻结引擎保持不变。 |
| `assets/` | 固定版本模型、纹理、许可证和锁文件。 |
| `docs/validation/` | 正式/历史冻结证据及必要开发记录，保留全部失败。 |
| `docs/final_report/`、`docs/final_video/` | 当前报告源码、讲稿、字幕、镜头表。 |
| `deliverables/` | 当前审片视频、15段原速素材及其清单。 |
| `output/pdf/` | 唯一最终报告。 |
| `output/packages/` | 按需生成的ZIP，不纳入Git。 |
| `outputs/` | 本地运行、录制、缓存、编译和验证临时输出，不纳入Git。 |

历史报告、视频、旧ZIP和重复运行目录已从当前工作树清理，可通过Git历史恢复。没有重写历史。整理范围见[清理记录](docs/CLEANUP.md)。

候选策略研究180次与探索筛查126次分别报告，不能合并成统一成功率。仿真碰撞地图仍使用已知几何，合成深度不是玻璃光学，故障恢复为指定暂态闭合故障；详细限制见报告和实验指南。模型归属见[许可证说明](docs/ASSET_ATTRIBUTION.md)。
