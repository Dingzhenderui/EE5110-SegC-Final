# 综合报告 LaTeX 源码

`report.tex` 为唯一主文件，目标为 A4 单栏、10 页实质内容（没有独立空封面）。报告整合基线、180 次局部候选消融和126次拓展筛查，保留旧 PDF 与冻结引擎。

## 编译

项目根目录运行：

```powershell
.venv\Scripts\python scripts/build_final_report.py --engine tectonic
```

也支持 `--engine pdflatex` 或 `--engine xelatex`。编译器需要自行安装；首次 Tectonic 运行需要联网下载 LaTeX 包。图表生成依赖项目 `requirements-report.txt` 中的 matplotlib；PDF 编译本身不使用 ReportLab。

Overleaf：把本文件夹的 `report.tex`、`results_table.tex` 和整个 `figures/` 上传，以 `report.tex` 为主文件，选 pdfLaTeX。所有图片均为本地相对路径，不需要访问项目其他目录。`evidence_summary.json` 保留图表数据来源。

生成表格和图但不编译：

```powershell
.venv\Scripts\python scripts/build_final_report.py --figures-only
```

编译后 PDF：`output/pdf/EE5110_Final_Report.pdf`。`report.pdf` 是源目录旁的同内容编译副本。组员姓名/学号没有编造；如课程另需身份栏，修改 `\TeamLine`，填写真实组员信息后重新编译。

## 页内容

1. 摘要、研究问题和工作台
2. 场景、公开数据集、坐标与完整流程
3. 感知、IK/规划、控制和物理成功门槛
4. 局部候选算法与180次配对实验
5. 软体与力反馈的保持/变形权衡
6. 受损点云与稳健融合
7. 真实暂态闭合故障和同场景恢复
8. 其他探索及14条件全结果
9. 统计解释、失败、局限和后续实验
10. 复现、验证、源码定位和参考文献
