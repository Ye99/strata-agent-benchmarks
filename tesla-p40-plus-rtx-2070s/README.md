# Strata on a Tesla P40 24 GB + RTX 2070 SUPER 8 GB: reproducing the setup on different GPUs

The parent README's tuning was measured on two RTX 4060 Ti 16 GB. This folder repeats the setup and the same
benchmark on a much weaker and older pair of cards, to answer the question the parent README leaves open: which
settings have to be re-tuned when the GPUs change, and which do not.

**Machine:** Tesla P40 24 GB (sm_61, x16 slot) + RTX 2070 SUPER 8 GB (sm_75, x4 slot), no P2P; Ryzen 9 5900X
(AVX2 only, no AVX-512); 91 GiB RAM; Ubuntu 26.04.1; NVIDIA driver 580.178.04; ZFS root. Model: Qwen3.8-Flash-Next
IQ3_S, images off. Strata commit `99f3dbd`, engine compiled locally (the releases ship no Linux engine).
**Date:** 2026-10-04.

## Result

**The card Strata rejects is the only usable one.** `setup.sh --check` reports the P40 as
`not supported - older than the RTX 20 series (compute capability 6.1; Strata needs 7.5 or newer)` and accepts the
2070 SUPER with `less than 12 GB of VRAM: Strata will run, but most experts stay on the CPU and it will be slow`.
Measured, that warning is the understatement: on 8 GB the expert cache holds **473 experts (0.99 GiB)** and cold
prefill falls to **27-28 tokens/s**, so a 30K-token prompt takes **18 minutes**. Decode (20-24 t/s) and the
conversation cache (1 s) are fine; prefill is what makes agent use impossible.

Strata's community Pascal path (`-DSTRATA_EXPERIMENTAL_SM60=ON`, `STRATA_EXPERIMENTAL_SM60=1`) builds for sm_61 and
changes everything: **8,891 expert slots** and a 10-13x faster prefill.

| IQ3_S, 262,144-token context | Expert slots | Cold prefill t/s (6K / 43K / 100K) | Decode t/s | Cached next-turn TTFT | Needle |
| --- | --- | --- | --- | --- | --- |
| RTX 2070 SUPER, `--kv-resident 16384`, conv 4096 | 473 | 28.5 / 27.4 / - | 22.3 / 22.0 | 1.21 s | 43K ok, 6K miss |
| **Tesla P40, same config** (experimental sm_61 engine) | **8,891** | **279 / 350 / 353** | 28.6 / 27.3 / 25.1 | 0.96-1.24 s | ok at 6K, 43K, 100K |
| same, setup's own defaults (32K context) | 508 | not run at depth | - | - | - |

Against the parent README's 4060 Ti (900-1,280 t/s prefill, 25-37 t/s decode), the P40 is still 2.6-3.6x slower on
prefill: Pascal has no tensor cores, and the engine's pre-sm_80 prompt-attention path is fp32 FMAs. But it is the
difference between an 18-minute prompt and an 86-second one. **VRAM, not the slot or the CPU, was the limit** -
consistent with the docs' "every extra GB holds ~700 more experts".

## Settings sweep (P40, 6K + 43K, one run each)

| Variant | Expert slots | Prefill t/s 6K / 43K | Decode t/s | Cached turn |
| --- | --- | --- | --- | --- |
| `--kv-resident 16384`, conv 4096, spec 4 (**chosen**) | 8,891 | 279 / 350 | 28.6 / 27.3 | 0.96 / 0.98 s |
| `--kv-resident 8192` | 8,891 | 279 / 350 | 27.8 / 27.9 | 0.91 / 0.96 s |
| `--kv-resident 32768` | 8,813 | 281 / 353 | 23.2 / 26.1 | 0.99 / 2.72 s |
| conversation cache 16384 MiB | 8,891 | 284 / 354 | 29.1 / 27.4 | 0.97 s |
| `--spec 6` | 8,890 | 283 / 354 | 24.5 / 24.5 | 0.96 s |
| `--kv k8v4` | - | did not start: `--kv k8v4 does not support --kv-resident streaming (yet)` | | |

