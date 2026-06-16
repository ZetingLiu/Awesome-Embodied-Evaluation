# Awesome Embodied Evaluation [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![English](https://img.shields.io/badge/lang-English-lightgrey.svg)](README.md) [![简体中文](https://img.shields.io/badge/lang-简体中文-blue.svg)](README_CN.md)

面向具身基础模型的**评测基准与评测方法**清单，覆盖三条线：**视觉语言模型（VLM）**、**视觉-语言-动作模型（VLA）**、**世界模型（WM）**。

多数现有清单只覆盖其中一条线。本仓库把三条线放在一起，重点说清**每个基准到底是怎么评的**——任务设置、输入输出、指标，以及复现这些数字需要哪些条件。

欢迎贡献，详见 [贡献指南](#贡献指南)。

## 目录

- [范围](#范围)
- [条目组织方式](#条目组织方式)
- [VLM 评测](#vlm-评测)
- [VLA 评测](#vla-评测)
- [世界模型评测](#世界模型评测)
- [相关清单](#相关清单)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 范围

本清单聚焦具身基础模型的评测：

- **VLM** —— 多模态理解与推理。
- **VLA** —— 语言条件下的机器人操作与控制。
- **WM** —— 世界模型的感知质量与下游可用性。

不在范围内：纯导航 / 仅语言的基准（除非与具身评测直接相关），以及没有明确评测协议的论文合集。

## 条目组织方式

每个条目都给出论文、官方代码、主要指标，以及复现相关的说明。在有必要时，条目还会标注输入/输出格式、评分方式（基于规则、仿真器、VLM 充当裁判，或人工），以及泛化设置（同分布、OOD、或 sim-to-real）。

## VLM 评测

| 基准 | 年份 | 评什么 | 指标 | 链接 |
|---|---|---|---|---|
| **MMMU** | 2023 | 大学级、多学科多模态推理（30 个学科，图像类型高度异构） | Accuracy | [论文](https://arxiv.org/abs/2311.16502) · [代码](https://github.com/MMMU-Benchmark/MMMU) · [主页](https://mmmu-benchmark.github.io/) |
| **MMBench** | 2023 | 细粒度、多能力维度理解，含 CircularEval；中英双语 | Accuracy | [论文](https://arxiv.org/abs/2307.06281) · [代码](https://github.com/open-compass/MMBench) |
| **MathVista** | 2023 | 视觉情境下的数学推理（图表、几何、图形） | Accuracy | [论文](https://arxiv.org/abs/2310.02255) · [代码](https://github.com/lupantech/MathVista) |
| **Video-MME / Video-MME-v2** | 2024/2026 | 全面视频理解评测；v2 进一步强调鲁棒性、一致性与推理可靠性 | Accuracy / 组级评分（v2） | [论文 v1](https://arxiv.org/abs/2405.21075) · [代码 v1](https://github.com/MME-Benchmarks/Video-MME) · [论文 v2](https://arxiv.org/abs/2604.05015) · [代码 v2](https://github.com/MME-Benchmarks/Video-MME-v2) |
| **SEED-Bench 系列** | 2023-2024 | 覆盖更广的多模态能力（图像/视频、生成式理解、富文本视觉理解） | Accuracy | [论文](https://arxiv.org/abs/2307.16125) · [代码](https://github.com/AILab-CVC/SEED-Bench) |
| **DocVQA（RRC 赛道）** | 2020-持续更新 | 文档视觉问答与文档推理，按挑战赛协议评测 | ANLS / Accuracy | [论文](https://arxiv.org/abs/2007.00398) · [RRC](https://rrc.cvc.uab.es/) |

常用工具：[VLMEvalKit](https://github.com/open-compass/VLMEvalKit) 为上述基准及 80+ 其他基准提供标准化评测。

## VLA 评测

| 基准 | 年份 | 评什么 | 指标 | 链接 |
|---|---|---|---|---|
| **LIBERO** | 2023 | 终身 / 语言条件下的桌面操作（Spatial、Object、Goal、Long 四个子集） | 成功率 | [论文](https://arxiv.org/abs/2306.03310) · [代码](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| **CALVIN** | 2021 | 长时序指令串联；组合泛化（ABC→D） | 平均完成链长 | [论文](https://arxiv.org/abs/2112.03227) · [代码](https://github.com/mees/calvin) |
| **SimplerEnv** | 2024 | 真实机器人策略的 real-to-sim 评测（Google Robot、WidowX+Bridge） | 成功率、sim↔real 相关性（MMRV、Pearson r） | [论文](https://arxiv.org/abs/2405.05946) · [代码](https://github.com/simpler-env/SimplerEnv) |
| **ManiSkill2** | 2023 | 多对象、多技能条件下的泛化操作评测，强调高吞吐仿真 | 任务成功率 / 奖励相关指标 | [论文](https://arxiv.org/abs/2302.04659) · [代码](https://github.com/haosulab/ManiSkill2-task-dev) |
| **BEHAVIOR-1K** | 2024 | 面向真实日常活动的长时程任务评测，强调高保真物理与场景复杂度 | 活动成功率 / 完成度指标 | [论文](https://arxiv.org/abs/2403.09227) · [代码](https://github.com/StanfordVL/BEHAVIOR-1K) |
| **RoboCasa / RoboCasa365** | 2024/2026 | 大规模厨房场景日常操作评测，覆盖原子技能到长时程复合任务 | 各套件成功率 | [论文](https://arxiv.org/abs/2406.02523) · [代码](https://github.com/robocasa/robocasa) |

常用框架：[vla-evaluation-harness](https://github.com/allenai/vla-evaluation-harness) 用 Docker 和统一协议运行上述多个基准。

## 世界模型评测

| 基准 | 年份 | 评什么 | 指标 | 链接 |
|---|---|---|---|---|
| **WorldArena** | 2026 | 感知质量 + 功能效用（数据引擎、策略评测、动作规划） | EWMScore（综合） | [论文](https://arxiv.org/abs/2602.08971) · [主页](https://world-arena.ai/) |
| **WorldScore** | 2025 | 统一的世界生成评测，覆盖 3D/4D/T2V/I2V；可控性、质量、动态性 | WorldScore（综合） | [论文](https://arxiv.org/abs/2504.00983) · [主页](https://haoyi-duan.github.io/WorldScore/) |
| **EWMBench** | 2025 | 具身世界模型：场景一致性、运动正确性、语义对齐 | 各维度分数 | [代码](https://github.com/AgibotTech/EWMBench) |
| **WorldModelBench** | 2025 | 面向世界建模能力的评测：指令遵循、常识一致性、物理一致性 | 综合世界建模分数 | [论文](https://arxiv.org/abs/2502.20694) · [代码](https://github.com/WorldModelBench-Team/WorldModelBench) |
| **4DWorldBench** | 2025/2026 | 3D/4D 世界生成能力评测：感知质量、条件对齐、物理真实性与时空一致性 | 多维综合评测 | [论文](https://arxiv.org/abs/2511.19836) |

## 相关清单

- [awesome-vla-wam](https://github.com/DravenALG/awesome-vla-wam) —— VLA 与世界动作模型（WAM）。
- [Awesome-World-Action-Model](https://github.com/HyperbolicCurve/Awesome-World-Action-Model) —— WAM/VLA 的论文、数据集与基准。
- [awesome-embodied-vla-va-vln](https://github.com/jonyzhang2023/awesome-embodied-vla-va-vln) —— VLA / VA / VLN 模型与仿真器。

## 贡献指南

欢迎提 PR。新增条目时，请附带：

- 论文与官方代码链接。
- 任务设置、输入/输出格式，以及主要指标。
- 如果有，给一条最小运行命令。
- 你遇到过的复现坑（坐标约定、归一化统计、模糊的终止规则等）。

每行一个条目，放进对应的赛道表格中。

## 许可证

[MIT](LICENSE)
