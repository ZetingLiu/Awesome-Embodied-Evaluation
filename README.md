# Awesome Embodied Evaluation

> A curated list of **VLM / VLA / World Model** evaluation methods, benchmarks, protocols, and tooling for embodied AI.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Why This Repo

现有仓库通常只覆盖单条线（只做 VLM、只做 VLA、或只做 World Model）。  
本仓库目标是做一个统一入口：**把 VLM-VLA-WM 三条评测线放进同一个评测视角里**，并强调可复现协议。

---

## Scope

- **VLM Evaluation**: 多模态理解与推理能力评测
- **VLA Evaluation**: 语言条件机器人操作能力评测
- **World Model Evaluation**: 世界模型感知质量与功能效用评测

不包含：
- 纯导航/纯语言 benchmark（除非与 embodied 评测直接相关）
- 仅论文列表、无评测定义的“模型盘点”

---

## Taxonomy: 汇总维度（建议标准）

建议每个 benchmark / 方法都按以下维度记录，便于横向对比：

1. **Task Level**：感知 / 推理 / 操作 / 规划 / 长时序
2. **Embodiment Level**：offline QA、open-loop rollout、closed-loop control
3. **Input Modality**：image / video / language / state / action / tactile
4. **Output Type**：MCQ、free-form text、point/box、action trajectory、success signal
5. **Metrics**：accuracy、success rate、chain length、correlation、human preference、composite score
6. **Generalization Axis**：IID / OOD / cross-task / cross-scene / sim2real
7. **Evaluator Type**：rule-based、simulator-based、VLM-as-judge、human
8. **Reproducibility**：官方代码、docker、checkpoint、seed、protocol 是否齐全
9. **Cost Profile**：GPU/CPU、数据规模、单次评测耗时
10. **License & Access**：开源许可、数据是否需申请、是否可商用

---

## Recommended Canonical Fields

建议在后续 PR 中统一成如下字段：

| Field | Description |
|---|---|
| Name | Benchmark / Eval Method 名称 |
| Track | VLM / VLA / WM |
| Year | 发布年份 |
| Task & Setting | 任务定义与场景（offline / sim / real） |
| Input -> Output | 输入输出格式 |
| Metric | 主指标 |
| Official Repo | 官方仓库 |
| Paper | 论文链接 |
| Reproducibility | Code/Data/Checkpoint/Protocol 完整度 |
| Notes | 复现坑点、评测注意事项 |

---

## Quick Start: 先放每条线 3 个权威代表工作

> 目标：先有一个最小可用版本（MVP），后续再扩到全面列表。

### 1) VLM Evaluation (Top 3)

- **MMMU**  
  - Paper: https://arxiv.org/abs/2311.16502  
  - Repo: https://github.com/MMMU-Benchmark/MMMU  
  - Why: 专家级多学科多模态推理主流基准，长期被主流 VLM 报告。

- **MMBench**  
  - Paper: https://arxiv.org/abs/2307.06281  
  - Repo: https://github.com/open-compass/MMBench  
  - Why: 中文/英文多维细粒度评估，工程上与 OpenCompass 生态结合紧密。

- **MathVista**  
  - Paper: https://arxiv.org/abs/2310.02255  
  - Repo: https://github.com/lupantech/MathVista  
  - Why: 视觉数学推理代表 benchmark，能有效拉开模型复杂推理能力差异。

### 2) VLA Evaluation (Top 3)

- **LIBERO**  
  - Paper: https://arxiv.org/abs/2306.03310  
  - Repo: https://github.com/Lifelong-Robot-Learning/LIBERO  
  - Why: VLA 操作评测事实标准之一，几乎是主流论文必报项。

- **CALVIN**  
  - Paper: https://arxiv.org/abs/2112.03227  
  - Repo: https://github.com/mees/calvin  
  - Why: 长时序 instruction chaining 代表基准，强调组合泛化。

- **SimplerEnv (SIMPLER)**  
  - Paper: https://arxiv.org/abs/2405.05946  
  - Repo: https://github.com/simpler-env/SimplerEnv  
  - Why: 强调 sim-to-real 评测相关性（如相关性指标），是离线策略评估关键补充。

### 3) World Model Evaluation (Top 3)

- **WorldArena**  
  - Paper: https://arxiv.org/abs/2602.08971  
  - Website: https://world-arena.ai/  
  - Why: 同时看感知质量和功能效用（data engine / policy eval / action planning）。

- **WorldScore**  
  - Paper: https://arxiv.org/abs/2504.00983  
  - Website: https://haoyi-duan.github.io/WorldScore/  
  - Why: 提供统一 world generation 评测框架，覆盖 controllability/quality/dynamics。

- **EWMBench**  
  - Repo: https://github.com/AgibotTech/EWMBench  
  - Why: 聚焦 embodied world model 的 scene/motion/semantic 三维评测，工程可落地性较强。

---

## Existing Repos Closest to This Goal (Reference)

- https://github.com/DravenALG/awesome-vla-wam
- https://github.com/HyperbolicCurve/Awesome-World-Action-Model
- https://github.com/jonyzhang2023/awesome-embodied-vla-va-vln

本仓库差异化目标：**不仅列资源，还要统一评测字段与协议可复现信息**。

---

## Contribution Guide (Draft)

欢迎 PR，建议每个新增条目附带：

- 官方 repo + paper
- 任务定义、输入输出、主指标
- 最小复现命令（可选）
- 你踩过的复现坑（建议）

PR 标题建议：
- `add(vlm): MMMU protocol notes`
- `add(vla): LIBERO reproducibility checklist`
- `add(wm): WorldArena evaluator details`

---

## License

MIT
