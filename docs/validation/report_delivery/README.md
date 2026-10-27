# 综合交付验证：2026-10-27

- 基点`f65ee0c55c2a90bd4695514dcebf9d4d328efefe`，核对远端10分支的提交关系，全部被最新完整分支包含。
- 原有49个unittest全部通过，耗时89.236秒；本机Python3.12.4、MuJoCo3.15.0、NumPy2.5.3。未重新批量采样180/126次正式实验。
- `check_completion_evidence.py`：180条完整候选策略证据及配对通过。
- `check_exploration_evidence.py`：126条探索证据、物理机制、配对初态/材料/首包通过。审计重写comparison时会在Windows改行尾，新3.1打包路径在finally恢复原始字节；两套冻结目录和物理引擎与基点无diff。
- LaTeX由Tectonic0.17.0实际编译，正好10页；无overfull boxes、undefined references。逐页渲染检查，页内图/表/公式无重叠裁切，未使用独立空封面凑页数。
- 视频：1280×720、25fps、H.264、300.00秒、无音轨；全片解码通过；20个时点视觉检查通过，倍速和静帧注明，原4:3素材不拉伸，字幕不遮挡物理操作区域。
- 讲稿635词、23镜头、61段字幕，时间轴连续、源片切点均在界内、所有输入素材哈希匹配。
- review kit独立解压：CRC、413条manifest SHA-256、模型和两套证据审计通过；dense seed45、soft_adaptive seed43、recovery_retry seed43各1/1物理成功。
- 版本3.1不带`--review-kit`时拒绝将名称含preview的无配音预览冒充最终视频；历史打包选项保持。
- 后续仅更新打包器的comparison字节保留与文件导航；重新打包后复核全部CRC/哈希。223个核心/资产/证据/视频/报告文件与独立解压验证副本一致，其中comparison.json仅规范化行尾后比较。

`verification.json`保存主产物的大小和SHA-256。本记录是交付验证而非正式抓取成功率样本；预览仍需小组录音，身份栏按真实组员填写。
