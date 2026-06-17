# Awesome Embodied Evaluation [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![简体中文](https://img.shields.io/badge/lang-简体中文-lightgrey.svg)](README_CN.md)

A curated list of **benchmarks and evaluation methods** for unified / omni embodied models, spanning three core capabilities: **Reasoning & Planning**, **Action**, and **World Modeling**.

Most existing lists cover only one or two capabilities. This repo puts all three in one place and focuses on **how each benchmark is actually evaluated** — task setup, inputs/outputs, metrics, and what it takes to reproduce the numbers.

Contributions are welcome. See [Contributing](#contributing).

## Contents

- [Scope](#scope)
- [How Entries Are Organized](#how-entries-are-organized)
- [Ecosystem Completeness](#ecosystem-completeness)
- [Reasoning & Planning Evaluation](#reasoning--planning-evaluation)
- [Action Evaluation](#action-evaluation)
- [World Modeling Evaluation](#world-modeling-evaluation)
- [Related Lists](#related-lists)
- [Contributing](#contributing)
- [License](#license)

## Scope

This list focuses on evaluation for unified / omni embodied models across three core capabilities:

- **Reasoning & Planning** — multimodal perception, spatial / physical reasoning, embodied QA, task planning, and next-step prediction.
- **Action** — action-generating embodied policies for simulation and real-robot control, including VLA models and world-action models.
- **World Modeling** — predictive or generative models of environment dynamics, physical consistency, controllability, and downstream utility.

We prioritize **authoritative, widely-adopted** benchmarks — those with strong community traction (high stars) and a **complete ecosystem** (official code, an active leaderboard, and a reproducible protocol).

For the **Reasoning & Planning Primary** table specifically, we only include benchmarks whose task objective is directly embodied (spatial grounding, embodied planning, physical reasoning, or environment-level embodied QA). General multimodal benchmarks are kept in the Control Set.

Out of scope: pure navigation/language-only benchmarks (unless tied to embodied evaluation), and paper collections without a concrete evaluation protocol.

## How Entries Are Organized

Each entry lists the paper, the official code, the main metric, and notes on reproducibility. Where useful, entries also note the input/output format, the evaluator (rule-based, simulator, VLM-as-judge, or human), and the generalization setting (in-distribution, OOD, or sim-to-real).

Tables are further split by **reasoning / planning capability axis**, **action evaluation environment** (simulation / sim-to-real / real robot), or **world-modeling dimension**. See `data/benchmarks.yaml` for the taxonomy fields (`vlm_category`, `vla_env`, `wm_category`).

The **Stars** and **Updated** columns come from GitHub repository metadata and are refreshed manually by maintainers when the tables are updated. Every other field is curated by hand.

## Ecosystem Completeness

This list treats ecosystem completeness as a practical reproducibility signal. When adding or reviewing entries, maintainers check whether the benchmark provides:

- **Paper**: a peer-reviewed paper, arXiv preprint, or technical report.
- **Code**: official evaluation code, a harness, or runnable scripts.
- **Data / Tasks**: public datasets, simulator assets, task definitions, or benchmark splits.
- **Protocol**: documented metrics, prompts, scoring rules, splits, or submission format.
- **Leaderboard**: a public leaderboard, standardized submission path, or active challenge.

Benchmarks with missing components can still be included when they are important, but the gap should be visible in the entry links or description and revisited during maintenance.

## Reasoning & Planning Evaluation

We split reasoning & planning evaluation into two layers:

- **Embodied Reasoning & Planning Benchmarks (Primary)**: directly evaluate embodied capabilities (spatial grounding, planning, physical understanding, environment-level QA).
- **General Multimodal Benchmarks (Control Set)**: track broad multimodal competence so gains on embodied tasks are not traded for general capability regressions.

### Embodied Reasoning & Planning Benchmarks (Primary)

#### Spatial grounding & 3D scene understanding

<!-- AEE-TABLE:VLM-PRIMARY-SPATIAL:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 1 | **Where2Place** | 2024 | Spatial free-space reference: language-conditioned placement in cluttered real scenes | Point accuracy | 224 | 2025-07 | [Paper](https://arxiv.org/abs/2406.10721) · [Code](https://github.com/wentaoyuan/RoboPoint) · [Dataset](https://huggingface.co/datasets/wentao-yuan/where2place) |
| 2 | **EmbSpatial-Bench** | 2024 | Egocentric spatial relationships (above/below/left/right/close/far) in embodied 3D scenes | Accuracy | 31 | 2024-06 | [Paper](https://arxiv.org/abs/2406.05756) · [Code](https://github.com/mengfeidu/EmbSpatial-Bench) · [Dataset](https://huggingface.co/datasets/Phineas476/EmbSpatial-Bench) |
| 3 | **RefSpatial-Bench** | 2025 | Multi-step spatial referring and placement reasoning in complex 3D scenes | Accuracy (Location / Placement) | 263 | 2025-12 | [Paper](https://arxiv.org/abs/2506.04308) · [Code](https://github.com/Zhoues/RoboRefer) · [Site](https://zhoues.github.io/RoboRefer/) |
| 4 | **VSI-Bench** | 2025 | Egocentric video-based visual-spatial intelligence (configurational, measurement, spatiotemporal) | Accuracy / MRA | 726 | 2025-08 | [Paper](https://arxiv.org/abs/2412.14171) · [Code](https://github.com/vision-x-nyu/thinking-in-space) · [Dataset](https://huggingface.co/datasets/nyu-visionx/VSI-Bench) |
| 5 | **ESI-Bench** | 2026 | Embodied spatial intelligence with active perception, locomotion, and manipulation across 10 categories and 29 subcategories | Accuracy under passive / active / oracle observation settings | 107 | 2026-06 | [Paper](https://arxiv.org/abs/2605.18746) · [Code](https://github.com/ESI-Bench/ESI-Bench) · [Site](https://esi-bench.github.io/) · [Dataset](https://huggingface.co/datasets/ESI-Bench/esi-bench) |
<!-- AEE-TABLE:VLM-PRIMARY-SPATIAL:END -->

#### Planning & next-step reasoning

<!-- AEE-TABLE:VLM-PRIMARY-PLANNING:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 6 | **EgoPlan-Bench2** | 2024 | Egocentric real-world planning across daily scenarios and long-horizon task progress | Accuracy | 31 | 2025-04 | [Paper](https://arxiv.org/abs/2412.04447) · [Code](https://github.com/qiulu66/EgoPlan-Bench2/) · [Site](https://qiulu66.github.io/egoplanbench2/) |
| 7 | **GroundedPlanBench** | 2026 | Spatially grounded long-horizon action planning in real-world manipulation scenes | Task success rate / action recall rate / spatial grounding accuracy | — | — | [Paper](https://arxiv.org/abs/2603.13433) · [Microsoft Research](https://www.microsoft.com/en-us/research/blog/groundedplanbench-spatially-grounded-long-horizon-task-planning-for-robot-manipulation/) · [Site](https://groundedplanning.github.io/GroundedPlanning/) |
<!-- AEE-TABLE:VLM-PRIMARY-PLANNING:END -->

#### Embodied question answering

<!-- AEE-TABLE:VLM-PRIMARY-QA:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 8 | **OpenEQA** | 2024 | Embodied question answering with episodic-memory and active-exploration settings | LLM-judge score / answer quality | 365 | 2024-09 | [Paper](https://openaccess.thecvf.com/content/CVPR2024/html/Majumdar_OpenEQA_Embodied_Question_Answering_in_the_Era_of_Foundation_Models_CVPR_2024_paper.html) · [Code](https://github.com/facebookresearch/open-eqa) · [Site](https://open-eqa.github.io/) |
<!-- AEE-TABLE:VLM-PRIMARY-QA:END -->

#### Physical reasoning

<!-- AEE-TABLE:VLM-PRIMARY-PHYSICAL:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 9 | **PhysBench** | 2025 | Physical-world understanding for embodied agents (object physics, relations, scene dynamics) | Accuracy across physical dimensions | 91 | 2026-01 | [Paper](https://arxiv.org/abs/2501.16411) · [Code](https://github.com/physical-superintelligence-lab/PhysBench) · [Site](https://physbench.github.io/) |
| 10 | **KinDER** | 2026 | Kinematic and dynamic embodied reasoning across 25 procedurally generated robot environments | Success / reward / benchmark scores across TAMP, RL, IL, and foundation-model baselines | 35 | 2026-06 | [Paper](https://arxiv.org/abs/2604.25788) · [Code](https://github.com/Princeton-Robot-Planning-and-Learning/kindergarden) · [Site](https://prpl-group.com/kinder-site/) · [Baselines](https://github.com/Princeton-Robot-Planning-and-Learning/kinder-baselines) |
<!-- AEE-TABLE:VLM-PRIMARY-PHYSICAL:END -->

#### Embodied reasoning (multimodal QA)

<!-- AEE-TABLE:VLM-PRIMARY-REASONING:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 11 | **ERQA** | 2025 | Multimodal embodied reasoning QA (spatial reasoning, world knowledge) in real-world robotic scenarios | Accuracy (MCQ) | 275 | 2025-03 | [Report](https://storage.googleapis.com/deepmind-media/gemini-robotics/gemini_robotics_report.pdf) · [Code](https://github.com/embodiedreasoning/ERQA) |
| 12 | **ERIQ** | 2025/2026 | Embodied reasoning independent of motor execution: spatial perception, planning, error recovery, and human intent | Accuracy over multiple-choice and binary QA | 15 | 2026-01 | [Paper](https://arxiv.org/abs/2512.24125) · [Code](https://github.com/GenieReasoner/ERIQ) · [Dataset](https://huggingface.co/datasets/KineMind/ERIQ) · [Site](https://geniereasoner.github.io/GenieReasoner/) |
<!-- AEE-TABLE:VLM-PRIMARY-REASONING:END -->

### General Multimodal Benchmarks (Control Set)

#### Reasoning

<!-- AEE-TABLE:VLM-CONTROL-REASONING:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 13 | **MMMU** | 2023 | College-level, multi-discipline multimodal reasoning (30 subjects, heterogeneous image types) | Accuracy | 576 | 2026-02 | [Paper](https://arxiv.org/abs/2311.16502) · [Code](https://github.com/MMMU-Benchmark/MMMU) · [Site](https://mmmu-benchmark.github.io/) |
| 14 | **MathVista** | 2023 | Mathematical reasoning in visual contexts (charts, geometry, figures) | Accuracy | 363 | 2025-09 | [Paper](https://arxiv.org/abs/2310.02255) · [Code](https://github.com/lupantech/MathVista) |
<!-- AEE-TABLE:VLM-CONTROL-REASONING:END -->

#### Perception & understanding

<!-- AEE-TABLE:VLM-CONTROL-PERCEPTION:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 15 | **MMBench** | 2023 | Fine-grained, multi-ability understanding with CircularEval; EN/ZH | Accuracy | 303 | 2025-05 | [Paper](https://arxiv.org/abs/2307.06281) · [Code](https://github.com/open-compass/MMBench) |
| 16 | **SEED-Bench series** | 2023-2024 | Broad multimodal capability coverage (image/video, generation-oriented comprehension, text-rich understanding) | Accuracy | 364 | 2025-01 | [Paper](https://arxiv.org/abs/2307.16125) · [Code](https://github.com/AILab-CVC/SEED-Bench) |
<!-- AEE-TABLE:VLM-CONTROL-PERCEPTION:END -->

#### Video understanding

<!-- AEE-TABLE:VLM-CONTROL-VIDEO:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 17 | **Video-MME / Video-MME-v2** | 2024/2026 | Comprehensive video understanding, with v2 targeting robustness, consistency, and reasoning faithfulness | Accuracy / Group-based score (v2) | 779 | 2025-12 | [Paper v1](https://arxiv.org/abs/2405.21075) · [Code v1](https://github.com/MME-Benchmarks/Video-MME) · [Paper v2](https://arxiv.org/abs/2604.05015) · [Code v2](https://github.com/MME-Benchmarks/Video-MME-v2) |
<!-- AEE-TABLE:VLM-CONTROL-VIDEO:END -->

#### Document understanding

<!-- AEE-TABLE:VLM-CONTROL-DOCUMENT:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 18 | **DocVQA (RRC track)** | 2020-ongoing | Document visual question answering and document reasoning under challenge protocol | ANLS / Accuracy | — | — | [Paper](https://arxiv.org/abs/2007.00398) · [RRC](https://rrc.cvc.uab.es/) |
<!-- AEE-TABLE:VLM-CONTROL-DOCUMENT:END -->

Common toolkit: [VLMEvalKit](https://github.com/open-compass/VLMEvalKit) provides standardized evaluation for the benchmarks above and 80+ others.

## Action Evaluation

Action benchmarks are grouped first by **where the policy is evaluated**: closed-loop simulation, real-to-sim proxy, or real hardware. Simulation benchmarks are further split by the failure mode or capability they are designed to expose.

### Simulation · Core suites

<!-- AEE-TABLE:VLA-SIM-CORE:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 1 | **RLBench** | 2020 | 100+ language-conditioned manipulation tasks in CoppeliaSim (Franka Panda); widely used action-model baseline | Success rate | 1.8k | 2025-01 | [Paper](https://arxiv.org/abs/1909.12271) · [Code](https://github.com/stepjam/RLBench) |
| 2 | **CALVIN** | 2021 | Long-horizon instruction chaining; compositional generalization (ABC→D) | Avg. completed chain length | 942 | 2025-09 | [Paper](https://arxiv.org/abs/2112.03227) · [Code](https://github.com/mees/calvin) |
| 3 | **LIBERO** | 2023 | Lifelong / language-conditioned tabletop manipulation (Spatial, Object, Goal, Long suites) | Success rate | 2.0k | 2025-03 | [Paper](https://arxiv.org/abs/2306.03310) · [Code](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| 4 | **ManiSkill2** | 2023 | Generalizable manipulation across diverse objects / skills with high-throughput simulation | Task success / reward-based scores | 1 | 2023-08 | [Paper](https://arxiv.org/abs/2302.04659) · [Code](https://github.com/haosulab/ManiSkill2-task-dev) |
| 5 | **BEHAVIOR-1K** | 2024 | Long-horizon, human-centered household activities with realistic simulation dynamics | Activity success / completion metrics | 1.5k | 2026-06 | [Paper](https://arxiv.org/abs/2403.09227) · [Code](https://github.com/StanfordVL/BEHAVIOR-1K) |
<!-- AEE-TABLE:VLA-SIM-CORE:END -->

### Simulation · Robustness and perturbation diagnostics

<!-- AEE-TABLE:VLA-SIM-ROBUSTNESS:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 6 | **THE COLOSSEUM** | 2024 | Generalization in robotic manipulation under visual/semantic/execution perturbations | Success rate | 149 | 2025-03 | [Paper](https://arxiv.org/abs/2402.08191) · [Code](https://github.com/robot-colosseum/robot-colosseum) · [Site](https://robot-colosseum.github.io) |
| 7 | **LIBERO-PRO** | 2025 | Robust LIBERO extension with perturbations on objects, initial states, instructions, and environments | Success rate under perturbations | 268 | 2026-03 | [Paper](https://arxiv.org/abs/2510.03827) · [Code](https://github.com/Zxy-MLlab/LIBERO-PRO) · [Site](https://zxy-mllab.github.io/LIBERO-PRO-Webpage/) |
| 8 | **LIBERO-Plus** | 2025 | LIBERO robustness benchmark with 10,030 tasks across seven perturbation factors (camera, robot state, language, lighting, texture, noise, layout) | Success rate by perturbation axis | 349 | 2026-01 | [Paper](https://arxiv.org/abs/2510.13626) · [Code](https://github.com/sylvestf/LIBERO-plus) · [Site](https://sylvestf.github.io/LIBERO-plus) · [LeRobot](https://huggingface.co/docs/lerobot/main/libero_plus) |
| 9 | **VLA-Arena** | 2025 | Structured action-model eval across task structure, language, and vision axes (170 tasks; Safety/Distractor/Extrapolation/Long-Horizon) | Success rate by difficulty level (L0–L2) | 178 | 2026-03 | [Paper](https://arxiv.org/abs/2512.22539) · [Code](https://github.com/PKU-Alignment/VLA-Arena) · [Site](https://vla-arena.github.io/) |
<!-- AEE-TABLE:VLA-SIM-ROBUSTNESS:END -->

### Simulation · Memory and history dependence

<!-- AEE-TABLE:VLA-SIM-MEMORY:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 10 | **LIBERO-Mem** | 2025 | Object-level memory in partially observable manipulation: motion, sequence, relations, and occlusion | Success rate under temporal scaling | 22 | 2025-11 | [Paper](https://arxiv.org/abs/2511.11478) · [Code](https://github.com/libero-mem/libero-mem) · [Site](https://libero-mem.github.io/) |
| 11 | **RoboMME** | 2026 | Memory-augmented manipulation across temporal, spatial, object, and procedural memory suites | Success rate across 16 tasks | 113 | 2026-06 | [Paper](https://arxiv.org/abs/2603.04639) · [Code](https://github.com/RoboMME/robomme_benchmark) · [Site](https://robomme.github.io/) · [Leaderboard](https://robomme.github.io/leaderboard.html) |
| 12 | **MIKASA-Robo-VLA** | 2026 | Memory-intensive tabletop manipulation for action models: 90 language-conditioned tasks across 10 memory types | Success rate by horizon and memory type | 112 | 2026-06 | [Paper](https://arxiv.org/abs/2502.10550) · [Code](https://github.com/CognitiveAISystems/MIKASA-Robo) · [Docs](https://mikasarobo.github.io/) |
<!-- AEE-TABLE:VLA-SIM-MEMORY:END -->

### Simulation · Long-horizon reasoning

<!-- AEE-TABLE:VLA-SIM-LONG-HORIZON:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 13 | **RoboCasa / RoboCasa365** | 2024/2026 | Large-scale everyday kitchen manipulation, from atomic skills to long-horizon composites | Success rate across benchmark suites | 1.5k | 2026-05 | [Paper](https://arxiv.org/abs/2406.02523) · [Code](https://github.com/robocasa/robocasa) |
| 14 | **VLABench** | 2024/2025 | Language-conditioned manipulation with long-horizon reasoning, implicit intentions, world knowledge, and 100 task categories | Success rate and capability breakdown | 442 | 2025-11 | [Paper](https://arxiv.org/abs/2412.18194) · [Code](https://github.com/OpenMOSS/VLABench) · [Site](https://vlabench.github.io/) |
| 15 | **RoboCerebra** | 2025 | Long-horizon robotic manipulation with System-2 planning, reflection, memory, and VLM-planner + action-controller interaction | Task success and reasoning/planning breakdown | 65 | 2026-04 | [Paper](https://arxiv.org/abs/2506.06677) · [Code](https://github.com/qiuboxiang/RoboCerebra) · [Site](https://robocerebra.github.io/) |
| 16 | **EmbodiedBench** | 2025 | MLLM-as-agent eval across 1,128 tasks in 4 sim environments (high/low-level; 6 capability subsets) | Task success rate | 311 | 2026-05 | [Paper](https://arxiv.org/abs/2502.09560) · [Code](https://github.com/EmbodiedBench/EmbodiedBench) · [Site](https://embodiedbench.github.io/) |
<!-- AEE-TABLE:VLA-SIM-LONG-HORIZON:END -->

### Simulation · Task-generalist and broad-control benchmarks

<!-- AEE-TABLE:VLA-SIM-GENERALIST:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 17 | **RoboTwin 2.0** | 2025 | Dual-arm manipulation benchmark with domain randomization; 50 tasks, 5 robot embodiments, sim-to-real protocol | Task success rate | 2.5k | 2026-05 | [Paper](https://arxiv.org/abs/2506.18088) · [Code](https://github.com/RoboTwin-Platform/RoboTwin) · [Site](https://robotwin-platform.github.io/) · [Leaderboard](https://robotwin-platform.github.io/leaderboard) |
| 18 | **Kinetix** | 2025 | Open-ended 2D physics-control tasks used by vla-eval as a broad control/generalization stress test | Task return / success | 258 | 2026-05 | [Paper](https://arxiv.org/abs/2410.23208) · [Site](https://kinetix-env.github.io/) |
| 19 | **RoboLab** | 2026 | High-fidelity Isaac Lab benchmark for DROID-trained task-generalist policies; 120 tasks across visual, procedural, and relational axes | SR%, progress score, EE speed, EE SPARC | 307 | 2026-06 | [Paper](https://arxiv.org/abs/2604.09860) · [Code](https://github.com/NVlabs/RoboLab) · [Site](https://research.nvidia.com/labs/srl/projects/robolab/) · [Leaderboard](https://research.nvidia.com/labs/srl/projects/robolab/leaderboard.html) |
| 20 | **MolmoSpaces-Bench** | 2026 | Zero-shot navigation and manipulation benchmark over procedurally generated spaces with pick, place, open, close, and door tasks | Task success rate | 365 | 2026-06 | [Paper](https://arxiv.org/abs/2602.11337) · [Code](https://github.com/allenai/molmospaces) · [Site](https://allenai.github.io/molmospaces/) |
<!-- AEE-TABLE:VLA-SIM-GENERALIST:END -->

### Sim-to-real proxy (real-to-sim)

<!-- AEE-TABLE:VLA-SIM2REAL:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 21 | **SimplerEnv** | 2024 | Real-to-sim evaluation of real-robot policies (Google Robot, WidowX+Bridge) | Success rate, sim↔real correlation (MMRV, Pearson r) | 1.1k | 2025-12 | [Paper](https://arxiv.org/abs/2405.05946) · [Code](https://github.com/simpler-env/SimplerEnv) |
| 22 | **REALM** | 2025 | Real-to-sim validated generalization benchmark (DROID embodiment; 15 perturbations, 7 skills) | Success rate; sim↔real correlation | 60 | 2026-06 | [Paper](https://arxiv.org/abs/2512.19562) · [Code](https://github.com/martin-sedlacek/REALM) · [Site](https://martin-sedlacek.com/realm/) |
<!-- AEE-TABLE:VLA-SIM2REAL:END -->

### Real robot

<!-- AEE-TABLE:VLA-REAL:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 23 | **DROID** | 2024 | In-the-wild Franka manipulation eval on real hardware; multi-scene generalization protocol | Success rate (ID / OOD) | 289 | 2025-04 | [Paper](https://arxiv.org/abs/2403.12945) · [Code](https://github.com/droid-dataset/droid_policy_learning) · [Site](https://droid-dataset.github.io/) |
| 24 | **RoboArena** | 2025 | Distributed real-world evaluation of generalist robot policies via double-blind pairwise comparisons on DROID robots | Pairwise preference / Elo-style ranking | 104 | 2026-04 | [Paper](https://arxiv.org/abs/2506.18123) · [Code](https://github.com/robo-arena/roboarena) · [Site](https://robo-arena.github.io/) |
| 25 | **RoboChallenge / Table30** | 2025/2026 | Large-scale remote real-robot evaluation across Table30 / Table30 V2 tasks and multiple robot embodiments | Success rate, progress score, and leaderboard ranking | 146 | 2026-06 | [Paper](https://arxiv.org/abs/2510.17950) · [Code](https://github.com/RoboChallenge/RoboChallengeInference) · [Site / Leaderboard](https://robochallenge.ai/) · [Table30](https://huggingface.co/datasets/RoboChallenge/Table30) · [Table30 V2](https://huggingface.co/datasets/RoboChallenge/Table30v2) |
| 26 | **VLA-REPLICA** | 2026 | Low-cost reproducible real-world action-model benchmark using an SO-101 arm, RGB-D cameras, and standardized ID/OOD manipulation tasks | Real-world success rate (ID / OOD) | — | — | [Paper](https://arxiv.org/abs/2605.20774) · [Site](https://irvlutd.github.io/VLAReplica/) |
| 27 | **ManipArena** | 2026 | Real-world bimanual and mobile manipulation with reasoning-oriented tasks, OOD generalization, and sensory diagnostics | Task success rate and process diagnostics | 53 | 2026-05 | [Paper](https://arxiv.org/abs/2603.28545) · [Code](https://github.com/maniparena/maniparena-repo) · [Site](https://maniparena.x2robot.com/) · [Dataset](https://huggingface.co/datasets/ManipArena/maniparena-dataset) · [Simulation](https://github.com/maniparena/maniparena-sim) |
<!-- AEE-TABLE:VLA-REAL:END -->

Common harness: [vla-evaluation-harness](https://github.com/allenai/vla-evaluation-harness) runs many of these benchmarks in Docker with a shared protocol.

## World Modeling Evaluation

World-model benchmarks are grouped by **what aspect of a world model is measured**: perceptual quality, world generation, interactive control, embodied downstream utility, or physical / instruction adherence.

### Perceptual quality

<!-- AEE-TABLE:WM-PERCEPTUAL:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 1 | **VBench** | 2024 | 16-dimension video generation quality (subject, motion, temporal consistency, etc.) | VBench composite + per-dimension scores | 1.7k | 2026-03 | [Paper](https://arxiv.org/abs/2311.17909) · [Code](https://github.com/Vchitect/VBench) · [Site](https://vchitect.github.io/VBench-project/) |
<!-- AEE-TABLE:WM-PERCEPTUAL:END -->

### World generation (3D/4D/T2V/I2V)

<!-- AEE-TABLE:WM-GENERATION:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 2 | **WorldScore** | 2025 | Unified world generation across 3D/4D/T2V/I2V; controllability, quality, dynamics | WorldScore (composite) | 284 | 2025-12 | [Paper](https://arxiv.org/abs/2504.00983) · [Site](https://haoyi-duan.github.io/WorldScore/) |
| 3 | **4DWorldBench** | 2025/2026 | 3D/4D world generation realism: perceptual quality, condition alignment, physics, and consistency | Multi-dimension composite evaluation | — | — | [Paper](https://arxiv.org/abs/2511.19836) |
<!-- AEE-TABLE:WM-GENERATION:END -->

### Interactive / multi-turn

<!-- AEE-TABLE:WM-INTERACTIVE:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 4 | **WBench** | 2026 | Multi-turn interactive video world models (navigation, subject action, event editing, perspective switch) | 22 sub-metrics across 5 dimensions | 146 | 2026-06 | [Paper](https://arxiv.org/abs/2605.25874) · [Code](https://github.com/meituan-longcat/WBench) · [Site](https://meituan-longcat.github.io/WBench/) |
| 5 | **WorldMark** | 2026 | Interactive image-to-video world models under shared scenes, action sequences, and unified WASD-style controls | Visual quality, control alignment, and world consistency | 0 | 2026-04 | [Paper](https://arxiv.org/abs/2604.21686) · [Code](https://github.com/alaya-studio/WorldMark) · [Site](https://alaya-studio.github.io/WorldMark/) · [Arena](https://warena.ai/) |
<!-- AEE-TABLE:WM-INTERACTIVE:END -->

### Embodied downstream utility

<!-- AEE-TABLE:WM-EMBODIED:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 6 | **WorldArena** | 2026 | Perceptual quality + functional utility (data engine, policy eval, action planning) | EWMScore (composite) | 221 | 2026-05 | [Paper](https://arxiv.org/abs/2602.08971) · [Site](https://world-arena.ai/) |
| 7 | **RoboWM-Bench** | 2026 | Manipulation-centric world-model evaluation: generated human/robot videos are converted to executable robot actions and validated in simulation | Step-level executability and final task success | 0 | 2026-05 | [Paper](https://arxiv.org/abs/2604.19092) · [Code](https://github.com/flyingGH/RoboWM-Bench) · [Site](https://robowm-bench.github.io/RoboWM-Bench/) |
<!-- AEE-TABLE:WM-EMBODIED:END -->

### Physical consistency & instruction adherence

<!-- AEE-TABLE:WM-PHYSICAL:START -->
| No. | Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|---|
| 8 | **WorldModelBench** | 2025 | World modeling capability under instruction following, commonsense, and physical adherence | Composite world-modeling scores | 41 | 2025-07 | [Paper](https://arxiv.org/abs/2502.20694) · [Code](https://github.com/WorldModelBench-Team/WorldModelBench) |
| 9 | **EWMBench** | 2025 | Embodied world models: scene consistency, motion correctness, semantic alignment | Per-dimension scores | 126 | 2025-06 | [Code](https://github.com/AgibotTech/EWMBench) |
| 10 | **MiraBench** | 2026 | Action-conditioned reliability in robotic world models: physics adherence, action-following fidelity, and optimism-bias detection | Physics adherence, action-following fidelity, optimism-bias score | — | — | [Paper](https://arxiv.org/abs/2605.29360) · [Dataset](https://huggingface.co/datasets/Anonymous-nips-submissions/Anonymous-nips-submissions) |
<!-- AEE-TABLE:WM-PHYSICAL:END -->

## Related Lists

- [awesome-vla-wam](https://github.com/DravenALG/awesome-vla-wam) — VLA and World Action Models.
- [Awesome-World-Action-Model](https://github.com/HyperbolicCurve/Awesome-World-Action-Model) — papers, datasets, and benchmarks for action models, including WAM/VLA.
- [awesome-embodied-vla-va-vln](https://github.com/jonyzhang2023/awesome-embodied-vla-va-vln) — VLA / VA / VLN models and simulators.

## Contributing

Pull requests are welcome. For a new entry, please include:

- Links to the paper and the official code.
- Ecosystem status: whether data/tasks, evaluation protocol, and leaderboard are public or missing.
- Task setup, input/output format, and the main metric.
- A minimal run command, if you have one.
- Any reproducibility caveats you ran into (coordinate conventions, normalization stats, ambiguous termination rules, etc.).

Keep one entry per row and place it in the matching capability table. Assign a **per-capability, contiguous `seq`** in `data/benchmarks.yaml` (shown as the first table column; Reasoning & Planning / Action / World Modeling each starts at 1). After manual bulk edits, run `python scripts/render_readme.py --assign-seq` before re-rendering.

## License

[MIT](LICENSE)
