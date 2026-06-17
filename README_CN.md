# Awesome Embodied Evaluation [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![English](https://img.shields.io/badge/lang-English-lightgrey.svg)](README.md) [![简体中文](https://img.shields.io/badge/lang-简体中文-blue.svg)](README_CN.md)

面向统一 / Omni 具身模型的**评测基准与评测方法**清单，覆盖三类核心能力：**Reasoning & Planning（推理与规划）**、**Action（动作）**、**World Modeling（世界建模）**。

多数现有清单只覆盖其中 1-2 类能力。本仓库把三类能力放在一起，重点说清**每个基准到底是怎么评的**——任务设置、输入输出、指标，以及复现这些数字需要哪些条件。

欢迎贡献，详见 [贡献指南](#贡献指南)。

## 目录

- [范围](#范围)
- [条目组织方式](#条目组织方式)
- [生态完整性](#生态完整性)
- [Reasoning & Planning 评测](#reasoning--planning-评测)
- [Action 评测](#action-评测)
- [World Modeling 评测](#world-modeling-评测)
- [相关清单](#相关清单)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 范围

本清单聚焦统一 / Omni 具身模型的三类核心能力评测：

- **Reasoning & Planning（推理与规划）** —— 多模态感知、空间 / 物理推理、具身问答、任务规划与下一步预测。
- **Action（动作）** —— 在仿真或真机中生成并执行动作的具身策略，覆盖 VLA 模型与世界动作模型。
- **World Modeling（世界建模）** —— 对环境动态、物理一致性、可控性与下游任务效用进行预测或生成建模。

我们优先收录**权威、被广泛采用**的基准——即社区认可度高（star 多）、且**生态完整**（有官方代码、活跃 leaderboard、可复现协议）的工作。

对 **Reasoning & Planning 主榜单（Primary）**，我们采用更严格标准：仅收录任务目标**直接对应具身能力**的基准（空间落地、具身规划、物理推理、环境级具身问答）；通用多模态基准统一放在对照集（Control Set）。

不在范围内：纯导航 / 仅语言的基准（除非与具身评测直接相关），以及没有明确评测协议的论文合集。

## 条目组织方式

每个条目都给出论文、官方代码、主要指标，以及复现相关的说明。在有必要时，条目还会标注输入/输出格式、评分方式（基于规则、仿真器、VLM 充当裁判，或人工），以及泛化设置（同分布、OOD、或 sim-to-real）。

表格进一步按 **推理 / 规划能力维度**、**动作评测环境**（仿真 / sim-to-real / 真机）、或 **世界建模维度** 拆分。分类字段见 `data/benchmarks.yaml`（`vlm_category`、`vla_env`、`wm_category`）。

表中的 **Stars** 与 **最近更新** 两列来自 GitHub 仓库元数据，由维护者在更新表格时手动刷新；其余字段全部人工策展。

## 生态完整性

本清单把生态完整性视为可复现性的实践信号。新增或复核条目时，维护者会检查该基准是否提供：

- **论文**：正式论文、arXiv 预印本或技术报告。
- **代码**：官方评测代码、统一 harness 或可运行脚本。
- **数据 / 任务**：公开数据集、仿真资产、任务定义或 benchmark split。
- **协议**：清晰的指标、prompt、评分规则、数据划分或提交格式。
- **排行榜**：公开 leaderboard、标准提交入口或仍活跃的挑战赛。

重要基准即使生态组件不完整也可以收录，但缺口应在条目链接或描述中可见，并在后续维护时继续复核。

## Reasoning & Planning 评测

Reasoning & Planning 评测拆成两层：

- **具身 Reasoning & Planning 主榜单（Primary）**：直接评估具身相关能力（空间落地、规划、物理理解、环境级问答）。
- **通用多模态对照集（Control Set）**：用于监控通用多模态能力，避免“具身能力提升但通用能力退化”。

### 具身 Reasoning & Planning 主榜单（Primary）

#### 空间定位与 3D 场景理解

<!-- AEE-TABLE:VLM-PRIMARY-SPATIAL:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 1 | **Where2Place** | 2024 | 空闲空间指代与放置点预测：在杂乱真实场景中根据语言定位可放置区域 | 点位准确率 | 224 | 2025-07 | [论文](https://arxiv.org/abs/2406.10721) · [代码](https://github.com/wentaoyuan/RoboPoint) · [数据集](https://huggingface.co/datasets/wentao-yuan/where2place) |
| 2 | **RefSpatial-Bench** | 2025 | 复杂 3D 场景下的多步空间指代与放置推理 | 准确率（Location / Placement） | 263 | 2025-12 | [论文](https://arxiv.org/abs/2506.04308) · [代码](https://github.com/Zhoues/RoboRefer) · [主页](https://zhoues.github.io/RoboRefer/) |
| 3 | **VSI-Bench** | 2025 | 基于第一视角视频的视觉空间智能评测（配置关系、测量估计、时空记忆） | Accuracy / MRA | 726 | 2025-08 | [论文](https://arxiv.org/abs/2412.14171) · [代码](https://github.com/vision-x-nyu/thinking-in-space) · [数据集](https://huggingface.co/datasets/nyu-visionx/VSI-Bench) |
| 4 | **EmbSpatial-Bench** | 2024 | 具身 3D 场景中的第一视角空间关系理解（上下左右/远近等 6 类关系） | Accuracy | 31 | 2024-06 | [论文](https://arxiv.org/abs/2406.05756) · [代码](https://github.com/mengfeidu/EmbSpatial-Bench) · [数据集](https://huggingface.co/datasets/Phineas476/EmbSpatial-Bench) |
<!-- AEE-TABLE:VLM-PRIMARY-SPATIAL:END -->

#### 规划与下一步推理

<!-- AEE-TABLE:VLM-PRIMARY-PLANNING:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 5 | **EgoPlan-Bench2** | 2024 | 第一视角真实日常场景规划，强调长时程任务进度理解与下一步决策 | Accuracy | 31 | 2025-04 | [论文](https://arxiv.org/abs/2412.04447) · [代码](https://github.com/qiulu66/EgoPlan-Bench2/) · [主页](https://qiulu66.github.io/egoplanbench2/) |
<!-- AEE-TABLE:VLM-PRIMARY-PLANNING:END -->

#### 具身问答

<!-- AEE-TABLE:VLM-PRIMARY-QA:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 6 | **OpenEQA** | 2024 | 具身问答：覆盖 episodic memory 与 active exploration 两种设定 | LLM 裁判分 / 回答质量 | 365 | 2024-09 | [论文](https://openaccess.thecvf.com/content/CVPR2024/html/Majumdar_OpenEQA_Embodied_Question_Answering_in_the_Era_of_Foundation_Models_CVPR_2024_paper.html) · [代码](https://github.com/facebookresearch/open-eqa) · [主页](https://open-eqa.github.io/) |
<!-- AEE-TABLE:VLM-PRIMARY-QA:END -->

#### 物理推理

<!-- AEE-TABLE:VLM-PRIMARY-PHYSICAL:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 7 | **PhysBench** | 2025 | 面向具身体的物理世界理解（物体属性/关系、场景物理、动态） | 物理维度综合准确率 | 91 | 2026-01 | [论文](https://arxiv.org/abs/2501.16411) · [代码](https://github.com/physical-superintelligence-lab/PhysBench) · [主页](https://physbench.github.io/) |
<!-- AEE-TABLE:VLM-PRIMARY-PHYSICAL:END -->

#### 具身推理（多模态 QA）

<!-- AEE-TABLE:VLM-PRIMARY-REASONING:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 8 | **ERQA（具身推理问答）** | 2025 | 真实机器人场景下的多模态具身推理问答（空间推理与世界知识） | Accuracy（选择题） | 275 | 2025-03 | [技术报告](https://storage.googleapis.com/deepmind-media/gemini-robotics/gemini_robotics_report.pdf) · [代码](https://github.com/embodiedreasoning/ERQA) |
<!-- AEE-TABLE:VLM-PRIMARY-REASONING:END -->

### 通用多模态对照集（Control Set）

#### 推理

<!-- AEE-TABLE:VLM-CONTROL-REASONING:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 9 | **MMMU** | 2023 | 大学级、多学科多模态推理（30 个学科，图像类型高度异构） | Accuracy | 576 | 2026-02 | [论文](https://arxiv.org/abs/2311.16502) · [代码](https://github.com/MMMU-Benchmark/MMMU) · [主页](https://mmmu-benchmark.github.io/) |
| 10 | **MathVista** | 2023 | 视觉情境下的数学推理（图表、几何、图形） | Accuracy | 363 | 2025-09 | [论文](https://arxiv.org/abs/2310.02255) · [代码](https://github.com/lupantech/MathVista) |
<!-- AEE-TABLE:VLM-CONTROL-REASONING:END -->

#### 感知与理解

<!-- AEE-TABLE:VLM-CONTROL-PERCEPTION:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 11 | **MMBench** | 2023 | 细粒度、多能力维度理解，含 CircularEval；中英双语 | Accuracy | 303 | 2025-05 | [论文](https://arxiv.org/abs/2307.06281) · [代码](https://github.com/open-compass/MMBench) |
| 12 | **SEED-Bench 系列** | 2023-2024 | 覆盖更广的多模态能力（图像/视频、生成式理解、富文本视觉理解） | Accuracy | 364 | 2025-01 | [论文](https://arxiv.org/abs/2307.16125) · [代码](https://github.com/AILab-CVC/SEED-Bench) |
<!-- AEE-TABLE:VLM-CONTROL-PERCEPTION:END -->

#### 视频理解

<!-- AEE-TABLE:VLM-CONTROL-VIDEO:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 13 | **Video-MME / Video-MME-v2** | 2024/2026 | 全面视频理解评测；v2 进一步强调鲁棒性、一致性与推理可靠性 | Accuracy / 组级评分（v2） | 779 | 2025-12 | [论文 v1](https://arxiv.org/abs/2405.21075) · [代码 v1](https://github.com/MME-Benchmarks/Video-MME) · [论文 v2](https://arxiv.org/abs/2604.05015) · [代码 v2](https://github.com/MME-Benchmarks/Video-MME-v2) |
<!-- AEE-TABLE:VLM-CONTROL-VIDEO:END -->

#### 文档理解

<!-- AEE-TABLE:VLM-CONTROL-DOCUMENT:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 14 | **DocVQA（RRC 赛道）** | 2020-持续更新 | 文档视觉问答与文档推理，按挑战赛协议评测 | ANLS / Accuracy | — | — | [论文](https://arxiv.org/abs/2007.00398) · [RRC](https://rrc.cvc.uab.es/) |
<!-- AEE-TABLE:VLM-CONTROL-DOCUMENT:END -->

常用工具：[VLMEvalKit](https://github.com/open-compass/VLMEvalKit) 为上述基准及 80+ 其他基准提供标准化评测。

## Action 评测

Action 基准先按 **策略在哪里评测** 分组：闭环仿真、sim-to-real 代理、真机硬件。仿真基准进一步按它主要暴露的能力或失败模式拆分。

### 仿真 · 核心套件

<!-- AEE-TABLE:VLA-SIM-CORE:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 1 | **LIBERO** | 2023 | 终身 / 语言条件下的桌面操作（Spatial、Object、Goal、Long 四个子集） | 成功率 | 2.0k | 2025-03 | [论文](https://arxiv.org/abs/2306.03310) · [代码](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| 2 | **CALVIN** | 2021 | 长时序指令串联；组合泛化（ABC→D） | 平均完成链长 | 942 | 2025-09 | [论文](https://arxiv.org/abs/2112.03227) · [代码](https://github.com/mees/calvin) |
| 3 | **RLBench** | 2020 | CoppeliaSim 中 100+ 语言条件操作任务（Franka Panda）；动作模型/操作学习长期基线 | 成功率 | 1.8k | 2025-01 | [论文](https://arxiv.org/abs/1909.12271) · [代码](https://github.com/stepjam/RLBench) |
| 4 | **ManiSkill2** | 2023 | 多对象、多技能条件下的泛化操作评测，强调高吞吐仿真 | 任务成功率 / 奖励相关指标 | 1 | 2023-08 | [论文](https://arxiv.org/abs/2302.04659) · [代码](https://github.com/haosulab/ManiSkill2-task-dev) |
| 5 | **BEHAVIOR-1K** | 2024 | 面向真实日常活动的长时程任务评测，强调高保真物理与场景复杂度 | 活动成功率 / 完成度指标 | 1.5k | 2026-06 | [论文](https://arxiv.org/abs/2403.09227) · [代码](https://github.com/StanfordVL/BEHAVIOR-1K) |
<!-- AEE-TABLE:VLA-SIM-CORE:END -->

### 仿真 · 鲁棒性与扰动诊断

<!-- AEE-TABLE:VLA-SIM-ROBUSTNESS:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 6 | **LIBERO-PRO** | 2025 | LIBERO 鲁棒性扩展：在物体、初始状态、指令、环境四维度施加扰动，诊断记忆化问题 | 扰动下成功率 | 267 | 2026-03 | [论文](https://arxiv.org/abs/2510.03827) · [代码](https://github.com/Zxy-MLlab/LIBERO-PRO) · [主页](https://zxy-mllab.github.io/LIBERO-PRO-Webpage/) |
| 7 | **LIBERO-Plus** | 2025 | LIBERO 鲁棒性基准：10030 个任务，覆盖相机、机器人初始状态、语言、光照、纹理、噪声、物体布局等七类扰动 | 按扰动维度统计的成功率 | 348 | 2026-01 | [论文](https://arxiv.org/abs/2510.13626) · [代码](https://github.com/sylvestf/LIBERO-plus) · [主页](https://sylvestf.github.io/LIBERO-plus) · [LeRobot](https://huggingface.co/docs/lerobot/main/libero_plus) |
| 8 | **VLA-Arena** | 2025 | 结构化动作模型评测：任务结构/语言/视觉三轴、170 任务（Safety/Distractor/Extrapolation/Long-Horizon） | 按难度等级（L0–L2）的成功率 | 178 | 2026-03 | [论文](https://arxiv.org/abs/2512.22539) · [代码](https://github.com/PKU-Alignment/VLA-Arena) · [主页](https://vla-arena.github.io/) |
| 9 | **THE COLOSSEUM** | 2024 | 机器人操作泛化评测：视觉/语义/执行多类扰动下的策略鲁棒性 | 成功率 | 149 | 2025-03 | [论文](https://arxiv.org/abs/2402.08191) · [代码](https://github.com/robot-colosseum/robot-colosseum) · [主页](https://robot-colosseum.github.io) |
<!-- AEE-TABLE:VLA-SIM-ROBUSTNESS:END -->

### 仿真 · 记忆与历史依赖

<!-- AEE-TABLE:VLA-SIM-MEMORY:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 10 | **LIBERO-Mem** | 2025 | 部分可观测操作中的对象级记忆：物体运动、顺序、关系与遮挡回忆 | 时间尺度压力测试下的成功率 | 22 | 2025-11 | [论文](https://arxiv.org/abs/2511.11478) · [代码](https://github.com/libero-mem/libero-mem) · [主页](https://libero-mem.github.io/) |
| 11 | **RoboMME** | 2026 | 记忆增强机器人操作：覆盖时间、空间、对象、程序性记忆四类任务套件 | 16 个任务上的成功率 | 113 | 2026-06 | [论文](https://arxiv.org/abs/2603.04639) · [代码](https://github.com/RoboMME/robomme_benchmark) · [主页](https://robomme.github.io/) · [排行榜](https://robomme.github.io/leaderboard.html) |
| 12 | **MIKASA-Robo-VLA** | 2026 | 面向动作模型的记忆密集桌面操作：90 个语言条件任务，覆盖 10 类记忆类型 | 按任务时长与记忆类型统计的成功率 | 112 | 2026-06 | [论文](https://arxiv.org/abs/2502.10550) · [代码](https://github.com/CognitiveAISystems/MIKASA-Robo) · [文档](https://mikasarobo.github.io/) |
<!-- AEE-TABLE:VLA-SIM-MEMORY:END -->

### 仿真 · 长程推理

<!-- AEE-TABLE:VLA-SIM-LONG-HORIZON:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 13 | **RoboCasa / RoboCasa365** | 2024/2026 | 大规模厨房场景日常操作评测，覆盖原子技能到长时程复合任务 | 各套件成功率 | 1.5k | 2026-05 | [论文](https://arxiv.org/abs/2406.02523) · [代码](https://github.com/robocasa/robocasa) |
| 14 | **VLABench** | 2024/2025 | 语言条件机器人操作：长程推理、隐式人类意图、世界知识迁移，覆盖 100 类任务与 2000+ 物体 | 成功率与能力维度分解 | 442 | 2025-11 | [论文](https://arxiv.org/abs/2412.18194) · [代码](https://github.com/OpenMOSS/VLABench) · [主页](https://vlabench.github.io/) |
| 15 | **RoboCerebra** | 2025 | 长程机器人操作：评测 System-2 高层规划、反思、记忆，以及 VLM planner 与动作 controller 的层级交互 | 任务成功率与推理/规划维度分解 | 65 | 2026-04 | [论文](https://arxiv.org/abs/2506.06677) · [代码](https://github.com/qiuboxiang/RoboCerebra) · [主页](https://robocerebra.github.io/) |
| 16 | **EmbodiedBench** | 2025 | MLLM 作为具身智能体：4 个仿真环境、1128 任务，覆盖高层语义与低层导航/操作 | 任务成功率 | 311 | 2026-05 | [论文](https://arxiv.org/abs/2502.09560) · [代码](https://github.com/EmbodiedBench/EmbodiedBench) · [主页](https://embodiedbench.github.io/) |
<!-- AEE-TABLE:VLA-SIM-LONG-HORIZON:END -->

### 仿真 · 通用任务与广义控制

<!-- AEE-TABLE:VLA-SIM-GENERALIST:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 17 | **RoboTwin 2.0** | 2025 | 双臂操作基准：50 任务、5 种机器人本体、强域随机化；社区动作模型评测常用（含 CVPR 挑战赛） | 任务成功率 | 2.5k | 2026-05 | [论文](https://arxiv.org/abs/2506.18088) · [代码](https://github.com/RoboTwin-Platform/RoboTwin) · [主页](https://robotwin-platform.github.io/) · [排行榜](https://robotwin-platform.github.io/leaderboard) |
| 18 | **RoboLab** | 2026 | 高保真 Isaac Lab 仿真基准：评测 DROID 训练的通用任务策略，120 任务覆盖视觉、程序、关系三类能力 | SR%、进度分、末端速度、EE SPARC | 307 | 2026-06 | [论文](https://arxiv.org/abs/2604.09860) · [代码](https://github.com/NVlabs/RoboLab) · [主页](https://research.nvidia.com/labs/srl/projects/robolab/) · [排行榜](https://research.nvidia.com/labs/srl/projects/robolab/leaderboard.html) |
| 19 | **Kinetix** | 2025 | 开放式 2D 物理控制任务；在 vla-eval 中作为广义控制与泛化压力测试 | 任务回报 / 成功率 | 258 | 2026-05 | [论文](https://arxiv.org/abs/2410.23208) · [主页](https://kinetix-env.github.io/) |
| 20 | **MolmoSpaces-Bench** | 2026 | 程序化生成空间中的零样本导航与操作基准，覆盖 pick/place/open/close/open-door 等任务 | 任务成功率 | 365 | 2026-06 | [论文](https://arxiv.org/abs/2602.11337) · [代码](https://github.com/allenai/molmospaces) · [主页](https://allenai.github.io/molmospaces/) |
<!-- AEE-TABLE:VLA-SIM-GENERALIST:END -->

### Sim-to-real 代理（real-to-sim）

<!-- AEE-TABLE:VLA-SIM2REAL:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 21 | **SimplerEnv** | 2024 | 真实机器人策略的 real-to-sim 评测（Google Robot、WidowX+Bridge） | 成功率、sim↔real 相关性（MMRV、Pearson r） | 1.1k | 2025-12 | [论文](https://arxiv.org/abs/2405.05946) · [代码](https://github.com/simpler-env/SimplerEnv) |
| 22 | **REALM** | 2025 | 经真机验证的 real-to-sim 泛化基准（DROID 本体；15 类扰动、7 类技能） | 成功率；sim↔real 相关性 | 60 | 2026-06 | [论文](https://arxiv.org/abs/2512.19562) · [代码](https://github.com/martin-sedlacek/REALM) · [主页](https://martin-sedlacek.com/realm/) |
<!-- AEE-TABLE:VLA-SIM2REAL:END -->

### 真机

<!-- AEE-TABLE:VLA-REAL:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 23 | **DROID** | 2024 | 真实 Franka 硬件上的 in-the-wild 操作评测；多场景泛化协议 | 成功率（同分布 / OOD） | 289 | 2025-04 | [论文](https://arxiv.org/abs/2403.12945) · [代码](https://github.com/droid-dataset/droid_policy_learning) · [主页](https://droid-dataset.github.io/) |
| 24 | **RoboArena** | 2025 | 分布式真机评测：在 DROID 机器人平台上通过双盲 pairwise comparison 排名通用机器人策略 | 成对偏好 / Elo 风格排名 | 104 | 2026-04 | [论文](https://arxiv.org/abs/2506.18123) · [代码](https://github.com/robo-arena/roboarena) · [主页](https://robo-arena.github.io/) |
| 25 | **VLA-REPLICA** | 2026 | 低成本可复现实验室真机动作模型基准：SO-101 机械臂、RGB-D 相机、标准化 ID/OOD 操作任务 | 真机成功率（ID / OOD） | — | — | [论文](https://arxiv.org/abs/2605.20774) · [主页](https://irvlutd.github.io/VLAReplica/) |
<!-- AEE-TABLE:VLA-REAL:END -->

常用框架：[vla-evaluation-harness](https://github.com/allenai/vla-evaluation-harness) 用 Docker 和统一协议运行上述多个基准。

## World Modeling 评测

世界模型基准按 **测什么维度** 分组：感知质量、世界生成、交互控制、具身下游效用、物理/指令一致性。

### 感知质量

<!-- AEE-TABLE:WM-PERCEPTUAL:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 1 | **VBench** | 2024 | 16 维视频生成质量评测（主体、运动、时序一致性等） | VBench 综合分 + 各维度分数 | 1.7k | 2026-03 | [论文](https://arxiv.org/abs/2311.17909) · [代码](https://github.com/Vchitect/VBench) · [主页](https://vchitect.github.io/VBench-project/) |
<!-- AEE-TABLE:WM-PERCEPTUAL:END -->

### 世界生成（3D/4D/T2V/I2V）

<!-- AEE-TABLE:WM-GENERATION:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 2 | **WorldScore** | 2025 | 统一的世界生成评测，覆盖 3D/4D/T2V/I2V；可控性、质量、动态性 | WorldScore（综合） | 284 | 2025-12 | [论文](https://arxiv.org/abs/2504.00983) · [主页](https://haoyi-duan.github.io/WorldScore/) |
| 3 | **4DWorldBench** | 2025/2026 | 3D/4D 世界生成能力评测：感知质量、条件对齐、物理真实性与时空一致性 | 多维综合评测 | — | — | [论文](https://arxiv.org/abs/2511.19836) |
<!-- AEE-TABLE:WM-GENERATION:END -->

### 交互式 / 多轮

<!-- AEE-TABLE:WM-INTERACTIVE:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 4 | **WBench** | 2026 | 多轮交互式视频世界模型评测（导航、主体动作、事件编辑、视角切换） | 5 维度共 22 项子指标 | 146 | 2026-06 | [论文](https://arxiv.org/abs/2605.25874) · [代码](https://github.com/meituan-longcat/WBench) · [主页](https://meituan-longcat.github.io/WBench/) |
<!-- AEE-TABLE:WM-INTERACTIVE:END -->

### 具身下游效用

<!-- AEE-TABLE:WM-EMBODIED:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 5 | **WorldArena** | 2026 | 感知质量 + 功能效用（数据引擎、策略评测、动作规划） | EWMScore（综合） | 220 | 2026-05 | [论文](https://arxiv.org/abs/2602.08971) · [主页](https://world-arena.ai/) |
| 6 | **RoboWM-Bench** | 2026 | 面向机器人操作的世界模型评测：将生成的人手/机器人视频转为可执行动作，并在仿真中验证任务完成 | 逐步可执行性与最终任务成功率 | 0 | 2026-05 | [论文](https://arxiv.org/abs/2604.19092) · [代码](https://github.com/flyingGH/RoboWM-Bench) · [主页](https://robowm-bench.github.io/RoboWM-Bench/) |
<!-- AEE-TABLE:WM-EMBODIED:END -->

### 物理一致性与指令遵循

<!-- AEE-TABLE:WM-PHYSICAL:START -->
| 序号 | 基准 | 年份 | 评什么 | 指标 | Stars | 最近更新 | 链接 |
|---|---|---|---|---|---|---|---|
| 7 | **WorldModelBench** | 2025 | 面向世界建模能力的评测：指令遵循、常识一致性、物理一致性 | 综合世界建模分数 | 41 | 2025-07 | [论文](https://arxiv.org/abs/2502.20694) · [代码](https://github.com/WorldModelBench-Team/WorldModelBench) |
| 8 | **EWMBench** | 2025 | 具身世界模型：场景一致性、运动正确性、语义对齐 | 各维度分数 | 126 | 2025-06 | [代码](https://github.com/AgibotTech/EWMBench) |
| 9 | **MiraBench** | 2026 | 机器人世界模型的动作条件可靠性：物理遵循、动作跟随一致性与成功幻觉/乐观偏差检测 | 物理遵循分、动作跟随一致性、乐观偏差分 | — | — | [论文](https://arxiv.org/abs/2605.29360) · [数据集](https://huggingface.co/datasets/Anonymous-nips-submissions/Anonymous-nips-submissions) |
<!-- AEE-TABLE:WM-PHYSICAL:END -->

## 相关清单

- [awesome-vla-wam](https://github.com/DravenALG/awesome-vla-wam) —— VLA 与世界动作模型（WAM）。
- [Awesome-World-Action-Model](https://github.com/HyperbolicCurve/Awesome-World-Action-Model) —— 动作模型相关论文、数据集与基准，包含 WAM/VLA。
- [awesome-embodied-vla-va-vln](https://github.com/jonyzhang2023/awesome-embodied-vla-va-vln) —— VLA / VA / VLN 模型与仿真器。

## 贡献指南

欢迎提 PR。新增条目时，请附带：

- 论文与官方代码链接。
- 生态状态：数据 / 任务、评测协议、leaderboard 是否公开或缺失。
- 任务设置、输入/输出格式，以及主要指标。
- 如果有，给一条最小运行命令。
- 你遇到过的复现坑（坐标约定、归一化统计、模糊的终止规则等）。

新增条目请在 `data/benchmarks.yaml` 中分配**能力内唯一、递增的 `seq`**（表格第一列序号；Reasoning & Planning / Action / World Modeling 各自从 1 开始）；手工批量添加后运行 `python scripts/render_readme.py --assign-seq` 再渲染 README。

## 许可证

[MIT](LICENSE)
