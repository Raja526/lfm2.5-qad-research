# Warm throughput comparison

`llama-bench`, CPU-only, 6 threads, 512 prompt tokens, 128 generated tokens,
3 repetitions. Rates are tokens/second; model loading is excluded.

| Variant | File size (MB) | Prompt tok/s | Generation tok/s |
|---|---:|---:|---:|
| BF16 | 459.5 | 543.8 ± 14.3 | 50.0 ± 1.6 |
| PTQ Q4_0 | 146.7 | 827.0 ± 8.8 | 143.1 ± 3.4 |
| QAD Q4_0 | 146.7 | 826.2 ± 5.8 | 142.6 ± 3.9 |
| Q5_K_M | 169.2 | 927.8 ± 2.2 | 113.2 ± 1.1 |

QAD and standard PTQ Q4_0 have effectively identical throughput and file size;
QAD is about 2.85x faster than BF16 for generation in this run.
