# Awesome Embodied Evaluation [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

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

Out of scope: pure navigation/language-only benchmarks (unless tied to embodied evaluation), and paper collections without a concrete evaluation protocol.

## How Entries Are Organized

Each entry lists the paper, the official code, the main metric, and notes on reproducibility. Where useful, entries also note the input/output format, the evaluator (rule-based, simulator, VLM-as-judge, or human), and the generalization setting (in-distribution, OOD, or sim-to-real).

## VLM Evaluation

| Benchmark | Year | What it tests | Metric | Links |
|---|---|---|---|---|
| **MMMU** | 2023 | College-level, multi-discipline multimodal reasoning (30 subjects, heterogeneous image types) | Accuracy | [Paper](https://arxiv.org/abs/2311.16502) · [Code](https://github.com/MMMU-Benchmark/MMMU) · [Site](https://mmmu-benchmark.github.io/) |
| **MMBench** | 2023 | Fine-grained, multi-ability understanding with CircularEval; EN/ZH | Accuracy | [Paper](https://arxiv.org/abs/2307.06281) · [Code](https://github.com/open-compass/MMBench) |
| **MathVista** | 2023 | Mathematical reasoning in visual contexts (charts, geometry, figures) | Accuracy | [Paper](https://arxiv.org/abs/2310.02255) · [Code](https://github.com/lupantech/MathVista) |

Common toolkit: [VLMEvalKit](https://github.com/open-compass/VLMEvalKit) provides standardized evaluation for the benchmarks above and 80+ others.

## VLA Evaluation

| Benchmark | Year | What it tests | Metric | Links |
|---|---|---|---|---|
| **LIBERO** | 2023 | Lifelong / language-conditioned tabletop manipulation (Spatial, Object, Goal, Long suites) | Success rate | [Paper](https://arxiv.org/abs/2306.03310) · [Code](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| **CALVIN** | 2021 | Long-horizon instruction chaining; compositional generalization (ABC→D) | Avg. completed chain length | [Paper](https://arxiv.org/abs/2112.03227) · [Code](https://github.com/mees/calvin) |
| **SimplerEnv** | 2024 | Real-to-sim evaluation of real-robot policies (Google Robot, WidowX+Bridge) | Success rate, sim↔real correlation (MMRV, Pearson r) | [Paper](https://arxiv.org/abs/2405.05946) · [Code](https://github.com/simpler-env/SimplerEnv) |

Common harness: [vla-evaluation-harness](https://github.com/allenai/vla-evaluation-harness) runs many of these benchmarks in Docker with a shared protocol.

## World Model Evaluation

| Benchmark | Year | What it tests | Metric | Links |
|---|---|---|---|---|
| **WorldArena** | 2026 | Perceptual quality + functional utility (data engine, policy eval, action planning) | EWMScore (composite) | [Paper](https://arxiv.org/abs/2602.08971) · [Site](https://world-arena.ai/) |
| **WorldScore** | 2025 | Unified world generation across 3D/4D/T2V/I2V; controllability, quality, dynamics | WorldScore (composite) | [Paper](https://arxiv.org/abs/2504.00983) · [Site](https://haoyi-duan.github.io/WorldScore/) |
| **EWMBench** | 2025 | Embodied world models: scene consistency, motion correctness, semantic alignment | Per-dimension scores | [Code](https://github.com/AgibotTech/EWMBench) |

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
