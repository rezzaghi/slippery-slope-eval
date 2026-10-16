# Slippery-slope eval

A learning project: an eval for a prompt-based classifier that detects slippery-slope fallacies.

```
pip install anthropic
export ANTHROPIC_API_KEY=...
python run_eval.py prompt.txt data/dev.jsonl
python run_eval.py prompt.txt data/test.jsonl
```

Past results are in `results/`.
