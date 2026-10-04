# Two Strata instances, one per GPU (2026-10-04)

Question: Strata uses one GPU (GPU 1, x8 slot). Can a second instance on GPU 0 (x4 slot) double the throughput for two
Claude Code sessions? Same machine as the main README, but the VM got more RAM (138 GB assigned, 132 GB visible).

**Answer: no measurable gain.** Two sessions on two instances took as long, in total busy time, as two sessions
sharing one instance, and each run was about 1.6-2.5x slower than a run alone.

## Memory

- One resident instance: 52-59 GB RSS (the pinned experts) plus its conversation cache; about 72 GB for the VM.
- Two instances: peak 123 GiB "used" (16 GiB conversation cache each), lowest "available" 9.4 GiB. 128 GB is the least that
  worked here; 94 GB does not fit two.

## Benchmark (`scripts/agent_bench.py`, 6K / 43K / 100K-token prompts, one run each; raw: `bench-A.json`, `bench-B.json`)

| | GPU 1 alone | both instances busy at once (GPU 1) | GPU 0 alone | both busy (GPU 0) |
| --- | --- | --- | --- | --- |
| Decode t/s | 36 / 27 / 31 | 17 / 19 / 18 | 34 / 18 / 27 | 14 / 18 / 31 |
| Cold prefill t/s | 901 / 1,085 / 1,350 | 788 / 1,125 / 1,337 | 592 / 730 / 942 | 502 / 744 / 947 |
| Cached next-turn start | 0.8-1.0 s | 1.5-2.0 s | 0.8-1.1 s | 1.8 s |

Prefill overlaps almost perfectly (it uses the GPU and PCIe). Decode halves when both decode at once: the experts the
GPU does not hold run on the CPU, and the two instances share its cores and the RAM bandwidth. (The 100K row on GPU 0
decoded after GPU 1 had finished, so it did not overlap.)

## Real Claude Code, two sessions (`run2.sh`)

Tasks A-F of `agent-comparison/`, 2 attempts each = 12 runs. Worker 1 runs A, B, C; worker 2 runs D, E, F, in parallel.
`shared`: both workers use the one instance on GPU 1. `dual`: worker 1 uses GPU 1, worker 2 uses GPU 0.

| | shared (1 instance) | dual (2 instances) |
| --- | --- | --- |
| Total time, 12 runs | 2,111 s | 2,328 s |
| Sum of all runs' time | 3,796 s | 3,752 s |
| Average run | 316 s | 313 s (GPU 1: 238 s, GPU 0: 388 s) |
| Average turns | 13.3 | 14.3 |
| Passed | 12 / 12 | 10 / 12 (E_wc failed both times, on GPU 0) |

For reference, the same tasks one at a time on one instance averaged 152 s (`agent-comparison/`, measured earlier on
this machine; not re-run on the day of this test). So two sessions at once were no faster in total than one after the other.

Caveats: the total time is set by worker 2, whose tasks are heavier and which has one long run (F_expr attempt 1: 822 s
shared, 921 s dual); the sum of run times is the fairer figure. One run per cell. The two E_wc failures on GPU 0 were
not investigated; they could be the model's variance or the different expert placement on that card. Each instance
used the engine's default CPU worker count; fewer workers per instance was not tried.

Files: `run2.sh` (the two-worker driver, uses `agent-comparison/run_one.sh` and `tasks/`), `cc-url.sh` (Claude Code against
`$CC_URL`, same environment as the launcher), `mk2.py` and `start2.sh` (start an instance on a given GPU and port),
`results-shared.jsonl`, `results-dual.jsonl`.
