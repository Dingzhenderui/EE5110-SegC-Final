# 当前交付与重新生成

## 当前文件

- 主报告：[EE5110_Final_Report.pdf](../output/pdf/EE5110_Final_Report.pdf)，英文10页。
- 审片视频：[EE5110_5min_reviewed_preview.mp4](../deliverables/EE5110_5min_reviewed_preview.mp4)，300秒、无口播。
- [635词讲稿](final_video/NARRATION_EN.md)、[54条字幕](final_video/narration.srt)、[23镜头时间表](final_video/shot_list.csv)、[全片检查记录](final_video/FULL_REVIEW_ZH.md)。
- [LaTeX源码](final_report/README.md)，可直接上传Overleaf。
- 完整源码/模型/冻结证据在当前项目；[文件指南](FILE_GUIDE.md)说明职责。

模型和源码不需要解压历史提交ZIP。先按[README](../README.md)建立Python3.12环境，安装`requirements.txt`，运行两个setup脚本，再用`demo_viewer.py`或主函数运行。Windows快捷入口`OPEN_DEMO.cmd`需要本项目`.venv`。

## 可选构建依赖与命令

```powershell
.venv\Scripts\python -m pip install -r requirements-report.txt -r requirements-video.txt
# 重新生成图表、编译10页报告；需要本机LaTeX引擎
.venv\Scripts\python scripts/build_final_report.py --engine tectonic
# 只导出自包含Overleaf源码ZIP，无需编译器
.venv\Scripts\python scripts/build_final_report.py --figures-only --source-zip
# 检查15段原速素材的哈希、时长和完整解码
.venv\Scripts\python scripts/prepare_editing_materials.py
# 根据显式cue生成讲稿、字幕、镜头表；另加--render-preview可重剪
.venv\Scripts\python scripts/build_final_video_materials.py
```

仿真/录像/编译临时文件写入被忽略的`outputs/`。最终报告只有`output/pdf/EE5110_Final_Report.pdf`；不在源码目录重复存PDF。当前审片版由本地原速素材生成，54条cue已按画面检查，但录音后仍需核对语音同步。实际组员身份在`report.tex`的`\TeamLine`中填写。

## 按需打包

ZIP统一生成到`output/packages/`，不提交到Git。当前格式为3.1.0（也是默认值），旧格式请在相应Git版本中使用。

```powershell
# 无配音审阅包，明确标注不是最终口播成片
.venv\Scripts\python scripts/package_submission.py --review-kit --video deliverables/EE5110_5min_reviewed_preview.mp4
# 校验CRC、全文件SHA，并在独立解压目录实际运行dense/soft/recovery
.venv\Scripts\python scripts/verify_submission.py
```

加入真实录音、合成最终视频后：

```powershell
.venv\Scripts\python scripts/package_submission.py --video deliverables/EE5110_Final_Demo.mp4
.venv\Scripts\python scripts/verify_submission.py --archive output/packages/EE5110SegC_submission_v3.1.0.zip --extract-to outputs/submission_verification_final
```

独立验证目录必须为空。打包器明确选择视频，不会把文件名含preview的无配音视频自动当作最终视频。包内有主报告、视频、源码/GUI入口、模型/许可证、两套当前正式证据、LaTeX及剪辑材料，不包含环境/缓存或其他ZIP。

## 正式证据

`docs/validation/v2.1.0`保留180次候选策略研究，`v3.0.0`保留126次拓展筛查。它们与开发演示分别统计。旧阶段的正式记录也保留，以支持历史审计；旧报告、旧视频和运行副本从工作树移除后仍可从Git历史恢复。
