# Two Strata instances, one per GPU

Question: Strata uses one GPU (GPU 1, x8 slot). Can a second instance on GPU 0 (x4 slot) double the throughput for two
Claude Code sessions?

**Machine:** the same as in the [main README](../README.md), but the VM was given more RAM (138 GB assigned, 132 GB
visible).

**Date:** 2026-10-04.

## Result

**No measurable gain.** Two sessions on two instances took as long, in total busy time, as two sessions sharing one
instance, and each run was about 1.6-2.5x slower than a run alone.

## Memory

- One resident instance: 52-59 GB RSS (the pinned experts) plus its conversation cache; about 72 GB for the VM.
- Two instances: peak 123 GiB "used" (a 16 GiB conversation cache each), lowest "available" 9.4 GiB. 128 GB is the
  least that worked here; 94 GB does not fit two.

## Benchmark: `scripts/agent_bench.py`

Depths 6K / 43K / 100K (prompts of about 5.3K, 30K and 88.6K tokens), one run each; raw results in `bench-A.json`
and `bench-B.json`.

| | GPU 1 alone | Both instances busy at once (GPU 1) | GPU 0 alone | Both busy (GPU 0) |
| --- | --- | --- | --- | --- |
| Decode tok/s | 36 / 27 / 31 | 17 / 19 / 18 | 34 / 18 / 27 | 14 / 18 / 31 |
| Cold prefill tok/s | 901 / 1,085 / 1,350 | 788 / 1,125 / 1,337 | 592 / 730 / 942 | 502 / 744 / 947 |
| Cached next-turn TTFT | 0.8-1.0 s | 1.5-2.0 s | 0.8-1.1 s | 1.8 s |

Prefill runs in parallel with almost no slowdown (it runs on each instance's own GPU and PCIe link). Decode halves
when both instances decode at once: the experts that the GPU does not hold run on the CPU, and the two instances share
its cores and the RAM bandwidth. (The 100K run on GPU 0 decoded after GPU 1 had finished, so it did not overlap.)

## Real Claude Code, two sessions (`run2.sh`)

Tasks A-F from [`agent-comparison/`](../agent-comparison/README.md), 2 attempts each = 12 runs. Worker 1 runs A, B and
C; worker 2 runs D, E and F in parallel. `shared`: both workers use the one instance on GPU 1. `dual`: worker 1 uses
GPU 1, worker 2 uses GPU 0.

| | Shared (1 instance) | Dual (2 instances) |
| --- | --- | --- |
| Total time, 12 runs | 2,111 s | 2,328 s |
| Sum of all runs' times | 3,796 s | 3,752 s |
| Average run | 316 s | 313 s (GPU 1: 238 s, GPU 0: 388 s) |
| Average turns | 13.3 | 14.3 |
| Passed | 12 / 12 | 10 / 12 (E_wc failed both times, on GPU 0) |

For reference, the same tasks run one at a time on one instance averaged 152 s
([`agent-comparison/`](../agent-comparison/README.md), measured earlier on this machine and not re-run on the day of
this test). So two sessions at once were no faster in total than running them one after the other.

## Caveats

- The total time is set by worker 2, whose tasks are heavier and which has one long run (F_expr attempt 1: 822 s
  shared, 921 s dual); the sum of run times is the fairer figure.
- One run per cell.
- The two E_wc failures on GPU 0 were not investigated; they could be model variance or the different expert placement
  on that card.
- Each instance used the engine's default CPU worker count; fewer workers per instance was not tried.

## Files

- `run2.sh`: the two-worker driver. It calls `ab/run_one.sh`; `ab` is a symlink to `../agent-comparison`, so the
  tasks are shared and each worker appends to `agent-comparison/results-<label>-w1.jsonl` or `-w2.jsonl`.
- `cc-url.sh`: Claude Code against `$CC_URL`, with the same environment as the launcher.
- `mk2.py` and `start2.sh`: start an instance on a given GPU and port.
- `results-shared.jsonl`, `results-dual.jsonl`: every run, with both workers' files combined (labels `<label>-w1`
  and `<label>-w2`).
