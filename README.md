# Strata settings for Claude Code: 256K context on 2x RTX 4060 Ti

Measurements of [Strata](https://github.com/Niko1221/Strata) (engine 0.1.38) running Qwen3.8-Flash-Next IQ3_S as the
backend of Claude Code. Question: which settings give the best agent experience with a context of at least 256K tokens?

**Machine:** 2x RTX 4060 Ti 16 GB (no P2P), Ryzen 9 7900, 94 GB RAM, Ubuntu guest VM, NVIDIA driver 615.71.09.

**Date:** 2026-10-03.

## Result

Claude Code runs a serial loop that resends a 20-45K-token prompt every turn, and it interleaves its main requests with
small side requests (about 30K tokens in, 8 tokens out; apparently Bash-command checks). With Strata's two-GPU layer
split, each side request evicts the live conversation, so **every main turn re-reads its whole prompt**: about 25 s at
43K tokens and 92 s at 184K. Strata's conversation cache, which keeps several conversations parked in RAM, fixes this,
but it works only on a single GPU. One GPU decodes more slowly, but a cached turn starts in about 1 s, so for agent use
it wins.

| 262,144-token context | Decode tok/s (6K -> 184K prompt) | Cold prefill tok/s | TTFT of the next turn after a side request (5K / 43K / 184K prompt) |
| --- | --- | --- | --- |
| 2 GPUs, int8 KV | 50 -> 45 | 830 -> 2,000 | 7 s / 25 s / 92 s |
| 1 GPU, no cache | 37 -> 28 | 600 -> 900 | 11 s / 52 s / 208 s |
| **1 GPU + conversation cache, x4 slot** | 36 -> 29-31 | 600 -> 900 | **0.7-1 s / 1 s / 1.3 s** |
| **1 GPU + conversation cache, x8 slot** | 36 -> 25-27 | 915 -> 1,260 | 0.7-0.8 s / 0.85 s / 1.4 s |

TTFT is the time to first token.

Real Claude Code on a small pytest task (4-6 requests): 157 s on 2 GPUs, 139 s on 1 GPU with the cache. The task is
short and consists mostly of first-time reads, so it understates the cache's benefit;
[`results/claude-code-run.log`](results/claude-code-run.log) lists the reused tokens for each request.

**The PCIe slot matters.** The two cards sit in different slots: GPU 0 at x4 and GPU 1 at x8
(`nvidia-smi --query-gpu=index,pcie.link.width.current`; both cards report a maximum of x8, but GPU 0 negotiates x4 in
this machine). All single-GPU rows above except the x8-slot row ran on the x4 card. Moving to the x8 card
([`configs/cfg-G16x8.json`](configs/cfg-G16x8.json)) raised cold prefill by about 40-45% (1,280 vs 880 tok/s at 43K,
1,263 vs 900 at 184K), because experts stream over PCIe. Decode and cached-turn times did not change measurably (the
184K decode figures, 25 vs 31 tok/s, are one run each).

**Chosen engine arguments** ([`configs/cfg-G16x8.json`](configs/cfg-G16x8.json)): GPU 1 (x8 slot) only,
`--max-context 262144`, `--kv int8 --kv-resident 16384`, `--spec 4`,
`--conversation-cache-mib 16384 --conversation-cache-slots 4`. GPU 0 stays free.

Settings that made no measurable difference (within run-to-run noise): q4_0 KV cache, 16K or 64K of KV kept in VRAM,
speculative depth 6, and a 384K context (YaRN rope scaling factor 1.5, experimental beyond the trained 262,144; it
loaded and found the needle at 184K at the same speed). All of them held a 262,144-token context and found a needle
placed at 40% of a 184K-token prompt.

All individual runs: [`results/all-runs.md`](results/all-runs.md) (raw JSON in `results/`).

## Method

- [`scripts/agent_bench.py`](scripts/agent_bench.py): the context is real source code (the Strata repo) rather than
  random words, because code drafts well and random text does not. A passphrase sentence is inserted at 40% of the
  context and asked for in turn 1 (the needle check). Turn 2 sends the same prefix, the assistant's answer and a new
  question, preceded by an unrelated short "title" request, as Claude Code does. Greedy decoding, reasoning off,
  300 max tokens.
- Depths 6K and 50K (2 repetitions each), 120K and 190K (1 repetition each), with the same text slices for every
  variant.
- `scripts/mkcfg.py` builds each variant's server config; `runvar.sh` starts it on port 8090 and waits until it has
  loaded; `chain2.sh` benchmarks a list of variants one after another; `cc_task.sh` runs the real Claude Code task.
  The scripts contain this machine's paths (`/home/ye/p/Strata`).
- Only one server ran on the GPUs at a time.

## Caveats

- One run per cell: differences under about 10% are noise (decode tok/s varies with how many draft tokens are
  accepted, which depends on the text).
- The needle check passed in most runs; the few misses at 5K happened with reasoning off and are not tied to a setting.
- Only one model and one quantization (IQ3_S) were tested. IQ2_XS, Q2_0 and the Swift fine-tune need separate
  downloads and were not tried.
- The Claude Code task ran with tools limited to writing files in a scratch directory and running pytest.
- The 256K-context rows were measured with the engine's default adaptive expert placement, under which sampled output
  is not reproducible from run to run.

## Related experiments

### Agent success rate: Strata vs vLLM 27B

A second experiment compares Strata (Qwen3.8-Flash-Next IQ3_S) with vLLM (Qwen3.8-27B INT4) as the backend of Claude
Code on 6 small coding tasks x 3 attempts. Both passed 17 of 18 runs with about the same number of turns (14.2 vs
14.8), and Strata was about 2.6x faster per run (152 s vs 401 s). The tasks were too easy to separate the models.
Tables, method and code: [`agent-comparison/`](agent-comparison/README.md).

### Two instances, one per GPU

A second instance on GPU 0, alongside the first, did not help two Claude Code sessions: total run time was the same as
when both sessions shared one instance (decode is limited by the shared CPU and RAM bandwidth). Two instances need
128 GB of RAM. Details: [`two-instances/`](two-instances/README.md).

### Different GPUs: Tesla P40 24 GB + RTX 2070 SUPER 8 GB

The same setup on older, weaker cards. The 8 GB card holds 473 experts and prefills at 27 tok/s (18 minutes for a
30K-token prompt), while the P40, which `setup.sh --check` rejects (compute capability 6.1), runs 10-13x faster with
the experimental sm_61 build: 8,891 experts and 279-353 tok/s prefill. `--kv-resident`, the conversation-cache size
and the PCIe slot turned out not to matter there, and speculative depth 4 is again the optimum. Details:
[`tesla-p40-plus-rtx-2070s/`](tesla-p40-plus-rtx-2070s/README.md).
