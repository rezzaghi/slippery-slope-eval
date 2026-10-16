"""Run a prompt-based classifier over a labeled dataset and score it.

Usage: python run_eval.py prompt.txt data/dev.jsonl
Needs ANTHROPIC_API_KEY set in the environment.
"""
import json
import sys
from collections import defaultdict

import anthropic

MODEL = "claude-opus-5-5"
LABELS = {"fallacy", "not_fallacy"}

client = anthropic.Anthropic()


def classify(prompt, text):
    """Send one input to the model and return (label, reason)."""
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=prompt,
        messages=[{"role": "user", "content": text}],
        output_config={"effort": "low"},
        # If the model declines, retry automatically on a fallback model.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        return "refused", ""
    reply = "".join(b.text for b in response.content if b.type == "text")
    label, reason = "unparseable", reply.strip()
    for line in reply.splitlines():
        if line.startswith("LABEL:"):
            label = line.removeprefix("LABEL:").strip()
        elif line.startswith("REASON:"):
            reason = line.removeprefix("REASON:").strip()
    if label not in LABELS:
        label = "unparseable"
    return label, reason


def main(prompt_path, cases_path):
    prompt = open(prompt_path).read()
    cases = [json.loads(line) for line in open(cases_path)]

    correct = 0
    by_difficulty = defaultdict(lambda: [0, 0])  # difficulty -> [correct, total]
    wrong = []

    for case in cases:
        predicted, reason = classify(prompt, case["input"])
        ok = predicted == case["label"]
        correct += ok
        by_difficulty[case["difficulty"]][0] += ok
        by_difficulty[case["difficulty"]][1] += 1
        if not ok:
            wrong.append((case, predicted, reason))
        print(f"{case['id']}: {'OK  ' if ok else 'MISS'} expected={case['label']} got={predicted}")

    print(f"\nAccuracy: {correct}/{len(cases)} = {correct / len(cases):.0%}")
    for difficulty, (c, t) in sorted(by_difficulty.items()):
        print(f"  {difficulty}: {c}/{t}")

    if wrong:
        print("\nWrong answers:")
        for case, predicted, reason in wrong:
            print(f"- {case['id']} expected {case['label']}, got {predicted}")
            print(f"  input:  {case['input']}")
            print(f"  reason: {reason}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
