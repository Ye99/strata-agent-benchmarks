# Agent success rate: Strata (Qwen3.8-Flash-Next IQ3_S) vs vLLM (Qwen3.8-27B INT4)

Both were driven by Claude Code through their own launchers (`claude-qwen-strata-iq3_s` and `claude-qwen-vllm`).
Question: which one is the better coding agent? Priority 1: success rate and trajectory length (turns); priority 2: speed.
Date: 2026-10-03. Machine: 2x RTX 4060 Ti 16 GB, 94 GB RAM.

## Result

6 small Python tasks x 3 attempts = 18 runs per backend. Each run starts from a fresh directory; success is decided by hidden checks
that the agent never sees (`tasks/*/verify.py`). "Turns" is Claude Code's `num_turns` for the run.

| Task | Strata: full passes / avg turns / avg time | vLLM: full passes / avg turns / avg time |
| --- | --- | --- |
| A: fix 3 bugs in a text-stats module (tests given) | 3/3, 7.0, 67 s | 3/3, 6.3, 133 s |
| B: build an inventory + storage module from a README | 3/3, 7.3, 130 s | 3/3, 7.3, 289 s |
| C: rename a function across 7 files, keep a similar name | 3/3, 31.3, 160 s | 3/3, 30.3, 318 s |
| D: fix a date bug from a bug report | 2/3, 7.3, 81 s | 3/3, 8.7, 157 s |
| E: write a `wc` clone from a spec | 3/3, 20.0, 245 s | 2/3, 27.0, 893 s |
| F: write an expression parser without `eval` (57 checks) | 3/3, 12.3, 231 s | 3/3, 9.0, 616 s |
| **All** | **17/18**, 14.2 turns (median 10), 152 s, ~4,200 output tokens | **17/18**, 14.8 turns (median 9.5), 401 s, ~12,500 output tokens |

- Success rate and turns are the same within noise (one miss each). Strata's miss (D, attempt 3) ended after 1 turn with
  "I'm ready - what would you like me to work on?" and never touched the task; vLLM's miss (E, attempt 2) passed 13 of 14
  checks and failed reading from stdin after 31 turns.
- Strata was about 2.6x faster per run; vLLM wrote about 3x as many output tokens per run (longer reasoning), so most of
  the gap is tokens, not decode speed.
- **Too easy to separate the models:** both are near the ceiling. A harder second round (larger refactors, longer
  trajectories) is needed to say which is the better agent.

## Setup and differences between the two sides

- Same prompts, same `CLAUDE_CODE_EFFORT_LEVEL=medium`, `--max-turns 40`, `--permission-mode default`, and the same tool
  allow-list: Read, Write, Edit, Glob, Grep, `python3 -m unittest`, `python3 *.py`, and read-only `ls cat grep head tail wc diff`.
  (Claude Code's own sandbox cannot start inside this VM, so scoped permissions were used instead of the sandbox.)
- The servers cannot share the GPUs: the Strata phase ran first, then Strata was stopped, vLLM ran, and Strata was restarted.
- Not identical: Strata used one GPU (the x8 slot) with a 262K context and a conversation cache; vLLM used both GPUs
  (tensor parallel 2, MTP-2, 163K context). Sampling and reasoning defaults come from each server and were left alone.
- 3 attempts per task is small; one run is 5.5 percentage points.

## Files

- `tasks/<task>/{start/,prompt.txt,verify.py}`: the starting project, the prompt and the hidden checks. `ref/` holds a
  reference solution per task; `sanity.sh` confirms that every starting state fails and every reference passes.
- `run_one.sh`: one run (launcher, task, attempt) -> one line in `results-<label>.jsonl`. `chain3.sh`: the two-phase
  sequence used here (it has this machine's launcher and vLLM paths). `summarize.py`: the table above from the JSONL files.
- `results-strata.jsonl`, `results-vllm.jsonl`: every run (turns, wall time, API time, tokens, checks passed, failed checks).
