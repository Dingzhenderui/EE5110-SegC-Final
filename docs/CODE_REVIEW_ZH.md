# 最新完整分支代码审读与交付分析

基准：`feature/demo-materials-and-viewer`，提交`f65ee0c55c2a90bd4695514dcebf9d4d328efefe`。2026-10-27读取远端全部10个分支并核对祖先关系。该分支包含`main`、候选补全、全部探索方向，以及素材/GUI，是当前完整的基础。新工作分支：`feature/final-latex-report-video`。原始工作目录及`outputs/gui_demo/`保持不动。

## 1. 项目实际做了什么

这是**MuJoCo仿真中的Panda物理抓放系统**，主语言Python3.12，核心依赖MuJoCo3.15.0/NumPy2.5.3。没有ROS、真实机械臂驱动或训练出的抓取神经网络。录像/报告是独立的可选依赖层。

| 层次 | 入口/代码 | 实际职责 |
|---|---|---|
| 单物体基线 | `main.py`；`environment.py`、`dataset.py` | pinned Panda/YCB模型、随机对象和位姿、物理状态、接触/释放 |
| 障碍搬运 | `challenge_main.py`；`obstacle_planning.py`、`robust_obstacles.py`、`search.py` | 复合障碍预检、多IK解、夹爪对称性、有界RRT-Connect |
| 合成深度 | `sensing_main.py`；`depth_sensing.py`、`active_sensing.py` | 正交射线、缺失/噪声、模板几何拟合、主动采样停止 |
| 杂乱抓放 | `clutter_main.py`；`clutter.py`、`clutter_planning.py`、`local_grasps.py` | 动态邻物、碰撞诊断、局部倾斜/偏移候选、邻物安全门槛 |
| 通用控制/恢复 | `pipeline.py`、`control.py`、`feedback.py`、`recovery.py` | 状态序列、执行器控制、接触验证、有限重试 |
| 扩展实验 | `exploration_main.py`；`exploration/` | 真flex、被动hinge、程序形状、受损无实例标签点云、力调节、真实暂态闭合故障 |
| 交互/素材 | `demo_viewer.py`；`scripts/prepare_editing_materials.py` | 选择/运行任务、提供15段原速开发演示及来源索引 |

`robot_manipulation/`为成熟可复用主干；`exploration/`以环境/观察器/控制器分离的方式扩展，不需要为做报告重构核心。已有物理回归测试和证据指纹，改引擎就需要重新采样，收益不及风险。

## 2. 算法调用链

`reset/settle → observe → generate_candidates → pregrasp/approach/task preview → actuator close → lift/hold → transfer/lower → open/retreat → verify`。

- `grasp.generate_candidates`：估计网格投影宽度＋6mm，最大80mm；140mm预抓取距离、160mm名义提升。
- `Planner.ik`：阻尼最小二乘，lambda=.025、旋转权重.4、最多500次迭代、2mm/0.025rad容差；碰撞拒绝和数值误差分别记录。最多九个IK初值。
- `Planner.validate`：约0.015rad的离散关节采样；有界RRT-Connect用于绕障，不是连续安全证明。
- `Controller.execute`：cubic smoothstep规划参考、0.5rad/s和2rad/s²命令约束；接触动力学由仿真推进。
- `local_candidates`：原前缀不变，closing axis保持不变，增加最多16个±30°/±45°和±12mm候选；模板支撑至少10mm，全部重新通过规划。
- `ContactController.regulate`：弱侧法向力误差积分调节preload，soft目标1.25N/指、rigid5N/指；demand范围.5–32N；双指接触丢失60ms停止。并非完整阻抗控制。
- `PointObserver`：没有CAD和target ID输入；已知桌面、固定hint、前景连通分量、最小面积框。robust为4mm体素至少3个不同数据包支持，不是统计独立性保证。

## 3. 最值得展开的证据

### 候选策略180次

严格配对，仅改变候选策略：三邻物54/60→58/60，五邻物26/30→29/30。分别恢复4次和3次失败，无退化，改进集中在foam_brick。精确McNemar p=.125/.25，不能写显著改善。失败开发例是手掌与罐子碰撞，不是机械臂一定够不到。

### 扩展筛查126次

14条件分别6或12次，完整计数见报告第8页。重点结论：

- 受损感知6/12→原始融合1/12→稳健融合9/12；raw11次planning fail，robust3次全为wedge contact-loss。瓶颈转换的证据比“多采几帧更准”更有价值。
- 真flex固定preload2/6、调节6/6；平均峰应变3.668%→4.904%，不能说减少变形。失败组暴露时间不同。
- 随机质量/摩擦/延迟的刚体force10/12→12/12；实际修改物理参数，不只改标签。
- 暂态闭合故障single0/6、retry6/6；first_success仍0/6，scene reset_count=1。不是自然故障恢复率。
- 强杂乱single5/6、active3/6；仅至少一个视角可见率<50%，另一个视角在全部试验中可见率1.0。不是所有方向完全遮挡。
- novel_prior/points均11/12；hinge6/6是被动整件搬运，不是开盖。
- 七个预声明比较，最小原始p=.0078125，Bonferroni校正后=.0546875，均未过.05。

## 4. 必须写清的真实性边界

1. 真值隔离仅针对指定观察器。碰撞地图、持物预测和TRANSFER居中依然使用仿真几何/真值中心；材料/力学实验用GeometryObserver隔离力学，不是纯视觉端到端。
2. alpha=.25是外观，射线dropout是合成损坏；没有玻璃折射/反光模型。
3. flex真实动态变形，但规划将当前形状刚性搬运，不是预测性软体规划。
4. baseline中的foam_brick为刚体；novel是程序生成未见实例，不是大规模真实物体泛化。
5. 40N是gripper执行器峰值上限，不是每指法向力上限，也不是实机安全保证。
6. 180次与126次分别研究，不能合成某个“306次总体成功率”；本次运行审计与49个功能测试，不冒称重新采样306次。
7. 虚拟采样不推进物理时间，不能用frames/30当实测相机延迟；并发实验wall time不能比较硬件效率。

## 5. 原交付的问题与本次处理

旧v3报告虽然10页，却把baseline/局部候选的大部分内容外置于6页v2报告。新综合报告以研究问题组织而非交接历史，保留全部结果和边界。旧报告和冻结日志不覆盖。

旧v3视频3:32.55、无音轨；15段原速素材总计736.35秒。新材料给出300秒镜头表、约5分钟英文口播、SRT与中文指南；字幕预览不等同已配音成片。

旧`package_submission.py`未纳入`demo_viewer.py/OPEN_DEMO.cmd`等GUI入口。新增3.1交付路径时补齐入口和LaTeX/讲稿，要求显式指定最终演示视频，避免误用旧视频或把未配音预览隐式当最终片。历史版本打包路径保留。

## 6. 维护和推荐下一步

本次不改冻结引擎。报告、图表构建、视频材料与打包工具在独立分支完成，维护README/PROGRESS/CHANGELOG并更新文件索引。后续研究优先做wedge接触稳定性的oracle/estimated消融、同暴露时长的应变对照，以及真实感知误差/安全撤离受阻的恢复实验；不建议在提交前随意加入新的控制器导致证据失效。
