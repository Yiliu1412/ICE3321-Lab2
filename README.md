# ICE3321-Lab2
Course codes for ICE3321 Lab2 ABR Algorithm Compare.

本项目是一个关于视频码率自适应算法的实验框架，包含 **BBA** 和 **RB** 两种算法的实现与比较，以及实验结果的分析和可视化。

---

## 项目简介

在视频流媒体传输中，码率自适应算法（ABR）是提升用户体验的关键技术。本项目通过实现和比较两种经典的 ABR 算法：
- **BBA (Buffer-Based Adaptation)**：基于缓冲区大小的码率自适应算法。
- **RB (Rate-Based Adaptation)**：基于固定码率的自适应算法。

通过实验，分析两种算法在不同网络条件下的表现，包括以下指标：
- 视频质量（码率）
- 视频卡顿时间
- 视频质量波动
- 最终用户体验（QoE）

---

## 项目结构

```
bbaLab/
├── bba.py                  # BBA 算法实现
├── rb.py                   # RB 算法实现
├── compare_bba_rb.py       # 比较 BBA 和 RB 算法的脚本
├── trace_plot.py           # 绘制网络带宽、缓冲区和码率变化图
├── fixed_env.py            # 实验环境定义
├── load_trace.py           # 加载网络轨迹工具
├── environment_check.py    # 环境检查脚本
├── test_traces/            # 网络带宽轨迹文件
├── video_size/             # 视频大小数据
├── report/                 # 实验报告和结果图表
└── README.md               # 项目说明文件
```

---

## 快速开始

### 1. 环境配置

运行 `environment_check.py` 检查所需的 Python 包是否已安装：
```bash
python environment_check.py
```

如果缺少依赖库，请根据提示安装。例如：
```bash
pip install matplotlib numpy
```

---

### 2. 运行示例代码

运行 `trace_plot.py`，选取至少三个网络带宽 trace 文件，绘制以下图像：
- 网络带宽随时间的变化图
- 缓冲区大小随时间的变化图
- 码率选择随时间的变化图

运行命令：
```bash
python trace_plot.py
```

示例输出图像将保存在当前目录下，或者直接显示在窗口中。

---

### 3. 调整 BBA 算法参数

打开 `bba.py` 文件，调整以下参数：
- `RESERVOIR`：缓冲区的保留大小
- `CUSHION`：缓冲区的缓冲大小

例如：
```python
RESERVOIR = 10  # 调整为 10
CUSHION = 20    # 调整为 20
```

运行 BBA 算法：
```bash
python bba.py
```

分析不同参数设置对以下指标的影响：
- 视频码率选择
- 缓冲区大小
- 视频卡顿时间

---

### 4. 实现并运行 RB 算法

根据 RB 算法的原理，完成 `rb.py` 中的实现逻辑。RB 算法的核心是基于固定的码率选择策略。

运行 RB 算法：
```bash
python rb.py
```

---

### 5. 比较 BBA 和 RB 算法

使用 `compare_bba_rb.py` 比较以下指标：
- 视频质量（视频码率）
- 视频卡顿时间
- 视频质量波动
- 最终的 QoE（reward）

运行命令：
```bash
python compare_bba_rb.py
```

生成的图像将保存在 `report/` 文件夹中，包括：
1. 视频码率随时间的变化图
2. 视频卡顿时间随时间的变化图
3. 视频质量波动随时间的变化图
4. 平均 QoE 的柱状图

---

## 实验结果

实验结果将帮助您深入理解 BBA 和 RB 算法的优缺点及其在不同场景下的表现。

---

## 引用

如果您在研究中使用了本项目，请引用以下文献：

- T.-Y. Huang et al., "A buffer-based approach to rate adaptation: Evidence from a large video streaming service," *Proc. ACM Conf. SIGCOMM (SIGCOMM)*, 2014. [DOI: 10.1145/2619239.2626296](https://doi.org/10.1145/2619239.2626296)
- [Pensieve Test BB](https://github.com/hongzimao/pensieve/blob/master/test/bb.py) 
