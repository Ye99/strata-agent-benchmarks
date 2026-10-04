# Strata settings for Claude Code (agent use): 256K context on two RTX 4060 Ti

Measurements of [Strata](https://github.com/Niko1221/Strata) (engine 0.1.38) running Qwen3.8-Flash-Next at IQ3_S,
used as the backend of Claude Code. The question: which settings give the best agent experience with at least a
256K-token context?

**Machine:** 2x RTX 4060 Ti 16 GB (no P2P), Ryzen 9 7900, 94 GB RAM, Ubuntu guest VM, NVIDIA driver 615.71.09.
**Date:** 2026-10-03.

## Result

Claude Code is a serial loop that resends a 20-45K-token prompt every turn, and it alternates its main requests with
small side requests (about 30K tokens in, 8 tokens out, apparently Bash-command checks). With Strata's two-GPU layer
split, the side request replaces the live conversation, so **every main turn re-read its whole prompt**: about 25 s at
43K tokens and 92 s at 184K. Strata's conversation cache keeps several conversations parked in RAM and fixes that, but
it only works on a single GPU. One GPU decodes slower, but a cached turn starts in about 1 s, so for agent use it wins.

| 262,144-token context | Decode t/s (6K -> 184K prompt) | Cold prefill t/s | Next turn's first token after a side request (5K / 43K / 184K prompt) |
| --- | --- | --- | --- |
| 2 GPUs, int8 KV | 50 -> 45 | 830 -> 2,000 | 7 s / 25 s / 92 s |
| 1 GPU, no cache | 37 -> 28 | 600 -> 900 | 11 s / 52 s / 208 s |
| **1 GPU + conversation cache** (on the x4 slot) | 36 -> 29-31 | 600 -> 900 | **0.7-1 s / 1 s / 1.3 s** |
| **same, on the x8 slot** | 36 -> 25-27 | 915 -> 1,260 | 0.7-0.8 s / 0.85 s / 1.4 s |

Real Claude Code, a small pytest task, 4-6 requests: 157 s on 2 GPUs, 139 s on 1 GPU with the cache. The task is short
and mostly first-time reads, so the cache's benefit is understated; see `results/claude-code-run.log` for each request's
reused tokens.

**PCIe slot matters.** The two cards sit in different slots: GPU 0 at x4, GPU 1 at x8 (`nvidia-smi --query-gpu=index,pcie.link.width.current`: both cards report a max of x8, but GPU 0 negotiates x4 in this machine). All single-GPU rows above except the "x8 slot" one ran on the x4 card. Moving to the x8 card (`configs/cfg-G16x8.json`) raised cold prefill about 40-45% (1,280 vs 880 t/s at 43K, 1,263 vs 900 at 184K) because experts stream over PCIe; decode and cached-turn times did not change measurably (the 184K decode, 25 vs 31 t/s, is one run each).

**Chosen engine arguments** (`configs/cfg-G16x8.json`): GPU 1 (the x8 slot) only, `--max-context 262144`, `--kv int8 --kv-resident 16384`,
`--spec 4`, `--conversation-cache-mib 16384 --conversation-cache-slots 4`. GPU 0 stays free.

Things that made no measurable difference (within the run-to-run noise): q4_0 KV cache, 16K or 64K of KV kept in VRAM,
speculative depth 6, and a 384K context (yarn rope scaling factor 1.5, experimental past the trained 262,144; it loaded
and found the needle at 184K at the same speed). All of them held a 262,144 context and found a needle placed at 40%
of a 184K-token prompt.

All individual runs: [`results/all-runs.md`](results/all-runs.md) (raw JSON in `results/`).

## Agent success rate: Strata vs vLLM 27B

A second experiment compares Strata (Qwen3.8-Flash-Next IQ3_S) with vLLM (Qwen3.8-27B INT4) as the backend of Claude Code on
6 small coding tasks x 3 attempts: both passed 17 of 18 runs with about the same number of turns (14.2 vs 14.8), and Strata was
about 2.6x faster per run (152 s vs 401 s). The tasks were too easy to separate the models. Tables, method and code:
[`agent-comparison/`](agent-comparison/README.md).

## Two instances, one per GPU

A second instance on GPU 0 next to the first did not help two Claude Code sessions: total run time was the same as
sharing one instance (decode is limited by the shared CPU and RAM bandwidth). Two instances need 128 GB of RAM. Details:
[`two-instances/`](two-instances/README.md).

## Method

- `scripts/agent_bench.py`: the context is real source code (the Strata repo), not random words, because code drafts
  well and random text does not. A passphrase sentence is inserted at 40% of the context and asked for in turn 1
  (needle check). Turn 2 sends the same prefix, the assistant's answer and a new question, after an unrelated short
  "title" request, which is the Claude Code pattern. Greedy decoding, reasoning off, 300 max tokens.
- Depths 6K and 50K (2 repetitions), 120K and 190K (1 repetition); the same text slices for every variant.
- `scripts/mkcfg.py` builds each variant's server config, `runvar.sh` starts it on port 8090 and waits until loaded,
  `chain2.sh` runs the benchmark for a list of variants one after another, `cc_task.sh` runs the real Claude Code task.
  The scripts have this machine's paths (`/home/ye/p/Strata`) in them.
- Only one server at a time ran on the GPUs.

## Caveats

- One run per cell: differences under about 10% are noise (decode t/s moves with how well the draft tokens are
  accepted, which depends on the text).
- The needle check passed in most runs; the few misses at 5K were with reasoning off and are not tied to a setting.
- One quantization (IQ3_S) and one model were tested. IQ2_XS, Q2_0 and the Swift fine-tune would need other downloads
  and were not tried.
- The Claude Code task ran with tools limited to writing files in a scratch directory and running pytest.
- The 256K-context rows were measured with the engine's default adaptive expert placement; with it, sampled output
  is not reproducible run to run.
