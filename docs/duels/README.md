# Duel records

_Written by `uv run python -m agents.duelist review`. One `duel-<id>.json` per duel holds everything; `feed.jsonl` holds the public feed's duel events (they may name the team behind an alias); `scores.jsonl` our duel points over time._

| duel | session | rival | role | limit | our_first | our_last | moves | status | price | surplus | points | avg_s | max_s | cost_usd | fallbacks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 103 | Duels I | Rival Oro | buyer | 129 | 85 | 88 | 2 | no_deal |  |  |  | 4.7 | 4.82 | 0.0099 | 0 |
| 104 | Duels I | Rival Azul | seller | 69 | 98 | 95 | 2 | no_deal |  |  |  | 5.3 | 5.67 | 0.0098 | 0 |
| 105 | Duels I | Rival Azul | seller | 74 | 118 | 113 | 4 | no_deal |  |  |  | 5.0 | 7.68 | 0.0182 | 1 |
| 106 | Duels I | Rival Oro | buyer | 96 | 62 | 66 | 4 | no_deal |  |  |  | 4.4 | 6.81 | 0.0175 | 1 |
| 113 | Duels I | Rival Verde | seller | 51 | 85 | 81 | 4 | no_deal |  |  |  | 4.2 | 5.94 | 0.0194 | 1 |
| 114 | Duels I | Rival Luna | buyer | 93 | 55 | 58 | 2 | deal | 58.0 | 35.0 |  | 5.3 | 5.67 | 0.0105 | 0 |
| 115 | Duels I | Rival Noche | seller | 69 | 98 | 98 | 1 | no_deal |  |  |  | 4.8 | 4.81 | 0.0038 | 0 |
| 116 | Duels I | Rival Oro | buyer | 140 | 85 | 85 | 1 | live |  |  |  | 5.2 | 5.18 | 0.0037 | 0 |
| 119 | Duels I | Rival Plata | buyer | 180 | 110 | 110 | 1 | no_deal |  |  |  | 5.4 | 5.44 | 0.0042 | 0 |
| 120 | Duels I | Rival Rojo | seller | 53 | 85 | 85 | 1 | no_deal |  |  |  | 6.9 | 6.87 | 0.0041 | 0 |
| 121 | Duels I | Rival Sol | seller | 74 | 118 | 96 | 5 | deal | 100.0 | 26.0 |  | 6.0 | 7.11 | 0.036 | 0 |
| 122 | Duels I | Rival Noche | buyer | 130 | 80 | 105 | 5 | deal | 105.0 | 25.0 |  | 6.2 | 9.3 | 0.0353 | 0 |
| 163 | Duels I | Rival Rojo | seller | 69 | 98 | 91 | 5 | deal | 91.0 | 22.0 |  | 4.4 | 5.98 | 0.0259 | 1 |
| 164 | Duels I | Rival Luna | buyer | 79 | 52 | 52 | 1 | deal | 52.0 | 27.0 |  | 11.1 | 11.05 | 0.0043 | 0 |
| 175 | Duels I | Rival Verde | seller | 80 | 130 | 118 | 6 | deal | 118.0 | 38.0 |  | 6.4 | 8.8 | 0.0462 | 0 |
| 176 | Duels I | Rival Plata | buyer | 107 | 72 | 80 | 5 | deal | 80.0 | 27.0 |  | 6.4 | 7.25 | 0.0336 | 0 |
| 181 | Duels I | Rival Verde | buyer | 85 | 50 | 67 | 6 | no_deal |  |  |  | 4.6 | 6.43 | 0.0361 | 1 |
| 182 | Duels I | Rival Oro | seller | 59 | 95 | 95 | 1 | live |  |  |  | 5.1 | 5.09 | 0.004 | 0 |
| 199 | Duels I | Rival Oro | buyer | 150 | 90 | 96 | 3 | deal | 97.0 | 53.0 |  | 5.5 | 6.81 | 0.0158 | 0 |
| 200 | Duels I | Rival Noche | seller | 68 | 104 | 104 | 2 | deal | 102.0 | 34.0 |  | 5.6 | 5.92 | 0.0107 | 0 |
| 227 | Duels I | Rival Luna | seller | 130 | 185 | 156 | 4 | live |  |  |  | 8.7 | 14.24 | 0.0255 | 0 |
| 228 | Duels I | Rival Verde | buyer | 138 | 105 | 113 | 3 | live |  |  |  | 6.7 | 7.24 | 0.0179 | 0 |
| 257 | Duels I | Rival Oro | seller | 78 | 115 | 103 | 4 | deal | 103.0 | 25.0 |  | 6.0 | 7.38 | 0.0323 | 0 |
| 258 | Duels I | Rival Noche | buyer | 64 | 38 | 38 | 1 | deal | 38.0 | 26.0 |  | 4.8 | 4.79 | 0.0037 | 0 |
| 269 | Duels I | Rival Rojo | seller | 81 | 112 | 106 | 2 | live |  |  |  | 8.1 | 10.13 | 0.0106 | 0 |
| 270 | Duels I | Rival Verde | buyer | 102 | 72 | 72 | 1 | live |  |  |  | 7.8 | 7.8 | 0.0067 | 0 |
| 31 | Duels I | Rival Sol | seller | 111 | 165 | 165 | 1 | no_deal |  |  |  | 7.1 | 7.13 | 0.0043 | 0 |
| 32 | Duels I | Rival Verde | buyer | 160 | 95 | 95 | 1 | no_deal |  |  |  | 7.6 | 7.57 | 0.0041 | 0 |
| 83 | Duels I | Rival Sol | seller | 86 | 125 | 125 | 1 | no_deal |  |  |  | 6.5 | 6.49 | 0.004 | 0 |
| 84 | Duels I | Rival Azul | buyer | 65 | 40 | 40 | 1 | no_deal |  |  |  | 5.7 | 5.69 | 0.0039 | 0 |

30 duels · 11 with a price · mean surplus 30.7 · mean decision 6.0 s · model spend $0.462
