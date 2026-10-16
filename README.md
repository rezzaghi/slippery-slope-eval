# Slippery-slope eval

A learning project: an eval for a prompt-based classifier that decides whether an argument is a slippery-slope fallacy.

## Layout

| File | What it is |
|---|---|
| `slippery-slope-fallacy.md` | The article the labels and prompt are based on |
| `LABELING.md` | Rules for labeling edge cases |
| `data/dev.jsonl` | 20 cases used while writing the prompt |
| `data/test.jsonl` | 10 held-out cases, not used to tune the prompt |
| `prompt.txt` | The classifier prompt |
| `run_eval.py` | Runs the prompt on a dataset through the Claude API and scores it |
| `results/` | Logs and raw predictions from past runs |

Each case has an `id`, `input`, expected `label` (`fallacy` or `not_fallacy`), `type`, `difficulty`, `contested` and `rationale`.

## Running

```
pip install anthropic
export ANTHROPIC_API_KEY=...
python run_eval.py prompt.txt data/dev.jsonl
python run_eval.py prompt.txt data/test.jsonl
```

## Results so far

One run, using Claude Code subagents as the model instead of the API: dev 19/20, test 10/10. The only miss is c15, where the model treated the opioid claim as common knowledge (rule 2) and the label says it isn't. See `results/`.

## Known limitations

- The prompt's "Not a fallacy" list was written after reading the dev cases, so the dev score is optimistic.
- The test set is all easy cases and several are near-copies of dev cases, so 100% says little.
- Only one run so far; scores may vary between runs.
