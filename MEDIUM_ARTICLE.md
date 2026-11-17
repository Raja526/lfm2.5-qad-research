# Does Quantization-Aware Distillation Preserve Small-Model Intelligence?

## A reproducible LFM2.5-230M comparison of BF16, PTQ, QAD, and Q5 quantization

Small language models are becoming more useful, but deployment still comes down
to a practical tradeoff: memory, speed, and behavior.

This project tested whether quantization-aware distillation (QAD) can preserve
more useful behavior than ordinary post-training quantization (PTQ), without
giving up the efficiency benefits of 4-bit weights.

## The experiment

I compared four LFM2.5-230M GGUF checkpoints:

- BF16 reference
- Standard PTQ Q4_0
- Liquid AI QAD Q4_0
- Q5_K_M

The evaluation used 10 prompts covering instruction following, structured
extraction, tool calls, factual questions, and arithmetic. Each model ran with
three seeds, giving 30 paired prompt-seed cases per checkpoint.

The scoring was intentionally explicit:

- exact-match accuracy
- JSON validity
- instruction compliance

Warm throughput was measured separately with `llama-bench` using 512 prompt
tokens, 128 generated tokens, six CPU threads, and three repetitions.

## Results

| Variant | Exact match | JSON valid | Instruction compliance |
|---|---:|---:|---:|
| BF16 | 18/30 (60%) | 12/30 (40%) | 24/30 (80%) |
| PTQ Q4_0 | 11/30 (37%) | 2/30 (7%) | 11/30 (37%) |
| QAD Q4_0 | 18/30 (60%) | 12/30 (40%) | 24/30 (80%) |
| Q5_K_M | 24/30 (80%) | 12/30 (40%) | 27/30 (90%) |

The most important result is the QAD/PTQ comparison. At the same approximate
file size, QAD matched BF16 on this suite and outperformed standard PTQ Q4_0.

Q5_K_M achieved the highest exact-match score, but it is a larger, higher-bit
checkpoint. That makes QAD interesting as a compact deployment option rather
than as the absolute accuracy winner.

## Efficiency results

| Variant | File size | Prompt tok/s | Generation tok/s |
|---|---:|---:|---:|
| BF16 | 459.5 MB | 543.8 | 50.0 |
| PTQ Q4_0 | 146.7 MB | 827.0 | 143.1 |
| QAD Q4_0 | 146.7 MB | 826.2 | 142.6 |
| Q5_K_M | 169.2 MB | 927.8 | 113.2 |

QAD reduced the model file by about 68% compared with BF16. Its warm generation
rate was approximately 2.85 times higher than BF16, while its throughput was
effectively the same as standard PTQ Q4_0.

In other words, the advantage observed here is primarily behavioral: QAD appears
to retain more of the reference model’s useful behavior at the same 4-bit size.

## Statistical perspective

Because the cases were paired by prompt and seed, I also computed exploratory
paired comparisons. Relative to PTQ Q4_0, QAD showed:

- +23 percentage points on exact match
- +33 points on JSON validity
- +43 points on instruction compliance

The exact paired tests are suggestive, but this is not a large benchmark. Ten
prompts are enough to expose failure modes; they are not enough to establish
general-purpose superiority.

## What this does—and does not—show

This experiment supports a narrow conclusion:

> On this small, reproducible LFM2.5-230M suite, QAD Q4_0 preserved BF16-level
> task scores better than standard PTQ Q4_0 at roughly one-third of the file size.

It does not show that QAD wins every workload, every prompt distribution, or
every hardware configuration. The arithmetic and JSON tasks also reveal that
all four variants need more structured-output testing.

The next research step is a larger task set with independently designed prompts,
more seeds, peak-memory measurements, and a clearer separation between semantic
accuracy and formatting compliance.

## Reproduce it

All prompts, raw outputs, scoring code, statistical analysis, and throughput
results are available here:

<https://github.com/Raja526/lfm2.5-qad-research>

The repository intentionally excludes model weights and the local llama.cpp
checkout. See `RESULTS_REPORT.md` for the full methodology and limitations.

---

*Tags: quantization, LLM inference, model compression, llama.cpp, edge AI,
machine learning, open source*
