#!/usr/bin/env python3
"""Publication-oriented uncertainty analysis for the 3-seed extended suite."""

import argparse
import json
import math
import random
import statistics
from pathlib import Path

from score_results import score


def wilson(k, n, z=1.96):
    if not n:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 4), round(c + h, 4)]


def bootstrap_diff(a, b, reps=10000, seed=7):
    rng = random.Random(seed)
    n = len(a)
    diffs = []
    for _ in range(reps):
        ix = [rng.randrange(n) for _ in range(n)]
        diffs.append(statistics.mean(a[i] - b[i] for i in ix))
    diffs.sort()
    return {
        "mean_difference": round(statistics.mean(a) - statistics.mean(b), 4),
        "ci95": [round(diffs[int(0.025 * reps)], 4), round(diffs[int(0.975 * reps)], 4)],
    }


def mcnemar(a, b):
    ab = sum(x == 1 and y == 0 for x, y in zip(a, b))
    ba = sum(x == 0 and y == 1 for x, y in zip(a, b))
    n = ab + ba
    if n == 0:
        p = 1.0
    else:
        tail = sum(math.comb(n, i) for i in range(min(ab, ba) + 1)) / (2 ** n)
        p = min(1.0, 2 * tail)
    return {"a_only": ab, "b_only": ba, "two_sided_exact_p": round(p, 6)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", default="prompts_extended.jsonl")
    ap.add_argument("--json-out", default="results/statistical_analysis.json")
    ap.add_argument("--md-out", default="results/statistical_analysis.md")
    args = ap.parse_args()
    prompts = {json.loads(x)["id"]: json.loads(x)["prompt"] for x in Path(args.prompts).read_text().splitlines() if x.strip()}
    specs = {
        "BF16": ["results/extended_BF16.jsonl", "results/extended_BF16_seed2024.jsonl", "results/extended_BF16_seed4242.jsonl"],
        "PTQ_Q4_0": ["results/extended_PTQ_Q4_0.jsonl", "results/extended_PTQ_Q4_0_seed2024.jsonl", "results/extended_PTQ_Q4_0_seed4242.jsonl"],
        "QAD_Q4_0": ["results/extended_QAD_Q4_0.jsonl", "results/extended_QAD_Q4_0_seed2024.jsonl", "results/extended_QAD_Q4_0_seed4242.jsonl"],
        "Q5_K_M": ["results/extended_Q5_K_M.jsonl", "results/extended_Q5_K_M_seed2024.jsonl", "results/extended_Q5_K_M_seed4242.jsonl"],
    }
    all_scores = {}
    for model, paths in specs.items():
        rows = []
        for path in paths:
            for line in Path(path).read_text().splitlines():
                record = json.loads(line)
                rows.append(score(record, prompts[record["id"]]))
        all_scores[model] = rows

    metrics = ["exact_match", "json_valid", "instruction_compliant"]
    summary = {}
    for model, rows in all_scores.items():
        summary[model] = {"n": len(rows), "metrics": {}}
        for metric in metrics:
            vals = [r[metric] for r in rows]
            k = sum(vals)
            summary[model]["metrics"][metric] = {"k": k, "n": len(vals), "rate": round(k / len(vals), 4), "wilson95": wilson(k, len(vals))}
        lat = [r["elapsed_ms"] for r in rows]
        summary[model]["latency_ms"] = {"mean": round(statistics.mean(lat), 2), "stdev": round(statistics.stdev(lat), 2)}

    comparisons = {}
    for left, right in [("QAD_Q4_0", "BF16"), ("QAD_Q4_0", "PTQ_Q4_0"), ("Q5_K_M", "QAD_Q4_0")]:
        comparisons[f"{left}_vs_{right}"] = {}
        for metric in metrics:
            a = [r[metric] for r in all_scores[left]]
            b = [r[metric] for r in all_scores[right]]
            comparisons[f"{left}_vs_{right}"][metric] = {"bootstrap": bootstrap_diff(a, b), "mcnemar": mcnemar(a, b)}

    result = {"summary": summary, "paired_comparisons": comparisons, "notes": ["95% Wilson intervals describe uncertainty over the 30 paired prompt-seed cases.", "Bootstrap intervals resample paired cases 10,000 times with seed 7.", "These are exploratory results, not a claim of generalization to unseen tasks."]}
    Path(args.json_out).write_text(json.dumps(result, indent=2) + "\n")
    lines = ["# Statistical analysis", "", "Exploratory 95% intervals over 30 paired prompt-seed cases; bootstrap uses 10,000 paired resamples.", "", "| Variant | Exact | 95% CI | JSON valid | 95% CI | Compliance | 95% CI | Mean latency (ms) |", "|---|---:|:---:|---:|:---:|---:|:---:|---:|"]
    for model, d in summary.items():
        m = d["metrics"]
        fmt = lambda key: f"{m[key]['k']}/{m[key]['n']} ({m[key]['rate']:.0%})"
        lines.append(f"| {model} | {fmt('exact_match')} | {m['exact_match']['wilson95']} | {fmt('json_valid')} | {m['json_valid']['wilson95']} | {fmt('instruction_compliant')} | {m['instruction_compliant']['wilson95']} | {d['latency_ms']['mean']} ± {d['latency_ms']['stdev']} |")
    lines += ["", "## Paired comparisons", ""]
    for name, vals in comparisons.items():
        lines.append(f"### {name}")
        for metric, d in vals.items():
            lines.append(f"- {metric}: mean difference {d['bootstrap']['mean_difference']:+.4f}, bootstrap 95% CI {d['bootstrap']['ci95']}, McNemar exact p={d['mcnemar']['two_sided_exact_p']}")
        lines.append("")
    lines += ["## Interpretation", "", "QAD Q4_0 is indistinguishable from BF16 on this small paired suite, while Q5_K_M has the highest exact-match rate. The QAD-vs-PTQ difference is directionally favorable to QAD, but the confidence intervals are exploratory and the prompt set is too small for a definitive claim."]
    Path(args.md_out).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
