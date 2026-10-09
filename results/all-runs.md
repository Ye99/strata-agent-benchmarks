# All runs

Every benchmark run on 2x RTX 4060 Ti, one row per run of [`scripts/agent_bench.py`](../scripts/agent_bench.py).
The Config column names the server config in [`configs/`](../configs/) (`cfg-<config>.json`); the raw results are in
`res-<config>-a.json` and `res-<config>-b.json` in this directory. TTFT is the time to first token. Summary:
[main README](../README.md).

| Variant | Config | Prompt tokens | Cold prefill tok/s | Decode tok/s | Turn-2 TTFT (s) | Cached tokens | Needle |
| --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |
| 2 GPUs, int8 KV, 32K KV in VRAM | L256 | 5,327 | 823.0 | 49.8 | 6.9 | 0 | no |
| 2 GPUs, int8 KV, 32K KV in VRAM | L256 | 5,704 | 884.3 | 53.0 | 7.2 | 0 | yes |
| 2 GPUs, int8 KV, 32K KV in VRAM | L256 | 34,979 | 1668.7 | 48.9 | 21.3 | 0 | yes |
| 2 GPUs, int8 KV, 32K KV in VRAM | L256 | 43,423 | 1782.6 | 48.8 | 24.7 | 0 | yes |
| 2 GPUs, int8 KV, 32K KV in VRAM | L256 | 82,738 | 1888.1 | 47.0 | 42.8 | 0 | yes |
| 2 GPUs, int8 KV, 32K KV in VRAM | L256 | 184,483 | 1996.4 | 45.1 | 92.4 | 0 | yes |
| 2 GPUs, q4_0 KV | L256q4 | 5,326 | 809.6 | 47.2 | 6.9 | 0 | yes |
| 2 GPUs, q4_0 KV | L256q4 | 5,703 | 886.0 | 51.2 | 7.2 | 0 | no |
| 2 GPUs, q4_0 KV | L256q4 | 34,977 | 1632.2 | 48.4 | 21.8 | 0 | yes |
| 2 GPUs, q4_0 KV | L256q4 | 43,422 | 1759.7 | 47.1 | 25.3 | 0 | no |
| 2 GPUs, q4_0 KV | L256q4 | 82,739 | 1850.6 | 38.4 | 43.8 | 0 | yes |
| 2 GPUs, q4_0 KV | L256q4 | 184,482 | 1956.4 | 41.5 | 94.2 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | L256r16 | 5,328 | 835.3 | 49.3 | 6.8 | 0 | no |
| 2 GPUs, 16K KV in VRAM | L256r16 | 5,702 | 895.3 | 50.7 | 7.2 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | L256r16 | 34,979 | 1701.8 | 50.1 | 21.0 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | L256r16 | 43,423 | 1808.2 | 49.2 | 24.6 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | L256r16 | 82,738 | 1903.5 | 46.1 | 42.8 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | L256r16 | 184,483 | 1994.7 | 41.1 | 92.2 | 0 | yes |
| 2 GPUs, 64K KV in VRAM | L256r64 | 5,325 | 823.4 | 46.0 | 7.0 | 0 | no |
| 2 GPUs, 64K KV in VRAM | L256r64 | 5,703 | 886.8 | 55.8 | 7.2 | 0 | no |
| 2 GPUs, 64K KV in VRAM | L256r64 | 34,978 | 1672.7 | 45.8 | 21.4 | 0 | yes |
| 2 GPUs, 64K KV in VRAM | L256r64 | 43,423 | 1781.2 | 52.0 | 24.9 | 0 | yes |
| 2 GPUs, 64K KV in VRAM | L256r64 | 82,737 | 1905.1 | 48.2 | 43.2 | 0 | yes |
| 2 GPUs, 64K KV in VRAM | L256r64 | 184,483 | 1969.1 | 42.5 | 93.5 | 0 | yes |
| 1 GPU, no conversation cache | L256g0 | 5,327 | 595.1 | 36.8 | 10.9 | 0 | yes |
| 1 GPU, no conversation cache | L256g0 | 5,702 | 646.0 | 35.7 | 10.9 | 0 | no |
| 1 GPU, no conversation cache | L256g0 | 34,978 | 843.3 | 33.4 | 43.4 | 0 | yes |
| 1 GPU, no conversation cache | L256g0 | 43,422 | 878.5 | 35.1 | 51.8 | 0 | yes |
| 1 GPU, no conversation cache | L256g0 | 82,738 | 903.8 | 32.6 | 93.4 | 0 | yes |
| 1 GPU, no conversation cache | L256g0 | 184,484 | 894.7 | 28.1 | 208.4 | 0 | yes |
| 1 GPU + cache 8 GiB | L256g0c | 5,327 | 583.0 | 36.7 | 0.7 | 5,470 | yes |
| 1 GPU + cache 8 GiB | L256g0c | 5,704 | 628.4 | 35.7 | 0.8 | 5,861 | no |
| 1 GPU + cache 8 GiB | L256g0c | 34,979 | 835.6 | 32.4 | 1.0 | 35,132 | yes |
| 1 GPU + cache 8 GiB | L256g0c | 43,423 | 876.3 | 34.7 | 1.0 | 43,634 | yes |
| 1 GPU + cache 8 GiB | L256g0c | 82,738 | 902.7 | 29.2 | 1.1 | 82,901 | yes |
| 1 GPU + cache 8 GiB | L256g0c | 184,482 | 896.5 | 28.6 | 1.4 | 184,643 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | G16 | 5,326 | 594.6 | 35.5 | 0.9 | 5,483 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | G16 | 5,704 | 640.6 | 32.8 | 0.7 | 5,930 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | G16 | 34,978 | 840.3 | 34.2 | 0.8 | 35,114 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | G16 | 43,423 | 879.4 | 36.8 | 0.9 | 43,592 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | G16 | 82,738 | 908.0 | 32.7 | 1.2 | 82,901 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | G16 | 184,482 | 902.1 | 30.9 | 1.3 | 184,653 | yes |
| 1 GPU + cache, q4_0 KV | Gq4 | 5,327 | 604.3 | 36.9 | 0.7 | 5,466 | yes |
| 1 GPU + cache, q4_0 KV | Gq4 | 5,702 | 648.8 | 35.2 | 0.7 | 5,861 | no |
| 1 GPU + cache, q4_0 KV | Gq4 | 34,978 | 823.5 | 32.6 | 0.8 | 35,134 | yes |
| 1 GPU + cache, q4_0 KV | Gq4 | 43,424 | 861.0 | 34.8 | 0.8 | 43,714 | yes |
| 1 GPU + cache, q4_0 KV | Gq4 | 82,739 | 883.7 | 29.5 | 3.3 | 82,732 | yes |
| 1 GPU + cache, q4_0 KV | Gq4 | 184,483 | 881.0 | 29.6 | 1.2 | 184,638 | yes |
| 1 GPU + cache, speculative depth 6 | Gs6 | 5,327 | 603.5 | 36.5 | 0.7 | 5,475 | no |
| 1 GPU + cache, speculative depth 6 | Gs6 | 5,705 | 644.0 | 34.7 | 3.0 | 5,698 | no |
| 1 GPU + cache, speculative depth 6 | Gs6 | 34,979 | 843.8 | 32.8 | 3.2 | 34,972 | yes |
| 1 GPU + cache, speculative depth 6 | Gs6 | 43,421 | 878.7 | 38.0 | 0.8 | 43,617 | yes |
| 1 GPU + cache, speculative depth 6 | Gs6 | 82,738 | 906.5 | 33.3 | 3.8 | 82,731 | yes |
| 1 GPU + cache, speculative depth 6 | Gs6 | 184,483 | 900.3 | 29.8 | 1.3 | 184,658 | yes |
| 1 GPU + cache, 384K context (YaRN 1.5) | G384 | 5,326 | 594.3 | 35.7 | 0.8 | 5,479 | yes |
| 1 GPU + cache, 384K context (YaRN 1.5) | G384 | 5,705 | 639.6 | 40.5 | 0.7 | 5,863 | yes |
| 1 GPU + cache, 384K context (YaRN 1.5) | G384 | 34,979 | 837.1 | 34.9 | 0.9 | 35,133 | yes |
| 1 GPU + cache, 384K context (YaRN 1.5) | G384 | 43,422 | 874.7 | 36.1 | 0.9 | 43,605 | yes |
| 1 GPU + cache, 384K context (YaRN 1.5) | G384 | 82,739 | 899.3 | 31.0 | 3.5 | 82,732 | yes |
| 1 GPU + cache, 384K context (YaRN 1.5) | G384 | 184,482 | 895.6 | 28.6 | 1.4 | 184,660 | yes |
| 1 GPU (x8 slot) + cache 16 GiB, 16K KV in VRAM (deployed) | G16x8 | 5,326 | 915.2 | 36.2 | 0.7 | 5,469 | yes |
| 1 GPU (x8 slot) + cache 16 GiB, 16K KV in VRAM (deployed) | G16x8 | 5,704 | 972.8 | 37.3 | 0.8 | 5,846 | yes |
| 1 GPU (x8 slot) + cache 16 GiB, 16K KV in VRAM (deployed) | G16x8 | 34,979 | 1220.7 | 32.2 | 0.9 | 35,124 | yes |
| 1 GPU (x8 slot) + cache 16 GiB, 16K KV in VRAM (deployed) | G16x8 | 43,423 | 1279.0 | 35.6 | 0.9 | 43,589 | yes |
| 1 GPU (x8 slot) + cache 16 GiB, 16K KV in VRAM (deployed) | G16x8 | 82,739 | 1292.5 | 31.9 | 2.2 | 82,732 | yes |
| 1 GPU (x8 slot) + cache 16 GiB, 16K KV in VRAM (deployed) | G16x8 | 184,481 | 1263.0 | 24.8 | 1.4 | 184,640 | yes |
