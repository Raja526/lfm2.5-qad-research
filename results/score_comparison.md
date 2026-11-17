# LFM2.5-230M scoring comparison

| Variant | Exact (5) | JSON valid (5) | Instruction-compliant (5) | Mean elapsed (ms) |
|---|---:|---:|---:|---:|
| 230m_bf16 | 3/5 | 2/5 | 4/5 | 2391.53 |
| 230m_ptq_q4_0 | 3/5 | 2/5 | 3/5 | 4986.6 |
| 230m_qad | 3/5 | 2/5 | 4/5 | 1900.78 |
| 230m_q5_k_m | 4/5 | 2/5 | 4/5 | 5199.87 |
