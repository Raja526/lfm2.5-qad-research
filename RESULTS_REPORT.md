# LFM2.5 QAD Quantization Research — Results Report

## Objective

Test whether Liquid AI’s QAD Q4_0 checkpoint preserves task behavior better
than standard PTQ Q4_0 at similar size, using BF16 as the reference and Q5_K_M
as a higher-bit comparison.

## Setup

- Model family: LFM2.5-230M
- Runtime: llama.cpp, CPU-only
- Evaluation: 10 prompts spanning instruction following, structured extraction,
  tool use, factual QA, and arithmetic
- Seeds: 1234, 2024, and 4242
- Throughput: 512 prompt tokens, 128 generated tokens, 6 threads, 3 repetitions
- Scoring: strict exact match, JSON validity, and instruction compliance

## Repeated-seed results

| Variant | Exact | JSON valid | Instruction-compliant | Mean elapsed (ms) |
|---|---:|---:|---:|---:|
| BF16 | 18/30 (60%) | 12/30 (40%) | 24/30 (80%) | 1444 |
| PTQ Q4_0 | 11/30 (37%) | 2/30 (7%) | 11/30 (37%) | 1074 |
| QAD Q4_0 | 18/30 (60%) | 12/30 (40%) | 24/30 (80%) | 805 |
| Q5_K_M | 24/30 (80%) | 12/30 (40%) | 27/30 (90%) | 911 |

QAD matched BF16 on every repeated-seed score while having similar compressed
size and lower end-to-end elapsed time in this harness. Q5_K_M was the strongest
model on exact-match accuracy.

## Warm throughput

| Variant | File size | Prompt tok/s | Generation tok/s |
|---|---:|---:|---:|
| BF16 | 459.5 MB | 543.8 | 50.0 |
| PTQ Q4_0 | 146.7 MB | 827.0 | 143.1 |
| QAD Q4_0 | 146.7 MB | 826.2 | 142.6 |
| Q5_K_M | 169.2 MB | 927.8 | 113.2 |

QAD and PTQ Q4_0 have effectively identical throughput. QAD generation is
approximately 2.85× faster than BF16 in the warm benchmark.

## Statistical analysis

The 30 paired cases per model produce exploratory Wilson 95% intervals. QAD
versus BF16 has zero observed difference on exact match, JSON validity, and
instruction compliance. QAD versus PTQ differs by +23 percentage points on
exact match, +33 points on JSON validity, and +43 points on instruction
compliance. Exact paired tests are suggestive, but the 10-prompt suite is too
small for broad generalization.

See `results/statistical_analysis.md` and `results/statistical_analysis.json`.

## Interpretation

The small experiment supports the hypothesis that QAD Q4_0 retains more useful
behavior than standard PTQ Q4_0 at the same file size. It does not beat Q5_K_M
on this task set, and the JSON scores show that all variants still need broader
structured-output testing.

## Limitations

- Only 10 prompts and three seeds were used.
- Exact-match rules are intentionally strict and may under-credit partially
  correct reasoning.
- The per-prompt benchmark includes process startup and model loading; use the
  warm `llama-bench` numbers for generation throughput comparisons.
- No memory/RAM peak measurement or larger benchmark suite has been run yet.

## Reproduction

See `prompts_extended.jsonl`, `benchmark.py`, `score_results.py`,
`aggregate_seeds.py`, and the JSONL artifacts under `results/`.
