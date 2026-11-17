# LFM2.5 QAD research scaffold

This project compares LFM2.5 checkpoints under a fixed runtime and evaluation set:

- BF16/F16 reference
- standard PTQ `Q4_0`
- Liquid AI QAD `Q4_0`
- `Q5_K_M` reference

The experiment is intentionally small and reproducible. It records generation
latency and output text, then scores exact match, JSON validity, instruction
compliance, and repeated-seed stability.

## Results

Across 10 prompts and three seeds (30 paired cases per model), QAD Q4_0 matched
BF16 at 18/30 exact matches while standard PTQ Q4_0 scored 11/30. Q5_K_M scored
24/30. Warm CPU generation was 142.6 tok/s for QAD versus 50.0 tok/s for BF16.

See [RESULTS_REPORT.md](RESULTS_REPORT.md),
[results/statistical_analysis.md](results/statistical_analysis.md), and
[PUBLICATION_DRAFTS.md](PUBLICATION_DRAFTS.md).

## Prerequisites

- `llama-cli` from `llama.cpp`
- Python 3.10+
- access to the LiquidAI LFM2.5 GGUF repositories

## Smoke test

```bash
python3 benchmark.py \
  --model "LiquidAI/LFM2.5-230M-GGUF" \
  --variant "LFM2.5-230M-QAD-Q4_0.gguf" \
  --output results/230m_qad.jsonl
```

Run the same prompts for every variant and keep runtime flags identical. The
generated JSONL is designed to be joined by prompt ID for later accuracy scoring.

