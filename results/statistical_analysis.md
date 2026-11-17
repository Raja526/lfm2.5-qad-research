# Statistical analysis

Exploratory 95% intervals over 30 paired prompt-seed cases; bootstrap uses 10,000 paired resamples.

| Variant | Exact | 95% CI | JSON valid | 95% CI | Compliance | 95% CI | Mean latency (ms) |
|---|---:|:---:|---:|:---:|---:|:---:|---:|
| BF16 | 18/30 (60%) | [0.4232, 0.7541] | 12/30 (40%) | [0.2459, 0.5768] | 24/30 (80%) | [0.6269, 0.905] | 1444.08 ± 812.3 |
| PTQ_Q4_0 | 11/30 (37%) | [0.2187, 0.5449] | 2/30 (7%) | [0.0185, 0.2132] | 11/30 (37%) | [0.2187, 0.5449] | 1074.11 ± 391.36 |
| QAD_Q4_0 | 18/30 (60%) | [0.4232, 0.7541] | 12/30 (40%) | [0.2459, 0.5768] | 24/30 (80%) | [0.6269, 0.905] | 804.77 ± 282.29 |
| Q5_K_M | 24/30 (80%) | [0.6269, 0.905] | 12/30 (40%) | [0.2459, 0.5768] | 27/30 (90%) | [0.7438, 0.9654] | 910.63 ± 374.77 |

## Paired comparisons

### QAD_Q4_0_vs_BF16
- exact_match: mean difference +0.0000, bootstrap 95% CI [0, 0], McNemar exact p=1.0
- json_valid: mean difference +0.0000, bootstrap 95% CI [0, 0], McNemar exact p=1.0
- instruction_compliant: mean difference +0.0000, bootstrap 95% CI [0, 0], McNemar exact p=1.0

### QAD_Q4_0_vs_PTQ_Q4_0
- exact_match: mean difference +0.2333, bootstrap 95% CI [0.0667, 0.4], McNemar exact p=0.039062
- json_valid: mean difference +0.3333, bootstrap 95% CI [0.1667, 0.5], McNemar exact p=0.001953
- instruction_compliant: mean difference +0.4333, bootstrap 95% CI [0.2667, 0.6], McNemar exact p=0.000244

### Q5_K_M_vs_QAD_Q4_0
- exact_match: mean difference +0.2000, bootstrap 95% CI [0.0667, 0.3333], McNemar exact p=0.03125
- json_valid: mean difference +0.0000, bootstrap 95% CI [0, 0], McNemar exact p=1.0
- instruction_compliant: mean difference +0.1000, bootstrap 95% CI [0, 0.2333], McNemar exact p=0.25

## Interpretation

QAD Q4_0 is indistinguishable from BF16 on this small paired suite, while Q5_K_M has the highest exact-match rate. The QAD-vs-PTQ difference is directionally favorable to QAD, but the confidence intervals are exploratory and the prompt set is too small for a definitive claim.
