# LFM2.5 QAD research scaffold

This project compares LFM2.5 checkpoints under a fixed runtime and evaluation set:

- BF16/F16 reference
- standard PTQ `Q4_0`
- Liquid AI QAD `Q4_0`
- `Q5_K_M` reference

The first experiment is intentionally small and reproducible. It records generation
latency and output text; task-specific scoring can be added after the smoke test.

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

