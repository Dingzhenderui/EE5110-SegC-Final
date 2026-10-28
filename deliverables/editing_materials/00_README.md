# 15段原速剪辑素材

全部视频为800×600、20fps、无音轨。执行片段来自实际MuJoCo运行，已移除2秒通用片头，尚未倍速；成片中的2x由最终剪辑脚本实施。

- `01_baseline/`：工作台、六YCB物体、候选姿态、完整抓放、六次开发随机试验。
- `02_explorations/`：杂乱遮挡、真软体、被动铰接、程序形状、力反馈、故障恢复、稳健感知。
- `03_comparisons/`：原候选安全拒绝、同场景改进抓放、五干扰物抓放。
- `CLIP_INDEX.json`：时长、原速属性、来源和SHA-256。`source`字段记录历史录制来源，不要求对应临时文件仍存在。
- `MANIFEST.json`：本目录当前文件的精确字节哈希，不包含清单自身。

所有片段都是开发演示，不进入正式180/126次分母。分析图在`docs/images/`，轨迹和记录在`docs/validation/`，不再复制一份到素材目录。

逐段说明见[演示指南](../../docs/DEMO_EDITING_GUIDE.md)，5分钟剪辑与录音见[剪辑指南](../../docs/final_video/EDITING_GUIDE_ZH.md)。校验：`python scripts/prepare_editing_materials.py`；按需打包：同命令加`--archive`。
