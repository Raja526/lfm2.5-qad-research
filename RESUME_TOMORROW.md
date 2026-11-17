# Resume point

Project: LFM2.5 Quantization-Aware Distillation research

Current status:

- `llama.cpp` has been built at `llama.cpp/build/bin/llama-cli` and `llama-bench`.
- 230M PTQ Q4_0, QAD Q4_0, and Q5_K_M checkpoints are cached locally.
- Smoke-test outputs are in `results/`.
- The benchmark harness is `benchmark.py` and prompts are in `prompts.jsonl`.

Next session:

1. Download and benchmark `LFM2.5-230M-BF16.gguf`.
2. Add a scoring script for exact-match, JSON validity, and instruction compliance.
3. Repeat throughput measurements under controlled settings.
4. Produce the first BF16/PTQ/QAD/Q5 comparison table.

Useful commands from this folder:

```bash
python3 benchmark.py --cli llama.cpp/build/bin/llama-cli \
  --model LiquidAI/LFM2.5-230M-GGUF \
  --variant LFM2.5-230M-BF16.gguf \
  --output results/230m_bf16.jsonl
```

The main research hypothesis is that QAD Q4_0 preserves more task accuracy
than standard PTQ Q4_0 at essentially the same model size.

Completed 2026-11-17:

- BF16 benchmark saved to `results/230m_bf16.jsonl` (five successful records).
- Deterministic scorer added as `score_results.py`.
- Comparison artifacts written to `results/score_comparison.md` and
  `results/score_comparison.json`.
- Warm CPU throughput benchmark written to `results/throughput_comparison.json`
  and summarized in `results/throughput_comparison.md`.
- Expanded 10-prompt suite added as `prompts_extended.jsonl`; four model runs
  are in `results/extended_*.jsonl` with scores in
  `results/extended_score_comparison.md` and `.json`.
- Repeated-seed runs for seeds 1234, 2024, and 4242 are aggregated in
  `results/seed_aggregate.md` and `results/seed_aggregate.json`.
- Consolidated interpretation and limitations are documented in
  `RESULTS_REPORT.md`.
- Statistical analysis is in `statistical_analysis.py` with outputs under
  `results/statistical_analysis.*`; platform drafts are in
  `PUBLICATION_DRAFTS.md`.

Next step: add repeated-seed scoring and refine partial-credit rules for JSON
and arithmetic responses.

