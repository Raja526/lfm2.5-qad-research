#!/usr/bin/env python3
"""Small, deterministic llama-cli benchmark harness for LFM2.5 checkpoints."""

import argparse
import json
import os
import subprocess
import time
from pathlib import Path


def load_prompts(path: Path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="llama-cli -hf repository or local model path")
    parser.add_argument("--variant", default=None, help="Optional GGUF filename for -hf")
    parser.add_argument("--prompts", default="prompts.jsonl")
    parser.add_argument("--output", required=True)
    parser.add_argument("--cli", default="llama-cli")
    parser.add_argument("--ctx-size", type=int, default=4096)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--threads", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=1234)
    args = parser.parse_args()

    prompts = load_prompts(Path(args.prompts))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    for item in prompts:
        command = [args.cli]
        if args.model.startswith("LiquidAI/") or "/" in args.model and not os.path.exists(args.model):
            command += ["-hf", args.model]
            if args.variant:
                command += ["--hf-file", args.variant]
        else:
            command += ["-m", args.model]
        command += [
            "-n", str(args.max_tokens),
            "--ctx-size", str(args.ctx_size),
            "--temp", str(args.temperature),
            "--seed", str(args.seed),
            "--no-display-prompt",
            "-p", item["prompt"],
        ]
        if args.threads:
            command += ["-t", str(args.threads)]

        started = time.perf_counter()
        completed = subprocess.run(command, capture_output=True, text=True)
        elapsed_ms = (time.perf_counter() - started) * 1000
        record = {
            "id": item["id"],
            "category": item["category"],
            "model": args.model,
            "variant": args.variant,
            "elapsed_ms": round(elapsed_ms, 2),
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "command": command,
        }
        with output.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"{item['id']}: {elapsed_ms:.0f} ms (exit {completed.returncode})")


if __name__ == "__main__":
    main()
