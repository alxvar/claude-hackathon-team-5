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
| 83 | Practice duels | Rival Sol | seller | 86 | 125 | 125 | 1 | no_deal |  |  |  | 0.0 |  | 6.5 | 6.49 | 0.004 | 0 |
| 84 | Practice duels | Rival Azul | buyer | 65 | 40 | 40 | 1 | no_deal |  |  |  | 0.0 |  | 5.7 | 5.69 | 0.0039 | 0 |

68 duels · 49 with a price · mean surplus 22.1 · mean decision 5.3 s · model spend $2.385
