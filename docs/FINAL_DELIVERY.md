# 综合报告与5分钟视频交付说明

本次以远端最新、包含所有旧分支的 `feature/demo-materials-and-viewer@f65ee0c` 为基础，新建 `feature/final-latex-report-video`，不修改冻结引擎，不覆盖历史交付文件。

## 阅读顺序

1. `output/pdf/EE5110_Final_Report.pdf`：唯一综合主报告，英文10页，有完整基线、局部候选、软体/力控、受损感知、恢复和全部结果，含统计/局限。
2. `docs/final_video/NARRATION_EN.md`：635词英文口播，300秒/10段。
3. `docs/final_video/EDITING_GUIDE_ZH.md`：中文剪辑指南。
4. `docs/final_video/shot_list.csv`：23镜头的素材源/切点/倍速/静帧时间；`narration.srt`：61段英文字幕草稿。
5. `deliverables/EE5110_5min_captioned_preview.mp4`：严格300秒的字幕版预览，**没有口播音轨**。直接配上实际录音即可作为成片基础。
6. `docs/CODE_REVIEW_ZH.md`：详细代码审读和结果边界。
7. `docs/final_report/report.tex`：自包含LaTeX主文件；同目录含图/表和编译说明，可上传Overleaf。

## 运行

已有Python3.12环境时，从项目根目录运行：

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts/setup_assets.py
.venv\Scripts\python scripts/setup_ycb.py
.venv\Scripts\python demo_viewer.py
.venv\Scripts\python main.py --headless --balanced --task place --trials 6
.venv\Scripts\python clutter_main.py --headless --scene dense --trials 3
.venv\Scripts\python exploration_main.py --case sensor_robust --trials 3
.venv\Scripts\python exploration_main.py --case soft_adaptive --trials 3
.venv\Scripts\python exploration_main.py --case recovery_retry --trials 3
```

如果尚无`.venv`，先`py -3.12 -m venv .venv`。也可双击`OPEN_DEMO.cmd`；缺少Python/依赖时按界面提示安装。Windows/Linux均使用项目核心Python，LaTeX工具只影响编译，不影响机器人仿真。

## 构建材料

```powershell
.venv\Scripts\python scripts/build_final_report.py --engine tectonic
.venv\Scripts\python scripts/build_final_video_materials.py
.venv\Scripts\python scripts/build_final_video_materials.py --render-preview
```

报告构建需matplotlib和LaTeX引擎；视频预览需Pillow/imageio-ffmpeg（requirements-video.txt）。预览使用Windows Arial字体；跨平台可换字体路径。脚本会校验所有使用素材的SHA-256、切点和完整300秒时间轴，拒绝越界或空洞；不修改冻结日志和源片。

## 打包与核验

当前review kit有报告/源代码/全部必要模型和许可证/正式证据/运行说明/LaTeX/讲稿/字幕/预览；预览未录音这一状态会写进`START_HERE.txt`。代码已修复旧包遗漏GUI入口的问题，历史打包选项不变。

```powershell
.venv\Scripts\python scripts/package_submission.py --version 3.1.0 --video deliverables/EE5110_5min_captioned_preview.mp4 --review-kit
```

小组录音、加音轨后再显式创建最终提交包：

```powershell
.venv\Scripts\python scripts/package_submission.py --version 3.1.0 --video deliverables/EE5110_Final_Demo.mp4
.venv\Scripts\python scripts/verify_submission.py --archive deliverables/EE5110SegC_submission_v3.1.0.zip --extract-to outputs/submission_verification_final
```

使用全新空解压目录。验证包括CRC/全文件SHA、模型和两套证据审计，并实际执行dense、soft和recovery物理释放。主报告固定10页，组名/真实成员身份可通过`\TeamLine`添加；如果教师另有小组编号要求需在提交前据实填写。不要以旧v3.0的ZIP代替这次综合交付。

## 证据解释

本次49项功能测试和两套证据审计通过。180次候选消融和126次扩展筛查为既有冻结记录的重新核验，不是本次新跑306次试验。全报告/讲稿不把开发镜头计入正式分母；没有编造个人贡献。所有物理核心源码的冻结指纹保持不变。
