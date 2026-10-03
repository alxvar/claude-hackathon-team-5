# Duel records

_Written by `uv run python -m agents.duelist review`. One `duel-<id>.json` per duel holds everything; `feed.jsonl` holds the public feed's duel events (they may name the team behind an alias); `scores.jsonl` our duel points over time._

| duel | session | rival | role | limit | our_first | our_last | moves | status | price | day | surplus | points | pred | avg_s | max_s | cost_usd | fallbacks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 103 | Practice duels | Rival Oro | buyer | 129 | 85 | 88 | 2 | no_deal |  |  |  | 0.0 |  | 4.7 | 4.82 | 0.0099 | 0 |
| 104 | Practice duels | Rival Azul | seller | 69 | 98 | 95 | 2 | no_deal |  |  |  | 0.0 |  | 5.3 | 5.67 | 0.0098 | 0 |
| 105 | Practice duels | Rival Azul | seller | 74 | 118 | 113 | 4 | no_deal |  |  |  | 0.0 |  | 5.0 | 7.68 | 0.0182 | 1 |
| 106 | Practice duels | Rival Oro | buyer | 96 | 62 | 66 | 4 | no_deal |  |  |  | 0.0 |  | 4.4 | 6.81 | 0.0175 | 1 |
| 113 | Practice duels | Rival Verde | seller | 51 | 85 | 81 | 4 | no_deal |  |  |  | 0.0 |  | 4.2 | 5.94 | 0.0194 | 1 |
| 114 | Practice duels | Rival Luna | buyer | 93 | 55 | 58 | 2 | deal | 58.0 |  | 35.0 | 32.9 | 32.9 | 5.3 | 5.67 | 0.0105 | 0 |
| 115 | Practice duels | Rival Noche | seller | 69 | 98 | 98 | 1 | no_deal |  |  |  | 0.0 |  | 4.8 | 4.81 | 0.0038 | 0 |
| 116 | Practice duels | Rival Oro | buyer | 140 | 85 | 123 | 6 | no_deal |  |  |  | 0.0 |  | 0.9 | 5.18 | 0.0037 | 0 |
| 119 | Practice duels | Rival Plata | buyer | 180 | 110 | 110 | 1 | no_deal |  |  |  | 0.0 |  | 5.4 | 5.44 | 0.0042 | 0 |
| 120 | Practice duels | Rival Rojo | seller | 53 | 85 | 85 | 1 | no_deal |  |  |  | 0.0 |  | 6.9 | 6.87 | 0.0041 | 0 |
| 121 | Practice duels | Rival Sol | seller | 74 | 118 | 96 | 5 | deal | 100.0 |  | 26.0 | 20.3 | 20.3 | 6.0 | 7.11 | 0.036 | 0 |
| 122 | Practice duels | Rival Noche | buyer | 130 | 80 | 105 | 5 | deal | 105.0 |  | 25.0 | 19.5 | 19.5 | 6.2 | 9.3 | 0.0353 | 0 |
| 163 | Practice duels | Rival Rojo | seller | 69 | 98 | 91 | 5 | deal | 91.0 |  | 22.0 | 20.7 | 20.7 | 4.4 | 5.98 | 0.0259 | 1 |
| 164 | Practice duels | Rival Luna | buyer | 79 | 52 | 52 | 1 | deal | 52.0 |  | 27.0 | 27.0 | 27.0 | 11.1 | 11.05 | 0.0043 | 0 |
| 175 | Practice duels | Rival Verde | seller | 80 | 130 | 118 | 6 | deal | 118.0 |  | 38.0 | 26.2 | 26.2 | 6.4 | 8.8 | 0.0462 | 0 |
| 176 | Practice duels | Rival Plata | buyer | 107 | 72 | 80 | 5 | deal | 80.0 |  | 27.0 | 19.8 | 19.8 | 6.4 | 7.25 | 0.0336 | 0 |
| 181 | Practice duels | Rival Verde | buyer | 85 | 50 | 67 | 6 | no_deal |  |  |  | 0.0 |  | 4.6 | 6.43 | 0.0361 | 1 |
| 182 | Practice duels | Rival Oro | seller | 59 | 95 | 70 | 6 | no_deal |  |  |  | 0.0 |  | 0.8 | 5.09 | 0.004 | 0 |
| 199 | Practice duels | Rival Oro | buyer | 150 | 90 | 96 | 3 | deal | 97.0 |  | 53.0 | 46.8 | 46.8 | 5.5 | 6.81 | 0.0158 | 0 |
| 200 | Practice duels | Rival Noche | seller | 68 | 104 | 104 | 2 | deal | 102.0 |  | 34.0 | 32.0 | 32.0 | 5.6 | 5.92 | 0.0107 | 0 |
| 227 | Practice duels | Rival Luna | seller | 130 | 185 | 156 | 5 | deal | 152.0 |  | 22.0 | 17.2 | 17.2 | 8.1 | 14.24 | 0.0336 | 0 |
| 228 | Practice duels | Rival Verde | buyer | 138 | 105 | 117 | 5 | deal | 117.0 |  | 21.0 | 17.4 | 17.4 | 6.3 | 7.24 | 0.0329 | 0 |
| 2296 | Duels I | Rival Sol | seller | 87 | 135 | 101 | 7 | deal | 97.0 |  | 10.0 | 6.9 | 6.9 | 6.1 | 6.6 | 0.0548 | 0 |
| 2297 | Duels I | Rival Plata | buyer | 175 | 130 | 157 | 5 | deal | 161.0 |  | 14.0 | 10.9 | 10.9 | 6.1 | 6.71 | 0.0336 | 0 |
| 2314 | Duels I | Rival Oro | buyer | 75 | 45 | 68 | 5 | deal | 68.0 |  | 7.0 | 6.6 | 6.6 | 6.4 | 7.42 | 0.0479 | 0 |
| 2315 | Duels I | Rival Oro | seller | 64 | 96 | 72 | 5 | deal | 72.0 |  | 8.0 | 7.5 | 7.5 | 6.6 | 8.05 | 0.0411 | 0 |
| 2318 | Duels I | Rival Sol | seller | 74 | 115 | 85 | 9 | deal | 85.0 |  | 11.0 | 6.3 | 6.3 | 6.1 | 6.92 | 0.0875 | 0 |
| 2319 | Duels I | Rival Oro | buyer | 97 | 55 | 91 | 10 | deal | 91.0 |  | 6.0 | 3.4 | 3.4 | 5.3 | 6.39 | 0.0901 | 0 |
| 2356 | Duels I | Rival Plata | seller | 101 | 150 | 117 | 10 | deal | 117.0 |  | 16.0 | 8.6 | 8.6 | 7.8 | 25.0 | 0.0976 | 1 |
| 2357 | Duels I | Rival Noche | buyer | 92 | 55 | 77 | 7 | deal | 78.0 |  | 14.0 | 9.7 | 9.7 | 5.1 | 6.73 | 0.0488 | 0 |
| 2366 | Duels I | Rival Oro | seller | 101 | 165 | 110 | 5 | deal | 110.0 |  | 9.0 | 6.6 | 6.6 | 6.6 | 8.84 | 0.0569 | 0 |
| 2367 | Duels I | Rival Oro | buyer | 72 | 44 | 69 | 5 | no_deal |  |  |  | 0.0 |  | 6.4 | 8.52 | 0.0641 | 0 |
| 2414 | Duels I | Rival Verde | seller | 60 | 95 | 71 | 8 | no_deal |  |  |  | 0.0 |  | 0.6 | 4.75 | 0.0043 | 0 |
| 2415 | Duels I | Rival Rojo | buyer | 95 | 55 | 83 | 8 | no_deal |  |  |  | 0.0 |  | 0.7 | 5.44 | 0.0041 | 0 |
| 2430 | Duels I | Rival Oro | buyer | 192 | 150 | 177 | 6 | deal | 184.0 |  | 8.0 | 6.6 | 6.6 | 5.5 | 8.95 | 0.0537 | 0 |
| 2431 | Duels I | Rival Verde | seller | 125 | 175 | 145 | 6 | deal | 134.0 |  | 9.0 | 7.5 | 7.5 | 5.5 | 6.91 | 0.053 | 0 |
| 2446 | Duels I | Rival Oro | buyer | 73 | 45 | 45 | 1 | deal | 45.0 |  | 28.0 | 28.0 | 28.0 | 5.2 | 5.17 | 0.0036 | 0 |
| 2447 | Duels I | Rival Verde | seller | 86 | 130 | 122 | 3 | deal | 118.0 |  | 32.0 | 28.3 | 28.3 | 3.6 | 5.62 | 0.0096 | 0 |
| 2460 | Duels I | Rival Azul | seller | 172 | 260 | 198 | 11 | deal | 198.0 |  | 26.0 | 14.0 | 14.0 | 5.5 | 6.65 | 0.1048 | 0 |
| 2461 | Duels I | Rival Sol | buyer | 170 | 95 | 150 | 14 | deal | 150.0 |  | 20.0 | 9.5 | 9.5 | 5.9 | 9.16 | 0.1342 | 0 |
| 2472 | Duels I | Rival Sol | seller | 80 | 130 | 88 | 8 | deal | 92.0 |  | 12.0 | 11.3 | 11.3 | 3.9 | 8.54 | 0.0374 | 0 |
| 2473 | Duels I | Rival Rojo | buyer | 94 | 55 | 90 | 7 | deal | 88.0 |  | 6.0 | 5.6 | 5.6 | 3.9 | 6.71 | 0.0321 | 0 |
| 2494 | Duels I | Rival Sol | seller | 57 | 95 | 74 | 7 | deal | 74.0 |  | 17.0 | 15.0 | 15.0 | 5.4 | 7.5 | 0.0427 | 0 |
| 2495 | Duels I | Rival Rojo | buyer | 124 | 70 | 107 | 8 | deal | 107.0 |  | 17.0 | 17.0 | 17.0 | 0.7 | 5.7 | 0.0039 | 0 |
| 2506 | Duels I | Rival Noche | buyer | 103 | 62 | 98 | 8 | deal | 96.0 |  | 7.0 | 4.8 | 4.8 | 6.2 | 8.94 | 0.0697 | 1 |
| 2507 | Duels I | Rival Rojo | seller | 100 | 160 | 101 | 8 | deal | 106.0 |  | 6.0 | 3.9 | 3.9 | 6.5 | 7.34 | 0.0834 | 0 |
| 2522 | Duels I | Rival Plata | seller | 44 | 72 | 61 | 9 | deal | 59.0 |  | 15.0 | 9.7 | 9.7 | 5.8 | 6.07 | 0.0757 | 0 |
| 2523 | Duels I | Rival Noche | buyer | 196 | 110 | 170 | 8 | no_deal |  |  |  | 0.0 |  | 0.7 | 5.52 | 0.004 | 0 |
| 2530 | Duels I | Rival Azul | seller | 87 | 125 | 101 | 6 | deal | 97.0 |  | 10.0 | 8.8 | 8.8 | 5.2 | 6.87 | 0.0388 | 0 |
| 2531 | Duels I | Rival Sol | buyer | 146 | 95 | 95 | 2 | deal | 101.0 |  | 45.0 | 42.3 | 42.3 | 5.7 | 5.87 | 0.009 | 0 |
| 2534 | Duels I | Rival Sol | seller | 129 | 175 | 167 | 4 | deal | 167.0 |  | 38.0 | 29.7 | 29.7 | 5.6 | 6.95 | 0.0301 | 0 |
| 2535 | Duels I | Rival Noche | buyer | 219 | 150 | 176 | 4 | deal | 176.0 |  | 43.0 | 33.6 | 33.6 | 6.2 | 8.19 | 0.0551 | 0 |
| 2540 | Duels I | Rival Luna | seller | 71 | 110 | 90 | 8 | deal | 90.0 |  | 19.0 | 12.3 | 12.3 | 6.4 | 14.53 | 0.0883 | 0 |
| 2541 | Duels I | Rival Azul | buyer | 108 | 65 | 87 | 7 | deal | 87.0 |  | 21.0 | 14.5 | 14.5 | 5.3 | 8.05 | 0.0441 | 0 |
| 257 | Practice duels | Rival Oro | seller | 78 | 115 | 103 | 4 | deal | 103.0 |  | 25.0 | 20.8 | 20.8 | 6.0 | 7.38 | 0.0323 | 0 |
| 258 | Practice duels | Rival Noche | buyer | 64 | 38 | 38 | 1 | deal | 38.0 |  | 26.0 | 26.0 | 26.0 | 4.8 | 4.79 | 0.0037 | 0 |
| 2584 | Duels I | Rival Verde | seller | 122 | 175 | 175 | 1 | deal | 175.0 |  | 53.0 | 49.8 | 49.8 | 5.9 | 6.45 | 0.0093 | 0 |
| 2585 | Duels I | Rival Rojo | buyer | 160 | 95 | 95 | 2 | deal | 96.0 |  | 64.0 | 60.2 | 60.2 | 2.8 | 5.56 | 0.0037 | 0 |
| 269 | Practice duels | Rival Rojo | seller | 81 | 112 | 95 | 6 | deal | 95.0 |  | 14.0 | 9.7 | 9.7 | 7.1 | 10.13 | 0.0442 | 0 |
| 270 | Practice duels | Rival Verde | buyer | 102 | 72 | 76 | 2 | deal | 72.0 |  | 30.0 | 28.2 | 28.2 | 7.0 | 7.8 | 0.0127 | 0 |
| 271 | Practice duels | Rival Noche | seller | 87 | 125 | 112 | 4 | deal | 112.0 |  | 25.0 | 23.5 | 23.5 | 3.0 | 6.59 | 0.0105 | 0 |
| 272 | Practice duels | Rival Oro | buyer | 128 | 80 | 105 | 5 | deal | 105.0 |  | 23.0 | 18.0 | 18.0 | 5.9 | 6.05 | 0.0317 | 0 |
| 277 | Practice duels | Rival Plata | seller | 119 | 175 | 125 | 12 | deal | 132.0 |  | 13.0 | 6.6 | 6.6 | 6.3 | 8.68 | 0.1143 | 0 |
| 278 | Practice duels | Rival Oro | buyer | 116 | 80 | 104 | 11 | deal | 111.0 |  | 5.0 | 2.7 | 2.7 | 5.7 | 8.79 | 0.0865 | 0 |
| 31 | Practice duels | Rival Sol | seller | 111 | 165 | 165 | 1 | no_deal |  |  |  | 0.0 |  | 7.1 | 7.13 | 0.0043 | 0 |
| 32 | Practice duels | Rival Verde | buyer | 160 | 95 | 95 | 1 | no_deal |  |  |  | 0.0 |  | 7.6 | 7.57 | 0.0041 | 0 |
| 5616 | Duels II | Rival Verde | seller | 69 | 128 | 102 | 6 | deal | 105.0 | 0 | 36.0 | 33.1 | 33.1 | 9.6 | 14.5 | 0.0989 | 0 |
| 5617 | Duels II | Rival Verde | buyer | 88 | 35 | 64 | 5 | no_deal |  |  |  | 0.0 |  | 8.5 | 9.71 | 0.0881 | 0 |
| 5618 | Duels II | Rival Azul | buyer | 50 | 12 | 24 | 5 | no_deal |  |  |  | 0.0 |  | 9.2 | 11.48 | 0.108 | 0 |
| 5619 | Duels II | Rival Oro | seller | 123 | 182 | 140 | 7 | no_deal |  |  |  | 0.0 |  | 8.9 | 11.57 | 0.1253 | 0 |
| 5622 | Duels II | Rival Plata | seller | 83 | 135 | 92 | 6 | no_deal |  |  |  | 0.0 |  | 8.8 | 10.14 | 0.1259 | 0 |
| 5623 | Duels II | Rival Azul | buyer | 119 | 70 | 91 | 6 | deal | 97.0 | 5 | 22.0 | 2.6 | 2.7 | 7.9 | 12.02 | 0.0912 | 0 |
| 5652 | Duels II | Rival Verde | seller | 63 | 105 | 100 | 3 | deal | 98.0 | 10 | 35.0 | 52.9 | 52.9 | 8.7 | 12.41 | 0.0987 | 0 |
| 5653 | Duels II | Rival Verde | buyer | 114 | 55 | 74 | 5 | deal | 74.0 | 10 | 40.0 | 11.0 | 11.0 | 9.7 | 11.06 | 0.0807 | 0 |
| 5662 | Duels II | Rival Noche | seller | 79 | 145 | 110 | 8 | deal | 100.0 | 5 | 21.0 | 26.9 | 26.9 | 7.8 | 12.58 | 0.1295 | 0 |
| 5663 | Duels II | Rival Verde | buyer | 72 | 52 | 57 | 5 | deal | 61.0 | 5 | 11.0 | 4.0 | 4.0 | 6.7 | 13.6 | 0.0851 | 0 |
| 5706 | Duels II | Rival Rojo | buyer | 122 | 80 | 115 | 4 | deal | 115.0 | 0 | 7.0 | 6.4 | 6.4 | 7.3 | 9.18 | 0.058 | 0 |
| 5707 | Duels II | Rival Azul | seller | 77 | 115 | 103 | 5 | deal | 90.0 | 0 | 13.0 | 11.0 | 11.0 | 7.9 | 13.6 | 0.0632 | 0 |
| 5736 | Duels II | Rival Sol | seller | 111 | 160 | 157 | 4 | deal | 165.0 | 2 | 54.0 | 43.3 | 43.3 | 7.3 | 11.57 | 0.0783 | 0 |
| 5737 | Duels II | Rival Oro | buyer | 78 | 44 | 47 | 3 | deal | 54.0 | 2 | 24.0 | 16.3 | 16.3 | 9.2 | 12.44 | 0.0899 | 0 |
| 5796 | Duels II | Rival Luna | seller | 93 | 145 | 141 | 3 | deal | 141.0 | 0 | 48.0 | 40.6 | 40.6 | 7.1 | 12.04 | 0.0262 | 0 |
| 5797 | Duels II | Rival Plata | buyer | 98 | 52 | 73 | 5 | deal | 73.0 | 0 | 25.0 | 17.9 | 17.9 | 8.2 | 14.15 | 0.1078 | 0 |
| 5800 | Duels II | Rival Azul | seller | 77 | 128 | 88 | 7 | deal | 88.0 | 5 | 11.0 | 18.7 | 18.7 | 6.6 | 11.8 | 0.0843 | 0 |
| 5801 | Duels II | Rival Noche | buyer | 86 | 50 | 82 | 9 | deal | 79.0 | 0 | 7.0 | 3.6 | 3.6 | 7.9 | 11.01 | 0.1305 | 0 |
| 5808 | Duels II | Rival Luna | buyer | 195 | 110 | 136 | 6 | deal | 158.0 | 0 | 37.0 | 24.4 | 24.4 | 8.3 | 11.07 | 0.107 | 0 |
| 5809 | Duels II | Rival Rojo | seller | 130 | 186 | 178 | 4 | deal | 167.0 | 0 | 37.0 | 28.8 | 28.8 | 9.4 | 13.28 | 0.0858 | 0 |
| 5812 | Duels II | Rival Rojo | seller | 73 | 125 | 92 | 7 | deal | 84.0 | 10 | 11.0 | 22.2 | 22.2 | 8.2 | 10.64 | 0.1283 | 0 |
| 5813 | Duels II | Rival Oro | buyer | 97 | 55 | 95 | 10 | no_deal |  |  |  | 0.0 |  | 9.1 | 13.07 | 0.2223 | 0 |
| 5816 | Duels II | Rival Luna | seller | 72 | 115 | 74 | 5 | no_deal |  |  |  | 0.0 |  | 0.6 | 5.16 | 0.0041 | 0 |
| 5817 | Duels II | Rival Sol | buyer | 110 | 70 | 104 | 8 | no_deal |  |  |  | 0.0 |  | 0.7 | 5.34 | 0.0034 | 0 |
| 5822 | Duels II | Rival Rojo | seller | 72 | 118 | 111 | 3 | deal | 111.0 | 0 | 39.0 | 33.0 | 33.0 | 8.6 | 11.11 | 0.0663 | 0 |
| 5823 | Duels II | Rival Sol | buyer | 61 | 30 | 57 | 6 | deal | 57.0 | 0 | 4.0 | 2.9 | 2.9 | 8.3 | 9.9 | 0.106 | 0 |
| 5826 | Duels II | Rival Sol | seller | 72 | 145 | 90 | 4 | deal | 90.0 | 10 | 18.0 | 40.0 | 40.0 | 11.1 | 13.53 | 0.0697 | 0 |
| 5827 | Duels II | Rival Plata | buyer | 109 | 48 | 48 | 2 | deal | 60.0 | 10 | 49.0 | 25.2 | 25.2 | 9.6 | 11.77 | 0.0753 | 0 |
| 5860 | Duels II | Rival Azul | seller | 114 | 155 | 169 | 4 | deal | 161.0 | 0 | 47.0 | 36.6 | 36.6 | 7.0 | 10.48 | 0.0595 | 0 |
| 5861 | Duels II | Rival Azul | buyer | 130 | 78 | 88 | 5 | deal | 95.0 | 0 | 35.0 | 25.1 | 25.1 | 7.9 | 10.22 | 0.0814 | 0 |
| 5892 | Duels II | Rival Oro | buyer | 97 | 62 | 93 | 7 | deal | 89.0 | 0 | 8.0 | 5.7 | 5.7 | 7.7 | 11.51 | 0.1085 | 0 |
| 5893 | Duels II | Rival Luna | seller | 65 | 140 | 92 | 6 | deal | 92.0 | 0 | 27.0 | 19.3 | 19.3 | 9.2 | 13.44 | 0.1156 | 0 |
| 5898 | Duels II | Rival Noche | seller | 76 | 120 | 79 | 7 | deal | 86.0 | 10 | 10.0 | 23.2 | 23.2 | 0.8 | 5.41 | 0.0039 | 0 |
| 5899 | Duels II | Rival Plata | buyer | 98 | 62 | 92 | 7 | no_deal |  |  |  | 0.0 |  | 0.6 | 5.15 | 0.0042 | 0 |
| 5946 | Duels II | Rival Rojo | seller | 124 | 175 | 153 | 4 | deal | 153.0 | 10 | 29.0 | 37.5 | 37.5 | 9.5 | 12.03 | 0.0672 | 0 |
| 5947 | Duels II | Rival Luna | buyer | 94 | 55 | 89 | 8 | deal | 84.0 | 0 | 10.0 | 7.8 | 7.8 | 2.9 | 9.3 | 0.0346 | 0 |
| 5964 | Duels II | Rival Rojo | seller | 87 | 135 | 139 | 5 | deal | 129.0 | 0 | 42.0 | 30.1 | 30.1 | 8.2 | 12.88 | 0.0841 | 0 |
| 5965 | Duels II | Rival Plata | buyer | 115 | 70 | 70 | 2 | deal | 76.0 | 0 | 39.0 | 35.9 | 35.9 | 5.9 | 8.51 | 0.0378 | 0 |
| 5968 | Duels II | Rival Azul | seller | 78 | 108 | 88 | 7 | deal | 111.0 | 0 | 33.0 | 23.6 | 23.6 | 8.1 | 12.65 | 0.104 | 0 |
| 5969 | Duels II | Rival Plata | buyer | 68 | 40 | 37 | 4 | deal | 45.0 | 2 | 23.0 | 13.9 | 13.9 | 7.3 | 9.58 | 0.0851 | 0 |
| 6006 | Duels II | Rival Verde | seller | 73 | 115 | 73 | 5 | no_deal |  |  |  | 0.0 |  | 0.6 | 5.69 | 0.0057 | 0 |
| 6007 | Duels II | Rival Plata | buyer | 48 | 30 | 45 | 8 | no_deal |  |  |  | 0.0 |  | 0.6 | 5.01 | 0.0039 | 0 |
| 6022 | Duels II | Rival Azul | buyer | 125 | 78 | 86 | 3 | deal | 86.0 | 10 | 39.0 | 19.3 | 19.2 | 9.6 | 12.05 | 0.1033 | 0 |
| 6023 | Duels II | Rival Azul | seller | 68 | 115 | 105 | 5 | deal | 96.0 | 0 | 28.0 | 20.1 | 20.1 | 8.3 | 9.69 | 0.094 | 0 |
| 6036 | Duels II | Rival Sol | seller | 141 | 225 | 192 | 4 | deal | 199.0 | 10 | 58.0 | 51.1 | 51.2 | 6.7 | 7.54 | 0.0406 | 0 |
| 6037 | Duels II | Rival Noche | buyer | 145 | 95 | 128 | 5 | deal | 120.0 | 0 | 25.0 | 16.5 | 16.5 | 7.4 | 8.5 | 0.0584 | 0 |
| 6040 | Duels II | Rival Azul | seller | 87 | 145 | 134 | 3 | deal | 134.0 | 0 | 47.0 | 36.6 | 36.6 | 7.6 | 8.95 | 0.0321 | 0 |
| 6041 | Duels II | Rival Sol | buyer | 99 | 45 | 39 | 4 | deal | 48.0 | 2 | 51.0 | 33.4 | 33.4 | 7.5 | 11.16 | 0.083 | 0 |
| 6048 | Duels II | Rival Rojo | seller | 83 | 138 | 131 | 3 | deal | 125.0 | 0 | 42.0 | 35.5 | 35.5 | 6.6 | 9.51 | 0.0353 | 0 |
| 6049 | Duels II | Rival Oro | buyer | 148 | 82 | 88 | 3 | deal | 96.0 | 10 | 52.0 | 22.6 | 22.6 | 8.9 | 10.73 | 0.0524 | 0 |
| 6084 | Duels II | Rival Plata | buyer | 126 | 78 | 98 | 5 | deal | 101.0 | 0 | 25.0 | 19.5 | 19.5 | 6.9 | 9.15 | 0.0534 | 0 |
| 6085 | Duels II | Rival Rojo | seller | 136 | 210 | 150 | 6 | deal | 158.0 | 0 | 22.0 | 17.1 | 17.1 | 10.1 | 21.91 | 0.1068 | 0 |
| 6094 | Duels II | Rival Luna | seller | 34 | 58 | 65 | 4 | deal | 65.0 | 0 | 31.0 | 24.1 | 24.1 | 11.8 | 20.04 | 0.2849 | 0 |
| 6095 | Duels II | Rival Verde | buyer | 46 | 20 | 43 | 8 | deal | 43.0 | 0 | 3.0 | 1.7 | 1.7 | 8.7 | 13.63 | 0.1308 | 1 |
| 6100 | Duels II | Rival Rojo | buyer | 122 | 85 | 108 | 5 | deal | 108.0 | 0 | 14.0 | 11.8 | 11.8 | 7.5 | 11.91 | 0.053 | 0 |
| 6101 | Duels II | Rival Plata | seller | 56 | 84 | 75 | 5 | deal | 75.0 | 0 | 19.0 | 17.5 | 17.5 | 7.3 | 14.22 | 0.0652 | 0 |
| 6140 | Duels II | Rival Rojo | seller | 80 | 135 | 140 | 5 | deal | 125.0 | 0 | 45.0 | 41.4 | 41.4 | 7.6 | 11.92 | 0.063 | 0 |
| 6141 | Duels II | Rival Noche | buyer | 147 | 95 | 104 | 3 | deal | 104.0 | 0 | 43.0 | 39.6 | 39.6 | 8.7 | 10.3 | 0.0441 | 0 |
| 6170 | Duels II | Rival Azul | seller | 70 | 125 | 92 | 8 | deal | 82.0 | 0 | 12.0 | 6.7 | 6.7 | 9.9 | 13.34 | 0.2448 | 0 |
| 6171 | Duels II | Rival Sol | buyer | 74 | 32 | 68 | 7 | deal | 63.0 | 0 | 11.0 | 6.1 | 6.1 | 8.8 | 14.87 | 0.1544 | 0 |
| 6176 | Duels II | Rival Verde | seller | 92 | 155 | 104 | 10 | deal | 96.0 | 0 | 4.0 | 1.9 | 1.9 | 9.0 | 14.68 | 0.1876 | 0 |
| 6177 | Duels II | Rival Plata | buyer | 76 | 45 | 74 | 7 | no_deal |  |  |  | 0.0 |  | 7.5 | 10.72 | 0.1168 | 0 |
| 6182 | Duels II | Rival Oro | seller | 71 | 105 | 78 | 8 | no_deal |  |  |  | 0.0 |  | 5.3 | 11.29 | 0.0749 | 0 |
| 6183 | Duels II | Rival Plata | buyer | 82 | 55 | 77 | 8 | deal | 77.0 | 0 | 5.0 | 5.0 | 5.0 | 0.7 | 5.47 | 0.0037 | 0 |
| 6184 | Duels II | Rival Plata | seller | 60 | 112 | 68 | 9 | deal | 66.0 | 0 | 6.0 | 3.1 | 3.1 | 8.9 | 13.48 | 0.1928 | 0 |
| 6185 | Duels II | Rival Sol | buyer | 54 | 34 | 45 | 5 | deal | 47.0 | 0 | 7.0 | 5.0 | 5.0 | 8.7 | 14.25 | 0.1266 | 0 |
| 6190 | Duels II | Rival Oro | buyer | 143 | 95 | 122 | 7 | deal | 88.0 | 10 | 55.0 | 3.6 | 3.6 | 9.2 | 15.67 | 0.1196 | 0 |
| 6191 | Duels II | Rival Luna | seller | 83 | 158 | 151 | 3 | deal | 139.0 | 0 | 56.0 | 47.4 | 47.4 | 10.5 | 13.56 | 0.0922 | 0 |
| 83 | Practice duels | Rival Sol | seller | 86 | 125 | 125 | 1 | no_deal |  |  |  | 0.0 |  | 6.5 | 6.49 | 0.004 | 0 |
| 84 | Practice duels | Rival Azul | buyer | 65 | 40 | 40 | 1 | no_deal |  |  |  | 0.0 |  | 5.7 | 5.69 | 0.0039 | 0 |

136 duels · 105 with a price · mean surplus 25.1 · mean decision 6.4 s · model spend $8.332
