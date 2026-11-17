#!/usr/bin/env python3
"""Score benchmark JSONL outputs and write a compact comparison table."""

import argparse
import json
import re
from pathlib import Path


EXPECTED = {
    "extraction_01": {"name": "Anita Rao", "city": "Hyderabad", "amount": 1250},
    "extraction_02": {"active": True, "count": 7},
    "tool_01": {"function_name": "set_alarm", "time": "07:30"},
    "tool_02": {"function_name": "set_timer", "time": "5", "unit": "minutes"},
    "factual_01": "Tokyo",
    "factual_02": "Paris",
}


def answer_text(record, prompts):
    text = record.get("stdout", "")
    prompt = prompts.get(record["id"], "")
    if prompt in text:
        text = text.split(prompt, 1)[1]
    text = re.split(r"\n\[ Prompt:", text, maxsplit=1)[0]
    return text.strip().strip("> ").strip()


def fenced_json(text):
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S | re.I)
    candidate = match.group(1) if match else text
    match = re.search(r"\{.*\}", candidate, re.S)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def score(record, prompt):
    answer = answer_text(record, {record["id"]: prompt})
    category = record["category"]
    valid_json = fenced_json(answer) is not None
    exact = False
    compliant = record.get("returncode") == 0

    if category == "instruction_following":
        if record["id"] == "instruction_01":
            bullets = [line for line in answer.splitlines() if line.strip().startswith(("-", "*"))]
            exact = len(bullets) == 3 and len(bullets) == len([line for line in answer.splitlines() if line.strip()])
        else:
            exact = len([line for line in answer.splitlines() if line.strip()]) == 1 and answer.endswith(".")
        compliant = compliant and exact
    elif category == "structured_extraction":
        obj = fenced_json(answer)
        exact = obj == EXPECTED[record["id"]]
        compliant = compliant and obj is not None and set(obj) == set(EXPECTED[record["id"]])
    elif category == "tool_use":
        obj = fenced_json(answer) or {}
        if record["id"] == "tool_01":
            exact = obj.get("function_name") == "set_alarm" and obj.get("arguments") in (["tomorrow", "07:30"], ["07:30"])
        else:
            exact = obj.get("function_name") == "set_timer" and obj.get("arguments") in (["5", "minutes"], [5, "minutes"])
        args = obj.get("arguments", [])
        if record["id"] == "tool_01":
            compliant = compliant and obj.get("function_name") == "set_alarm" and "07:30" in args
        else:
            compliant = compliant and obj.get("function_name") == "set_timer" and ("5" in args or 5 in args)
    elif category == "factual_qa":
        exact = answer.strip().lower().rstrip(".") == EXPECTED[record["id"]].lower()
        compliant = compliant and exact
    elif category == "math":
        if record["id"] == "math_01":
            exact = bool(re.search(r"(?:4\s*[×x*]\s*10\s*\^?\s*8|4e\+?8|400[, ]?000[, ]?000|400\s*million)", answer, re.I))
        else:
            exact = bool(re.search(r"(?:15\s*%\s*of\s*200\s*=\s*30|15\s*/\s*100\s*[×x*]\s*200|\b30\b)", answer, re.I))
        compliant = compliant and exact

    return {
        "id": record["id"],
        "category": category,
        "exact_match": int(exact),
        "json_valid": int(valid_json),
        "instruction_compliant": int(compliant),
        "elapsed_ms": record.get("elapsed_ms"),
        "answer": answer,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", default="prompts.jsonl")
    ap.add_argument("--results", nargs="+", required=True)
    ap.add_argument("--json-out", default="results/score_comparison.json")
    ap.add_argument("--md-out", default="results/score_comparison.md")
    args = ap.parse_args()

    prompts = {json.loads(line)["id"]: json.loads(line)["prompt"] for line in Path(args.prompts).read_text().splitlines() if line.strip()}
    comparison = {}
    for path in args.results:
        rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
        scored = [score(row, prompts[row["id"]]) for row in rows if row.get("returncode") == 0]
        name = Path(path).stem
        comparison[name] = {
            "records": scored,
            "n": len(scored),
            "exact_match": sum(r["exact_match"] for r in scored),
            "json_valid": sum(r["json_valid"] for r in scored),
            "instruction_compliant": sum(r["instruction_compliant"] for r in scored),
            "mean_elapsed_ms": round(sum(r["elapsed_ms"] for r in scored) / len(scored), 2) if scored else None,
        }

    Path(args.json_out).write_text(json.dumps(comparison, indent=2, ensure_ascii=False) + "\n")
    lines = ["# LFM2.5-230M scoring comparison", "", "| Variant | Exact | JSON valid | Instruction-compliant | Mean elapsed (ms) |", "|---|---:|---:|---:|---:|"]
    for name, data in comparison.items():
        lines.append(f"| {name} | {data['exact_match']}/{data['n']} | {data['json_valid']}/{data['n']} | {data['instruction_compliant']}/{data['n']} | {data['mean_elapsed_ms']} |")
    Path(args.md_out).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
