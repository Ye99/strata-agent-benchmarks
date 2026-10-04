| Variant | Prompt tokens | Cold prefill t/s | Decode t/s | Turn-2 first token (s) | Cached tokens | Needle |
| --- | ---: | ---: | ---: | ---: | ---: | :---: |
| 2 GPUs, int8 KV, 32K KV in VRAM | 5,327 | 823.0 | 49.8 | 6.9 | 0 | no |
| 2 GPUs, int8 KV, 32K KV in VRAM | 5,704 | 884.3 | 53.0 | 7.2 | 0 | yes |
| 2 GPUs, int8 KV, 32K KV in VRAM | 34,979 | 1668.7 | 48.9 | 21.3 | 0 | yes |
| 2 GPUs, int8 KV, 32K KV in VRAM | 43,423 | 1782.6 | 48.8 | 24.7 | 0 | yes |
| 2 GPUs, int8 KV, 32K KV in VRAM | 82,738 | 1888.1 | 47.0 | 42.8 | 0 | yes |
| 2 GPUs, int8 KV, 32K KV in VRAM | 184,483 | 1996.4 | 45.1 | 92.4 | 0 | yes |
| 2 GPUs, q4_0 KV | 5,326 | 809.6 | 47.2 | 6.9 | 0 | yes |
| 2 GPUs, q4_0 KV | 5,703 | 886.0 | 51.2 | 7.2 | 0 | no |
| 2 GPUs, q4_0 KV | 34,977 | 1632.2 | 48.4 | 21.8 | 0 | yes |
| 2 GPUs, q4_0 KV | 43,422 | 1759.7 | 47.1 | 25.3 | 0 | no |
| 2 GPUs, q4_0 KV | 82,739 | 1850.6 | 38.4 | 43.8 | 0 | yes |
| 2 GPUs, q4_0 KV | 184,482 | 1956.4 | 41.5 | 94.2 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | 5,328 | 835.3 | 49.3 | 6.8 | 0 | no |
| 2 GPUs, 16K KV in VRAM | 5,702 | 895.3 | 50.7 | 7.2 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | 34,979 | 1701.8 | 50.1 | 21.0 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | 43,423 | 1808.2 | 49.2 | 24.6 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | 82,738 | 1903.5 | 46.1 | 42.8 | 0 | yes |
| 2 GPUs, 16K KV in VRAM | 184,483 | 1994.7 | 41.1 | 92.2 | 0 | yes |
| 2 GPUs, 64K KV in VRAM | 5,325 | 823.4 | 46.0 | 7.0 | 0 | no |
| 2 GPUs, 64K KV in VRAM | 5,703 | 886.8 | 55.8 | 7.2 | 0 | no |
| 2 GPUs, 64K KV in VRAM | 34,978 | 1672.7 | 45.8 | 21.4 | 0 | yes |
| 2 GPUs, 64K KV in VRAM | 43,423 | 1781.2 | 52.0 | 24.9 | 0 | yes |
| 2 GPUs, 64K KV in VRAM | 82,737 | 1905.1 | 48.2 | 43.2 | 0 | yes |
| 2 GPUs, 64K KV in VRAM | 184,483 | 1969.1 | 42.5 | 93.5 | 0 | yes |
| 1 GPU, no conversation cache | 5,327 | 595.1 | 36.8 | 10.9 | 0 | yes |
| 1 GPU, no conversation cache | 5,702 | 646.0 | 35.7 | 10.9 | 0 | no |
| 1 GPU, no conversation cache | 34,978 | 843.3 | 33.4 | 43.4 | 0 | yes |
| 1 GPU, no conversation cache | 43,422 | 878.5 | 35.1 | 51.8 | 0 | yes |
| 1 GPU, no conversation cache | 82,738 | 903.8 | 32.6 | 93.4 | 0 | yes |
| 1 GPU, no conversation cache | 184,484 | 894.7 | 28.1 | 208.4 | 0 | yes |
| 1 GPU + conversation cache (8 GiB) | 5,327 | 583.0 | 36.7 | 0.7 | 5,470 | yes |
| 1 GPU + conversation cache (8 GiB) | 5,704 | 628.4 | 35.7 | 0.8 | 5,861 | no |
| 1 GPU + conversation cache (8 GiB) | 34,979 | 835.6 | 32.4 | 1.0 | 35,132 | yes |
| 1 GPU + conversation cache (8 GiB) | 43,423 | 876.3 | 34.7 | 1.0 | 43,634 | yes |
| 1 GPU + conversation cache (8 GiB) | 82,738 | 902.7 | 29.2 | 1.1 | 82,901 | yes |
| 1 GPU + conversation cache (8 GiB) | 184,482 | 896.5 | 28.6 | 1.4 | 184,643 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | 5,326 | 594.6 | 35.5 | 0.9 | 5,483 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | 5,704 | 640.6 | 32.8 | 0.7 | 5,930 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | 34,978 | 840.3 | 34.2 | 0.8 | 35,114 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | 43,423 | 879.4 | 36.8 | 0.9 | 43,592 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | 82,738 | 908.0 | 32.7 | 1.2 | 82,901 | yes |
| 1 GPU + cache 16 GiB, 16K KV in VRAM (chosen) | 184,482 | 902.1 | 30.9 | 1.3 | 184,653 | yes |
| 1 GPU + cache, q4_0 KV | 5,327 | 604.3 | 36.9 | 0.7 | 5,466 | yes |
| 1 GPU + cache, q4_0 KV | 5,702 | 648.8 | 35.2 | 0.7 | 5,861 | no |
| 1 GPU + cache, q4_0 KV | 34,978 | 823.5 | 32.6 | 0.8 | 35,134 | yes |
| 1 GPU + cache, q4_0 KV | 43,424 | 861.0 | 34.8 | 0.8 | 43,714 | yes |
| 1 GPU + cache, q4_0 KV | 82,739 | 883.7 | 29.5 | 3.3 | 82,732 | yes |
| 1 GPU + cache, q4_0 KV | 184,483 | 881.0 | 29.6 | 1.2 | 184,638 | yes |
| 1 GPU + cache, speculative depth 6 | 5,327 | 603.5 | 36.5 | 0.7 | 5,475 | no |
| 1 GPU + cache, speculative depth 6 | 5,705 | 644.0 | 34.7 | 3.0 | 5,698 | no |
| 1 GPU + cache, speculative depth 6 | 34,979 | 843.8 | 32.8 | 3.2 | 34,972 | yes |
| 1 GPU + cache, speculative depth 6 | 43,421 | 878.7 | 38.0 | 0.8 | 43,617 | yes |
| 1 GPU + cache, speculative depth 6 | 82,738 | 906.5 | 33.3 | 3.8 | 82,731 | yes |
| 1 GPU + cache, speculative depth 6 | 184,483 | 900.3 | 29.8 | 1.3 | 184,658 | yes |
| 1 GPU + cache, 384K context (yarn 1.5) | 5,326 | 594.3 | 35.7 | 0.8 | 5,479 | yes |
| 1 GPU + cache, 384K context (yarn 1.5) | 5,705 | 639.6 | 40.5 | 0.7 | 5,863 | yes |
| 1 GPU + cache, 384K context (yarn 1.5) | 34,979 | 837.1 | 34.9 | 0.9 | 35,133 | yes |
| 1 GPU + cache, 384K context (yarn 1.5) | 43,422 | 874.7 | 36.1 | 0.9 | 43,605 | yes |
| 1 GPU + cache, 384K context (yarn 1.5) | 82,739 | 899.3 | 31.0 | 3.5 | 82,732 | yes |
| 1 GPU + cache, 384K context (yarn 1.5) | 184,482 | 895.6 | 28.6 | 1.4 | 184,660 | yes |
| 1 GPU on the x8 slot + cache 16 GiB, 16K KV in VRAM (deployed) | 5,326 | 915.2 | 36.2 | 0.7 | 5,469 | yes |
| 1 GPU on the x8 slot + cache 16 GiB, 16K KV in VRAM (deployed) | 5,704 | 972.8 | 37.3 | 0.8 | 5,846 | yes |
| 1 GPU on the x8 slot + cache 16 GiB, 16K KV in VRAM (deployed) | 34,979 | 1220.7 | 32.2 | 0.9 | 35,124 | yes |
| 1 GPU on the x8 slot + cache 16 GiB, 16K KV in VRAM (deployed) | 43,423 | 1279.0 | 35.6 | 0.9 | 43,589 | yes |
| 1 GPU on the x8 slot + cache 16 GiB, 16K KV in VRAM (deployed) | 82,739 | 1292.5 | 31.9 | 2.2 | 82,732 | yes |
| 1 GPU on the x8 slot + cache 16 GiB, 16K KV in VRAM (deployed) | 184,481 | 1263.0 | 24.8 | 1.4 | 184,640 | yes |
