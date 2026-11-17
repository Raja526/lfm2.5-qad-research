# Repeated-seed extended-suite comparison

| Variant | Exact | JSON valid | Instruction-compliant | Mean elapsed (ms) |
|---|---:|---:|---:|---:|
| BF16 | 18/30 | 12/30 | 24/30 | 1444.08 |
| PTQ_Q4_0 | 11/30 | 2/30 | 11/30 | 1074.11 |
| QAD_Q4_0 | 18/30 | 12/30 | 24/30 | 804.77 |
| Q5_K_M | 24/30 | 12/30 | 27/30 | 910.63 |

Per-seed counts are preserved in the JSON artifact.
