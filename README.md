# Awesome Embodied Evaluation [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![简体中文](https://img.shields.io/badge/lang-简体中文-lightgrey.svg)](README_CN.md)

A curated list of **benchmarks and evaluation methods** for embodied foundation models, spanning three tracks: **Vision-Language Models (VLM)**, **Vision-Language-Action models (VLA)**, and **World Models (WM)**.

Most existing lists cover only one track. This repo puts all three in one place and focuses on **how each benchmark is actually evaluated** — task setup, inputs/outputs, metrics, and what it takes to reproduce the numbers.

Contributions are welcome. See [Contributing](#contributing).

## Contents

- [Scope](#scope)
- [How Entries Are Organized](#how-entries-are-organized)
- [VLM Evaluation](#vlm-evaluation)
- [VLA Evaluation](#vla-evaluation)
- [World Model Evaluation](#world-model-evaluation)
- [Related Lists](#related-lists)
- [Contributing](#contributing)
- [License](#license)

## Scope

This list focuses on evaluation for embodied foundation models:

- **VLM** — multimodal understanding and reasoning.
- **VLA** — language-conditioned robot manipulation and control.
- **WM** — perceptual quality and downstream usefulness of world models.

We prioritize **authoritative, widely-adopted** benchmarks — those with strong community traction (high stars) and a **complete ecosystem** (official code, an active leaderboard, and a reproducible protocol).

For the **Embodied VLM Primary** table specifically, we only include benchmarks whose task objective is directly embodied (spatial grounding, embodied planning, physical reasoning, or environment-level embodied QA). General multimodal benchmarks are kept in the Control Set.

Out of scope: pure navigation/language-only benchmarks (unless tied to embodied evaluation), and paper collections without a concrete evaluation protocol.

## How Entries Are Organized

Each entry lists the paper, the official code, the main metric, and notes on reproducibility. Where useful, entries also note the input/output format, the evaluator (rule-based, simulator, VLM-as-judge, or human), and the generalization setting (in-distribution, OOD, or sim-to-real).

Tables are further split by **capability axis** (VLM), **evaluation environment** (VLA: simulation / sim-to-real / real robot), or **world-model dimension** (WM). See `data/benchmarks.yaml` for the taxonomy fields (`vlm_category`, `vla_env`, `wm_category`).

The **Stars** and **Updated** columns are refreshed automatically **twice a week** (Monday and Thursday) by a GitHub Actions workflow, so the popularity and activity signals stay current. Every other field is curated by hand.

The same workflow can also propose newly discovered benchmark entries across VLM / VLA / WM via an automated PR. Rather than scraping README text, discovery anchors each candidate on its **arXiv paper** (the paper title becomes the canonical name, plus year and abstract) and applies strict guards: an official code repo, a star threshold, embodied-relevance keyword hits, and a survey/awesome-list filter so paper collections are rejected. When an LLM is configured, it makes the final "is this a real benchmark?" call and writes the *What it tests* / *Metric* summaries; otherwise deterministic rules are used. All auto-insertions land in a reviewable PR before merge.

## VLM Evaluation

We split VLM evaluation into two layers:

- **Embodied VLM Benchmarks (Primary)**: directly evaluate embodied capabilities (spatial grounding, planning, physical understanding, environment-level QA).
- **General VLM Benchmarks (Control Set)**: track broad multimodal competence so gains on embodied tasks are not traded for general capability regressions.

### Embodied VLM Benchmarks (Primary)

#### Spatial grounding & 3D scene understanding

<!-- AEE-TABLE:VLM-PRIMARY-SPATIAL:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **Where2Place** | 2024 | Spatial free-space reference: language-conditioned placement in cluttered real scenes | Point accuracy | 224 | 2025-07 | [Paper](https://arxiv.org/abs/2406.10721) · [Code](https://github.com/wentaoyuan/RoboPoint) · [Dataset](https://huggingface.co/datasets/wentao-yuan/where2place) |
| **RefSpatial-Bench** | 2025 | Multi-step spatial referring and placement reasoning in complex 3D scenes | Accuracy (Location / Placement) | 263 | 2025-12 | [Paper](https://arxiv.org/abs/2506.04308) · [Code](https://github.com/Zhoues/RoboRefer) · [Site](https://zhoues.github.io/RoboRefer/) |
| **VSI-Bench** | 2025 | Egocentric video-based visual-spatial intelligence (configurational, measurement, spatiotemporal) | Accuracy / MRA | 726 | 2025-08 | [Paper](https://arxiv.org/abs/2412.14171) · [Code](https://github.com/vision-x-nyu/thinking-in-space) · [Dataset](https://huggingface.co/datasets/nyu-visionx/VSI-Bench) |
| **EmbSpatial-Bench** | 2024 | Egocentric spatial relationships (above/below/left/right/close/far) in embodied 3D scenes | Accuracy | 31 | 2024-06 | [Paper](https://arxiv.org/abs/2406.05756) · [Code](https://github.com/mengfeidu/EmbSpatial-Bench) · [Dataset](https://huggingface.co/datasets/Phineas476/EmbSpatial-Bench) |
<!-- AEE-TABLE:VLM-PRIMARY-SPATIAL:END -->

#### Planning & next-step reasoning

<!-- AEE-TABLE:VLM-PRIMARY-PLANNING:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **EgoPlan-Bench2** | 2024 | Egocentric real-world planning across daily scenarios and long-horizon task progress | Accuracy | 31 | 2025-04 | [Paper](https://arxiv.org/abs/2412.04447) · [Code](https://github.com/qiulu66/EgoPlan-Bench2/) · [Site](https://qiulu66.github.io/egoplanbench2/) |
<!-- AEE-TABLE:VLM-PRIMARY-PLANNING:END -->

#### Embodied question answering

<!-- AEE-TABLE:VLM-PRIMARY-QA:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **OpenEQA** | 2024 | Embodied question answering with episodic-memory and active-exploration settings | LLM-judge score / answer quality | 365 | 2024-09 | [Paper](https://openaccess.thecvf.com/content/CVPR2024/html/Majumdar_OpenEQA_Embodied_Question_Answering_in_the_Era_of_Foundation_Models_CVPR_2024_paper.html) · [Code](https://github.com/facebookresearch/open-eqa) · [Site](https://open-eqa.github.io/) |
<!-- AEE-TABLE:VLM-PRIMARY-QA:END -->

#### Physical reasoning

<!-- AEE-TABLE:VLM-PRIMARY-PHYSICAL:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **PhysBench** | 2025 | Physical-world understanding for embodied agents (object physics, relations, scene dynamics) | Accuracy across physical dimensions | 91 | 2026-01 | [Paper](https://arxiv.org/abs/2501.16411) · [Code](https://github.com/physical-superintelligence-lab/PhysBench) · [Site](https://physbench.github.io/) |
<!-- AEE-TABLE:VLM-PRIMARY-PHYSICAL:END -->

#### Embodied reasoning (multimodal QA)

<!-- AEE-TABLE:VLM-PRIMARY-REASONING:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **ERQA** | 2025 | Multimodal embodied reasoning QA (spatial reasoning, world knowledge) in real-world robotic scenarios | Accuracy (MCQ) | 275 | 2025-03 | [Report](https://storage.googleapis.com/deepmind-media/gemini-robotics/gemini_robotics_report.pdf) · [Code](https://github.com/embodiedreasoning/ERQA) |
<!-- AEE-TABLE:VLM-PRIMARY-REASONING:END -->

### General VLM Benchmarks (Control Set)

#### Reasoning

<!-- AEE-TABLE:VLM-CONTROL-REASONING:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **MMMU** | 2023 | College-level, multi-discipline multimodal reasoning (30 subjects, heterogeneous image types) | Accuracy | 576 | 2026-02 | [Paper](https://arxiv.org/abs/2311.16502) · [Code](https://github.com/MMMU-Benchmark/MMMU) · [Site](https://mmmu-benchmark.github.io/) |
| **MathVista** | 2023 | Mathematical reasoning in visual contexts (charts, geometry, figures) | Accuracy | 363 | 2025-09 | [Paper](https://arxiv.org/abs/2310.02255) · [Code](https://github.com/lupantech/MathVista) |
<!-- AEE-TABLE:VLM-CONTROL-REASONING:END -->

#### Perception & understanding

<!-- AEE-TABLE:VLM-CONTROL-PERCEPTION:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **MMBench** | 2023 | Fine-grained, multi-ability understanding with CircularEval; EN/ZH | Accuracy | 303 | 2025-05 | [Paper](https://arxiv.org/abs/2307.06281) · [Code](https://github.com/open-compass/MMBench) |
| **SEED-Bench series** | 2023-2024 | Broad multimodal capability coverage (image/video, generation-oriented comprehension, text-rich understanding) | Accuracy | 364 | 2025-01 | [Paper](https://arxiv.org/abs/2307.16125) · [Code](https://github.com/AILab-CVC/SEED-Bench) |
<!-- AEE-TABLE:VLM-CONTROL-PERCEPTION:END -->

#### Video understanding

<!-- AEE-TABLE:VLM-CONTROL-VIDEO:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **Video-MME / Video-MME-v2** | 2024/2026 | Comprehensive video understanding, with v2 targeting robustness, consistency, and reasoning faithfulness | Accuracy / Group-based score (v2) | 779 | 2025-12 | [Paper v1](https://arxiv.org/abs/2405.21075) · [Code v1](https://github.com/MME-Benchmarks/Video-MME) · [Paper v2](https://arxiv.org/abs/2604.05015) · [Code v2](https://github.com/MME-Benchmarks/Video-MME-v2) |
<!-- AEE-TABLE:VLM-CONTROL-VIDEO:END -->

#### Document understanding

<!-- AEE-TABLE:VLM-CONTROL-DOCUMENT:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **DocVQA (RRC track)** | 2020-ongoing | Document visual question answering and document reasoning under challenge protocol | ANLS / Accuracy | — | — | [Paper](https://arxiv.org/abs/2007.00398) · [RRC](https://rrc.cvc.uab.es/) |
<!-- AEE-TABLE:VLM-CONTROL-DOCUMENT:END -->

Common toolkit: [VLMEvalKit](https://github.com/open-compass/VLMEvalKit) provides standardized evaluation for the benchmarks above and 80+ others.

## VLA Evaluation

VLA benchmarks are grouped by **where the policy is evaluated**: closed-loop simulation, real-to-sim proxy, or real hardware.

### Simulation (closed-loop)

<!-- AEE-TABLE:VLA-SIM:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **LIBERO** | 2023 | Lifelong / language-conditioned tabletop manipulation (Spatial, Object, Goal, Long suites) | Success rate | 2.0k | 2025-03 | [Paper](https://arxiv.org/abs/2306.03310) · [Code](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| **LIBERO-PRO** | 2025 | Robust LIBERO extension with perturbations on objects, initial states, instructions, and environments | Success rate under perturbations | 267 | 2026-03 | [Paper](https://arxiv.org/abs/2510.03827) · [Code](https://github.com/Zxy-MLlab/LIBERO-PRO) · [Site](https://zxy-mllab.github.io/LIBERO-PRO-Webpage/) |
| **CALVIN** | 2021 | Long-horizon instruction chaining; compositional generalization (ABC→D) | Avg. completed chain length | 942 | 2025-09 | [Paper](https://arxiv.org/abs/2112.03227) · [Code](https://github.com/mees/calvin) |
| **RoboTwin 2.0** | 2025 | Dual-arm manipulation benchmark with domain randomization; 50 tasks, 5 robot embodiments, sim-to-real protocol | Task success rate | 2.5k | 2026-05 | [Paper](https://arxiv.org/abs/2506.18088) · [Code](https://github.com/RoboTwin-Platform/RoboTwin) · [Site](https://robotwin-platform.github.io/) · [Leaderboard](https://robotwin-platform.github.io/leaderboard) |
| **VLA-Arena** | 2025 | Structured VLA eval across task structure, language, and vision axes (170 tasks; Safety/Distractor/Extrapolation/Long-Horizon) | Success rate by difficulty level (L0–L2) | 178 | 2026-03 | [Paper](https://arxiv.org/abs/2512.22539) · [Code](https://github.com/PKU-Alignment/VLA-Arena) · [Site](https://vla-arena.github.io/) |
| **THE COLOSSEUM** | 2024 | Generalization in robotic manipulation under visual/semantic/execution perturbations | Success rate | 150 | 2025-03 | [Paper](https://arxiv.org/abs/2402.08191) · [Code](https://github.com/robot-colosseum/robot-colosseum) · [Site](https://robot-colosseum.github.io) |
| **RLBench** | 2020 | 100+ language-conditioned manipulation tasks in CoppeliaSim (Franka Panda); widely used VLA baseline | Success rate | 1.8k | 2025-01 | [Paper](https://arxiv.org/abs/1909.12271) · [Code](https://github.com/stepjam/RLBench) |
| **ManiSkill2** | 2023 | Generalizable manipulation across diverse objects / skills with high-throughput simulation | Task success / reward-based scores | 1 | 2023-08 | [Paper](https://arxiv.org/abs/2302.04659) · [Code](https://github.com/haosulab/ManiSkill2-task-dev) |
| **BEHAVIOR-1K** | 2024 | Long-horizon, human-centered household activities with realistic simulation dynamics | Activity success / completion metrics | 1.5k | 2026-06 | [Paper](https://arxiv.org/abs/2403.09227) · [Code](https://github.com/StanfordVL/BEHAVIOR-1K) |
| **RoboCasa / RoboCasa365** | 2024/2026 | Large-scale everyday kitchen manipulation, from atomic skills to long-horizon composites | Success rate across benchmark suites | 1.5k | 2026-05 | [Paper](https://arxiv.org/abs/2406.02523) · [Code](https://github.com/robocasa/robocasa) |
| **EmbodiedBench** | 2025 | MLLM-as-agent eval across 1,128 tasks in 4 sim environments (high/low-level; 6 capability subsets) | Task success rate | 311 | 2026-05 | [Paper](https://arxiv.org/abs/2502.09560) · [Code](https://github.com/EmbodiedBench/EmbodiedBench) · [Site](https://embodiedbench.github.io/) |
<!-- AEE-TABLE:VLA-SIM:END -->

### Sim-to-real proxy (real-to-sim)

<!-- AEE-TABLE:VLA-SIM2REAL:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **SimplerEnv** | 2024 | Real-to-sim evaluation of real-robot policies (Google Robot, WidowX+Bridge) | Success rate, sim↔real correlation (MMRV, Pearson r) | 1.1k | 2025-12 | [Paper](https://arxiv.org/abs/2405.05946) · [Code](https://github.com/simpler-env/SimplerEnv) |
| **REALM** | 2025 | Real-to-sim validated generalization benchmark (DROID embodiment; 15 perturbations, 7 skills) | Success rate; sim↔real correlation | 58 | 2026-06 | [Paper](https://arxiv.org/abs/2512.19562) · [Code](https://github.com/martin-sedlacek/REALM) · [Site](https://martin-sedlacek.com/realm/) |
<!-- AEE-TABLE:VLA-SIM2REAL:END -->

### Real robot

<!-- AEE-TABLE:VLA-REAL:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **DROID** | 2024 | In-the-wild Franka manipulation eval on real hardware; multi-scene generalization protocol | Success rate (ID / OOD) | 289 | 2025-04 | [Paper](https://arxiv.org/abs/2403.12945) · [Code](https://github.com/droid-dataset/droid_policy_learning) · [Site](https://droid-dataset.github.io/) |
<!-- AEE-TABLE:VLA-REAL:END -->

Common harness: [vla-evaluation-harness](https://github.com/allenai/vla-evaluation-harness) runs many of these benchmarks in Docker with a shared protocol.

## World Model Evaluation

World-model benchmarks are grouped by **what aspect of a world model is measured**: perceptual quality, world generation, interactive control, embodied downstream utility, or physical / instruction adherence.

### Perceptual quality

<!-- AEE-TABLE:WM-PERCEPTUAL:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **VBench** | 2024 | 16-dimension video generation quality (subject, motion, temporal consistency, etc.) | VBench composite + per-dimension scores | 1.7k | 2026-03 | [Paper](https://arxiv.org/abs/2311.17909) · [Code](https://github.com/Vchitect/VBench) · [Site](https://vchitect.github.io/VBench-project/) |
<!-- AEE-TABLE:WM-PERCEPTUAL:END -->

### World generation (3D/4D/T2V/I2V)

<!-- AEE-TABLE:WM-GENERATION:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **WorldScore** | 2025 | Unified world generation across 3D/4D/T2V/I2V; controllability, quality, dynamics | WorldScore (composite) | 284 | 2025-12 | [Paper](https://arxiv.org/abs/2504.00983) · [Site](https://haoyi-duan.github.io/WorldScore/) |
| **4DWorldBench** | 2025/2026 | 3D/4D world generation realism: perceptual quality, condition alignment, physics, and consistency | Multi-dimension composite evaluation | — | — | [Paper](https://arxiv.org/abs/2511.19836) |
<!-- AEE-TABLE:WM-GENERATION:END -->

### Interactive / multi-turn

<!-- AEE-TABLE:WM-INTERACTIVE:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **WBench** | 2026 | Multi-turn interactive video world models (navigation, subject action, event editing, perspective switch) | 22 sub-metrics across 5 dimensions | 144 | 2026-06 | [Paper](https://arxiv.org/abs/2605.25874) · [Code](https://github.com/meituan-longcat/WBench) · [Site](https://meituan-longcat.github.io/WBench/) |
<!-- AEE-TABLE:WM-INTERACTIVE:END -->

### Embodied downstream utility

<!-- AEE-TABLE:WM-EMBODIED:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **WorldArena** | 2026 | Perceptual quality + functional utility (data engine, policy eval, action planning) | EWMScore (composite) | 220 | 2026-05 | [Paper](https://arxiv.org/abs/2602.08971) · [Site](https://world-arena.ai/) |
<!-- AEE-TABLE:WM-EMBODIED:END -->

### Physical consistency & instruction adherence

<!-- AEE-TABLE:WM-PHYSICAL:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **WorldModelBench** | 2025 | World modeling capability under instruction following, commonsense, and physical adherence | Composite world-modeling scores | 41 | 2025-07 | [Paper](https://arxiv.org/abs/2502.20694) · [Code](https://github.com/WorldModelBench-Team/WorldModelBench) |
| **EWMBench** | 2025 | Embodied world models: scene consistency, motion correctness, semantic alignment | Per-dimension scores | 126 | 2025-06 | [Code](https://github.com/AgibotTech/EWMBench) |
<!-- AEE-TABLE:WM-PHYSICAL:END -->

## Related Lists

- [awesome-vla-wam](https://github.com/DravenALG/awesome-vla-wam) — VLA and World Action Models.
- [Awesome-World-Action-Model](https://github.com/HyperbolicCurve/Awesome-World-Action-Model) — papers, datasets, and benchmarks for WAM/VLA.
- [awesome-embodied-vla-va-vln](https://github.com/jonyzhang2023/awesome-embodied-vla-va-vln) — VLA / VA / VLN models and simulators.

## Contributing

Pull requests are welcome. For a new entry, please include:

- Links to the paper and the official code.
- Task setup, input/output format, and the main metric.
- A minimal run command, if you have one.
- Any reproducibility caveats you ran into (coordinate conventions, normalization stats, ambiguous termination rules, etc.).

Keep one entry per row and place it in the matching track table.

## License

[MIT](LICENSE)
