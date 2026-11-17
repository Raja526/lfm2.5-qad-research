# Publication drafts: LFM2.5 QAD quantization study

These drafts are ready for editing and posting. They describe the local
experiment as exploratory, not as a benchmark claim about all workloads.

## Medium

### Does Quantization-Aware Distillation Preserve Small-Model Behavior?

I compared four LFM2.5-230M GGUF checkpoints on a small, reproducible CPU
evaluation: BF16, standard PTQ Q4_0, QAD Q4_0, and Q5_K_M.

The test suite contained 10 prompts covering instruction following, structured
extraction, tool calls, factual QA, and arithmetic. Each model was evaluated
with three seeds, producing 30 paired prompt-seed cases per checkpoint.

The headline result is that QAD Q4_0 matched BF16 exactly on this suite: 18/30
exact matches (60%) for both. Standard PTQ Q4_0 scored 11/30 (37%), while
Q5_K_M scored 24/30 (80%). The QAD and BF16 JSON-validity and instruction-
compliance rates also matched in this test.

The warm throughput run showed why quantization matters operationally. BF16
generated 50.0 tokens/s, compared with 142.6 tokens/s for QAD Q4_0, while the
QAD file was 146.7 MB versus 459.5 MB for BF16. QAD and standard PTQ had nearly
identical throughput, so the difference was behavioral rather than a speed
advantage over PTQ.

The paired analysis is encouraging but deliberately modest: QAD’s exact-match
advantage over PTQ was +23 percentage points (exploratory McNemar p=0.039), and
its JSON-validity advantage was +33 points (p=0.002). The dataset is only 10
prompts, so these numbers should be treated as a signal for larger testing,
not a final generalization claim.

The complete artifacts, prompts, scorer, and raw JSONL outputs are available in
the accompanying GitHub repository.

## Substack

### A Small Quantization Experiment With a Useful Signal

I ran a controlled comparison of LFM2.5-230M checkpoints to ask a practical
question: does QAD Q4_0 retain more task behavior than ordinary PTQ Q4_0 at the
same approximate file size?

Across 30 paired cases, QAD matched BF16 at 60% exact match and beat PTQ Q4_0
at 60% versus 37%. Q5_K_M led at 80%. QAD also reduced the model file from
459.5 MB (BF16) to 146.7 MB and generated at 142.6 tokens/s versus 50.0 for
BF16 in a warm CPU benchmark.

The caveat is the important part: this was a 10-prompt research scaffold, not
a broad language-model evaluation. The result is best read as evidence that
QAD deserves larger testing, not as proof that it wins every workload.

## GitHub README section

### Findings

Using 10 prompts × 3 seeds (30 paired cases per model):

| Variant | Exact | JSON valid | Instruction compliance |
|---|---:|---:|---:|
| BF16 | 18/30 | 12/30 | 24/30 |
| PTQ Q4_0 | 11/30 | 2/30 | 11/30 |
| QAD Q4_0 | 18/30 | 12/30 | 24/30 |
| Q5_K_M | 24/30 | 12/30 | 27/30 |

Warm generation throughput was 50.0 tok/s (BF16), 143.1 tok/s (PTQ Q4_0),
142.6 tok/s (QAD Q4_0), and 113.2 tok/s (Q5_K_M). These are CPU-only results
with llama.cpp, six threads, and three repetitions.

This is an exploratory small-sample study. See `RESULTS_REPORT.md`,
`results/statistical_analysis.md`, and `results/seed_aggregate.md` for details.

## LinkedIn

I finished a small reproducible study of LFM2.5-230M quantization.

Key result: QAD Q4_0 matched BF16 on my 30 paired prompt-seed cases (60% exact
match) and outperformed standard PTQ Q4_0 (37%). Q5_K_M was strongest overall
at 80%. QAD reduced the model file to 146.7 MB and generated at 142.6 tok/s on
CPU, versus 50.0 tok/s for BF16.

Important caveat: this is a 10-prompt exploratory suite, so I’m treating the
result as a research signal rather than a universal benchmark claim. Raw
prompts, JSONL outputs, scoring code, and the statistical analysis are included
for reproduction.

#quantization #llama.cpp #machinelearning #opensource #modelcompression
