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

The **Stars** and **Updated** columns are refreshed automatically **twice a week** (Monday and Thursday) by a GitHub Actions workflow, so the popularity and activity signals stay current. Every other field is curated by hand.

The same workflow can also propose newly discovered benchmark entries across VLM / VLA / WM via an automated PR. Auto-insertions are guarded by strict checks (paper link + official code + embodied relevance threshold), and all changes remain reviewable before merge.

## VLM Evaluation

We split VLM evaluation into two layers:

- **Embodied VLM Benchmarks (Primary)**: directly evaluate embodied capabilities (spatial grounding, planning, physical understanding, environment-level QA).
- **General VLM Benchmarks (Control Set)**: track broad multimodal competence so gains on embodied tasks are not traded for general capability regressions.

### Embodied VLM Benchmarks (Primary)

<!-- AEE-TABLE:VLM-PRIMARY:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **Where2Place** | 2024 | Spatial free-space reference: language-conditioned placement in cluttered real scenes | Point accuracy | 224 | 2025-07 | [Paper](https://arxiv.org/abs/2406.10721) · [Code](https://github.com/wentaoyuan/RoboPoint) · [Dataset](https://huggingface.co/datasets/wentao-yuan/where2place) |
| **RefSpatial-Bench** | 2025 | Multi-step spatial referring and placement reasoning in complex 3D scenes | Accuracy (Location / Placement) | 263 | 2025-12 | [Paper](https://arxiv.org/abs/2506.04308) · [Code](https://github.com/Zhoues/RoboRefer) · [Site](https://zhoues.github.io/RoboRefer/) |
| **VSI-Bench** | 2025 | Egocentric video-based visual-spatial intelligence (configurational, measurement, spatiotemporal) | Accuracy / MRA | 726 | 2025-08 | [Paper](https://arxiv.org/abs/2412.14171) · [Code](https://github.com/vision-x-nyu/thinking-in-space) · [Dataset](https://huggingface.co/datasets/nyu-visionx/VSI-Bench) |
| **EgoPlan-Bench2** | 2024 | Egocentric real-world planning across daily scenarios and long-horizon task progress | Accuracy | 31 | 2025-04 | [Paper](https://arxiv.org/abs/2412.04447) · [Code](https://github.com/qiulu66/EgoPlan-Bench2/) · [Site](https://qiulu66.github.io/egoplanbench2/) |
| **OpenEQA** | 2024 | Embodied question answering with episodic-memory and active-exploration settings | LLM-judge score / answer quality | 365 | 2024-09 | [Paper](https://openaccess.thecvf.com/content/CVPR2024/html/Majumdar_OpenEQA_Embodied_Question_Answering_in_the_Era_of_Foundation_Models_CVPR_2024_paper.html) · [Code](https://github.com/facebookresearch/open-eqa) · [Site](https://open-eqa.github.io/) |
| **PhysBench** | 2025 | Physical-world understanding for embodied agents (object physics, relations, scene dynamics) | Accuracy across physical dimensions | 91 | 2026-01 | [Paper](https://arxiv.org/abs/2501.16411) · [Code](https://github.com/physical-superintelligence-lab/PhysBench) · [Site](https://physbench.github.io/) |
<!-- AEE-TABLE:VLM-PRIMARY:END -->

### General VLM Benchmarks (Control Set)

<!-- AEE-TABLE:VLM-CONTROL:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **MMMU** | 2023 | College-level, multi-discipline multimodal reasoning (30 subjects, heterogeneous image types) | Accuracy | 576 | 2026-02 | [Paper](https://arxiv.org/abs/2311.16502) · [Code](https://github.com/MMMU-Benchmark/MMMU) · [Site](https://mmmu-benchmark.github.io/) |
| **MMBench** | 2023 | Fine-grained, multi-ability understanding with CircularEval; EN/ZH | Accuracy | 303 | 2025-05 | [Paper](https://arxiv.org/abs/2307.06281) · [Code](https://github.com/open-compass/MMBench) |
| **MathVista** | 2023 | Mathematical reasoning in visual contexts (charts, geometry, figures) | Accuracy | 363 | 2025-09 | [Paper](https://arxiv.org/abs/2310.02255) · [Code](https://github.com/lupantech/MathVista) |
| **Video-MME / Video-MME-v2** | 2024/2026 | Comprehensive video understanding, with v2 targeting robustness, consistency, and reasoning faithfulness | Accuracy / Group-based score (v2) | 779 | 2025-12 | [Paper v1](https://arxiv.org/abs/2405.21075) · [Code v1](https://github.com/MME-Benchmarks/Video-MME) · [Paper v2](https://arxiv.org/abs/2604.05015) · [Code v2](https://github.com/MME-Benchmarks/Video-MME-v2) |
| **SEED-Bench series** | 2023-2024 | Broad multimodal capability coverage (image/video, generation-oriented comprehension, text-rich understanding) | Accuracy | 364 | 2025-01 | [Paper](https://arxiv.org/abs/2307.16125) · [Code](https://github.com/AILab-CVC/SEED-Bench) |
| **DocVQA (RRC track)** | 2020-ongoing | Document visual question answering and document reasoning under challenge protocol | ANLS / Accuracy | — | — | [Paper](https://arxiv.org/abs/2007.00398) · [RRC](https://rrc.cvc.uab.es/) |
<!-- AEE-TABLE:VLM-CONTROL:END -->

Common toolkit: [VLMEvalKit](https://github.com/open-compass/VLMEvalKit) provides standardized evaluation for the benchmarks above and 80+ others.

## VLA Evaluation

<!-- AEE-TABLE:VLA:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **LIBERO** | 2023 | Lifelong / language-conditioned tabletop manipulation (Spatial, Object, Goal, Long suites) | Success rate | 2.0k | 2025-03 | [Paper](https://arxiv.org/abs/2306.03310) · [Code](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| **CALVIN** | 2021 | Long-horizon instruction chaining; compositional generalization (ABC→D) | Avg. completed chain length | 942 | 2025-09 | [Paper](https://arxiv.org/abs/2112.03227) · [Code](https://github.com/mees/calvin) |
| **SimplerEnv** | 2024 | Real-to-sim evaluation of real-robot policies (Google Robot, WidowX+Bridge) | Success rate, sim↔real correlation (MMRV, Pearson r) | 1.1k | 2025-12 | [Paper](https://arxiv.org/abs/2405.05946) · [Code](https://github.com/simpler-env/SimplerEnv) |
| **ManiSkill2** | 2023 | Generalizable manipulation across diverse objects / skills with high-throughput simulation | Task success / reward-based scores | 1 | 2023-08 | [Paper](https://arxiv.org/abs/2302.04659) · [Code](https://github.com/haosulab/ManiSkill2-task-dev) |
| **BEHAVIOR-1K** | 2024 | Long-horizon, human-centered household activities with realistic simulation dynamics | Activity success / completion metrics | 1.5k | 2026-06 | [Paper](https://arxiv.org/abs/2403.09227) · [Code](https://github.com/StanfordVL/BEHAVIOR-1K) |
| **RoboCasa / RoboCasa365** | 2024/2026 | Large-scale everyday kitchen manipulation, from atomic skills to long-horizon composites | Success rate across benchmark suites | 1.5k | 2026-05 | [Paper](https://arxiv.org/abs/2406.02523) · [Code](https://github.com/robocasa/robocasa) |
| **Clone repository** | 2025 | VLA-Arena is an open-source benchmark for systematic evaluation of Vision-Language-Action (VLA) models. | Task-specific benchmark metrics (see official protocol) | 178 | 2026-03 | [Paper](https://arxiv.org/abs/2512.22539) · [Code](https://github.com/PKU-Alignment/VLA-Arena) |
| **robot colosseum** | 2024 | A Benchmark for Evaluating Generalization for Robotic Manipulation | Task-specific benchmark metrics (see official protocol) | 150 | 2025-03 | [Paper](https://arxiv.org/abs/2402.08191) · [Code](https://github.com/robot-colosseum/robot-colosseum) · [Site](https://robot-colosseum.github.io) |
<!-- AEE-TABLE:VLA:END -->

Common harness: [vla-evaluation-harness](https://github.com/allenai/vla-evaluation-harness) runs many of these benchmarks in Docker with a shared protocol.

## World Model Evaluation

<!-- AEE-TABLE:WM:START -->
| Benchmark | Year | What it tests | Metric | Stars | Updated | Links |
|---|---|---|---|---|---|---|
| **WorldArena** | 2026 | Perceptual quality + functional utility (data engine, policy eval, action planning) | EWMScore (composite) | 220 | 2026-05 | [Paper](https://arxiv.org/abs/2602.08971) · [Site](https://world-arena.ai/) |
| **WorldScore** | 2025 | Unified world generation across 3D/4D/T2V/I2V; controllability, quality, dynamics | WorldScore (composite) | 284 | 2025-12 | [Paper](https://arxiv.org/abs/2504.00983) · [Site](https://haoyi-duan.github.io/WorldScore/) |
| **EWMBench** | 2025 | Embodied world models: scene consistency, motion correctness, semantic alignment | Per-dimension scores | 126 | 2025-06 | [Code](https://github.com/AgibotTech/EWMBench) |
| **WorldModelBench** | 2025 | World modeling capability under instruction following, commonsense, and physical adherence | Composite world-modeling scores | 41 | 2025-07 | [Paper](https://arxiv.org/abs/2502.20694) · [Code](https://github.com/WorldModelBench-Team/WorldModelBench) |
| **4DWorldBench** | 2025/2026 | 3D/4D world generation realism: perceptual quality, condition alignment, physics, and consistency | Multi-dimension composite evaluation | — | — | [Paper](https://arxiv.org/abs/2511.19836) |
| **0. Clone the repo** | 2026 | [ICML 2026🔥]Rethinking Video Generation Model for the Embodied World | Task-specific benchmark metrics (see official protocol) | 73 | 2026-06 | [Paper](https://arxiv.org/abs/2601.15282) · [Code](https://github.com/DAGroup-PKU/ReVidgen) |
| **Awesome World Models for VLA Agents** | 2023 | Official repository for "Towards Generalist Embodied AI: A Survey on World Models for VLA Agents". This curated list systematically organizes core resources including research papers, foundation models, evaluation metrics, and benchmarks. | Task-specific benchmark metrics (see official protocol) | 47 | 2026-03 | [Paper](https://arxiv.org/abs/2302.00111) · [Code](https://github.com/FutureTwT/awesome-world-models-for-vla-agents) |
<!-- AEE-TABLE:WM:END -->

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
