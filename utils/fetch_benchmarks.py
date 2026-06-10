"""Download benchmark subsets via the HuggingFace datasets-server API.

Writes normalized JSONL files ({"id", "problem", "gold"}) to tests/datasets/:
  - math500_50.jsonl  (HuggingFaceH4/MATH-500, first 50; gold = LaTeX answer)
  - gsm8k_50.jsonl    (openai/gsm8k main test, first 50; gold = value after ####)
  - aime25_30.jsonl   (math-ai/aime25, all 30; gold = integer string)

Usage: python utils/fetch_benchmarks.py
"""

import json
import os
import re

import requests

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "tests", "datasets")
API = "https://datasets-server.huggingface.co/rows"


def fetch_rows(dataset: str, config: str, split: str, count: int) -> list:
    rows = []
    offset = 0
    while len(rows) < count:
        batch = min(100, count - len(rows))
        resp = requests.get(API, params={
            "dataset": dataset, "config": config, "split": split,
            "offset": offset, "length": batch,
        }, timeout=60)
        resp.raise_for_status()
        data = resp.json()["rows"]
        if not data:
            break
        rows.extend(r["row"] for r in data)
        offset += len(data)
    return rows[:count]


def write_jsonl(path: str, items: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"wrote {len(items):3d} problems -> {path}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    math500 = fetch_rows("HuggingFaceH4/MATH-500", "default", "test", 50)
    write_jsonl(os.path.join(OUT_DIR, "math500_50.jsonl"), [
        {"id": r["unique_id"], "problem": r["problem"], "gold": r["answer"],
         "subject": r.get("subject", ""), "level": r.get("level", "")}
        for r in math500
    ])

    gsm8k = fetch_rows("openai/gsm8k", "main", "test", 50)
    items = []
    for i, r in enumerate(gsm8k):
        match = re.search(r"####\s*(.+)", r["answer"])
        gold = match.group(1).strip().replace(",", "") if match else r["answer"]
        items.append({"id": f"gsm8k_{i}", "problem": r["question"], "gold": gold})
    write_jsonl(os.path.join(OUT_DIR, "gsm8k_50.jsonl"), items)

    aime = fetch_rows("math-ai/aime25", "default", "test", 30)
    write_jsonl(os.path.join(OUT_DIR, "aime25_30.jsonl"), [
        {"id": f"aime25_{r['id']}", "problem": r["problem"], "gold": r["answer"]}
        for r in aime
    ])


if __name__ == "__main__":
    main()
