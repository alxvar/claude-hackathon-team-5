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
| 257 | Practice duels | Rival Oro | seller | 78 | 115 | 103 | 4 | deal | 103.0 |  | 25.0 | 20.8 | 20.8 | 6.0 | 7.38 | 0.0323 | 0 |
| 258 | Practice duels | Rival Noche | buyer | 64 | 38 | 38 | 1 | deal | 38.0 |  | 26.0 | 26.0 | 26.0 | 4.8 | 4.79 | 0.0037 | 0 |
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

34 duels · 19 with a price · mean surplus 25.8 · mean decision 5.6 s · model spend $0.768
