#!/usr/bin/env python3
"""Aggregate extended-suite scores across multiple benchmark seeds."""

import argparse
import json
import statistics
from pathlib import Path

from score_results import score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", default="prompts_extended.jsonl")
    ap.add_argument("--models", nargs="+", required=True, help="NAME=seed:path,seed:path,...")
    ap.add_argument("--json-out", default="results/seed_aggregate.json")
    ap.add_argument("--md-out", default="results/seed_aggregate.md")
    args = ap.parse_args()
    prompts = {json.loads(line)["id"]: json.loads(line)["prompt"] for line in Path(args.prompts).read_text().splitlines() if line.strip()}
    out = {}
    for spec in args.models:
        name, files = spec.split("=", 1)
        records = []
        per_seed = {}
        for part in files.split(","):
            seed, path = part.split(":", 1)
            rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
            scored = [score(row, prompts[row["id"]]) for row in rows if row.get("returncode") == 0]
            per_seed[seed] = {
                "n": len(scored),
                "exact_match": sum(r["exact_match"] for r in scored),
                "json_valid": sum(r["json_valid"] for r in scored),
                "instruction_compliant": sum(r["instruction_compliant"] for r in scored),
                "mean_elapsed_ms": round(statistics.mean(r["elapsed_ms"] for r in scored), 2),
            }
            records.extend(scored)
        out[name] = {
            "n": len(records),
            "exact_match": sum(r["exact_match"] for r in records),
            "json_valid": sum(r["json_valid"] for r in records),
            "instruction_compliant": sum(r["instruction_compliant"] for r in records),
            "mean_elapsed_ms": round(statistics.mean(r["elapsed_ms"] for r in records), 2),
            "per_seed": per_seed,
        }
    Path(args.json_out).write_text(json.dumps(out, indent=2) + "\n")
    lines = ["# Repeated-seed extended-suite comparison", "", "| Variant | Exact | JSON valid | Instruction-compliant | Mean elapsed (ms) |", "|---|---:|---:|---:|---:|"]
    for name, d in out.items():
        lines.append(f"| {name} | {d['exact_match']}/{d['n']} | {d['json_valid']}/{d['n']} | {d['instruction_compliant']}/{d['n']} | {d['mean_elapsed_ms']} |")
    lines += ["", "Per-seed counts are preserved in the JSON artifact."]
    Path(args.md_out).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
