# 当前进度

当前工作分支：`feature/final-latex-report-video`。基线、180次候选策略研究、126次探索筛查和5分钟审片材料已完成；原分支及冻结引擎不改写。

## 已完成

- MuJoCo/Panda/YCB完整物理抓放流水线、GUI和批量实验入口。
- 14个拓展条件，保留正负结果、配对信息和物理成功门槛。
- 唯一10页英文综合报告及可编辑LaTeX源码。
- 300秒审片视频、635词讲稿、54条按画面对齐的字幕、23镜头时间表。
- 完整逐秒视频审读及关键动作加密检查，记录见`docs/final_video/FULL_REVIEW_ZH.md`。
- 项目清理：保留源码/模型/许可证/正式证据/当前交付物；ZIP、原始运行副本和编译缓存改为按需生成。

## 提交前尚需小组完成

- 按当前逐句时间表录制口播，合成音轨并校准语音同步。
- 如课程需要，在LaTeX的`\TeamLine`填写真实组员身份。
- 用最终配音视频生成提交ZIP，检查独立解压运行结果。

## 验证入口

`python -m unittest discover -s tests -v`；`scripts/check_completion_evidence.py`；`scripts/check_exploration_evidence.py`；`scripts/prepare_editing_materials.py`；`scripts/build_file_inventory.py --verify-files`。

最新清理验证记录见`docs/validation/project_cleanup/`。旧阶段的详细变更见`CHANGELOG.md`及Git历史。不要把功能测试或旧证据审计称为新采样306次实验。