Nothing moved except speculative depth: `--kv-resident` 8K/16K/32K is a wash because the expert arena absorbs the
difference (8,891 vs 8,813 slots), and a 16 GiB conversation cache buys nothing over 4 GiB while pushing RAM from
~60 to 78 GiB used of 91. Spec depth 6 loses ~4 t/s of decode (draft acceptance 0.56-0.60 vs 0.67-0.78), so **4 is
the optimum here too**, matching the 4060 Ti result. The knobs that mattered on the 4060 Ti (single GPU vs split,
PCIe slot) do not apply: one card only, and the conversation cache works on a single GPU.

**Chosen:** P40, `--max-context 262144 --kv int8 --kv-resident 16384 --spec 4 --spec-min-p 0.5
--conversation-cache-mib 4096 --conversation-cache-slots 4` - i.e. the parent README's config unchanged, only the
card and the engine build differ. `cfg-p40.json` is it.

## Toolchain: what a different GPU actually costs you

- **No Linux prebuilt engine** in any Strata release (the assets are Windows-only), so a new box compiles - 10-20 min.
- **sm_61 needs a CUDA 12.x toolkit**: CUDA 13 dropped sm_60/sm_70. Both engines coexist here - `engine/strata`
  (sm_75, CUDA 13.1) and `engine/strata-sm61` (sm_61, CUDA 12.4) - selected per config with `"exe"`.
- Ubuntu 26.04 ships CUDA in multiverse: `cuda-nvcc-13-1` + `cuda-cudart-dev-13-1` + `libcublas-dev-13-1` for the
  Turing card, `nvidia-cuda-toolkit` (12.4.131) for the Pascal one. No NVIDIA apt repo needed.
- **A CUDA 12.3 toolkit left over from an older release cannot compile on 26.04**: first
  `unsupported GNU version! gcc versions later than 12`, which `g++-12` + `-ccbin g++-12` clears (`CUDAHOSTCXX`
  does not; CMake's `-DCMAKE_CXX_COMPILER` only sets the C++ side), then a fatal header clash with glibc 2.43 -
  `exception specification is incompatible with that of previous function "cospi"` (also `sinpi`, `rsqrt`).
- Driver 580.178.04 supports CUDA 13.x, so moving the toolkit needed no driver change.
- Model files: 84 GB. Downloading from Hugging Face measured 9.6 MB/s (~2 h); copying from another machine over
  SSH ran at ~92 MB/s (16 min). Worth checking before starting a download.

## Files

- `mkcfg.py` - builds each variant's server config from the installed `strata-iq3_s.json`; `runvar.sh` starts one on
  :8090 and waits until loaded; `chain.sh` runs a list of variants and logs memory. `agent_bench.py` is the parent
  README's script, unchanged.
- `cfg-<variant>.json` - the configs actually run. `res-<variant>.json` and `log-<variant>.txt` - the raw runs
  (`chain.log` has the expert-slot and memory lines per variant). `server-<variant>.out` - engine start-up logs,
  including the expert-cache size each variant negotiated and the `k8v4` refusal.
- Paths in the committed copies read `~/p/bench-p40`; the working directory was renamed for publication so no host
  identifiers remain.

## Caveats

- **One run per cell** - differences under ~10% are noise.
- **The 6K needle is not a usable check on this box.** It failed in 5 of 7 runs at 6K and in 0 of 7 at 43K/100K, and
  the failures are two different things: two runs emitted only 8 tokens - a spurious refusal, reproduced directly
  (the same 6K prompt answered `I can't help with that.` in 1 of 3 trials), because a hidden "deployment passphrase"
  inside a wall of source code sometimes reads to the model like a secret-exfiltration attempt; the rest were
  normal-length answers that paraphrased or garbled the token, which the exact-substring test scores as a miss.
  Toggling `reasoning_effort` between `none` and `low` on the same prompt flipped the result in both directions, so
  at this depth pass/fail tracks the run, not the setting under test.
- The sm_61 build is upstream's community-tested path, not part of the ready-made engine; it is also the only
  supported way to use a Pascal card, and it needs a CUDA 12.x toolkit.
- RAM is the binding constraint for anything bigger: one instance sits at 54-60 GiB of 91 GiB, and the 16 GiB
  conversation-cache variant reached 78 GiB used / 13 GiB free. A second quant or a second instance does not fit.
- The 2070 SUPER row is one run at each depth (the 100K run was stopped once the 27 t/s prefill made it pointless).
- No real Claude Code task was run on this machine (Claude Code was not installed there); the numbers above are all
  from `agent_bench.py`.
