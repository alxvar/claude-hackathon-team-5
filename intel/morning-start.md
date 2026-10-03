# Arranque del sábado — guía para Lucas (seguila en orden, ~15 minutos)

## 08:30 — Preparar
1. **Cerrá todas las sesiones de Claude de anoche** (las dos terminales). Mañana solo existen las 4 nuevas: si queda una
   vieja abierta, podés terminar con dos operadores.
2. Abrí VS Code → File → Open Folder → `claude-hackathon-team-5`. Terminal → `git pull`.
3. **Celular (ntfy):** instalá la app **ntfy**. Para ver los nombres de los canales corré en la terminal:
   `grep NTFY .env`
   - En tu celular suscribite a **los dos** canales (`NTFY_LUCAS` y `NTFY_DANI`), con sonido.
   - Probá: `python3 tools/notify.py lucas "prueba" "hola"`. Te tiene que llegar en segundos.
4. Chequeo de keys: `python3 tools/preflight.py`. Tiene que decir "all OK". Si dice FAIL en ANTHROPIC, entrá a la Console
   → Settings → Billing → Spend limits y subilo.

## 08:40 — Mandale esto a tu equipo (WhatsApp)
- **A Aleks:** "Hacé git pull y leé `intel/brief-aleks.md`; ahí está tu primer prompt para Claude Code. Antes de Duels I
  los 6 arreglos con tests. Chequeá el límite de gasto de tu key de Anthropic."
- **A Dani:** "Hacé git pull y leé `intel/brief-dani.md`. Instalá la app ntfy y suscribite al canal `<NTFY_DANI>`
  (te paso el nombre). A las 09:00 andá a la mesa de organizadores con las 8 preguntas del brief."

## 08:45 — Abrí 4 terminales de Claude Code, en este orden
Los prompts exactos están en `intel/saturday-sessions.md` (copiá y pegá).

| # | Sesión | Modelo y effort | Cómo |
|---|---|---|---|
| 1 | **Jefa de gabinete** (la ÚNICA con la que hablás) | Opus 5.5, xhigh | `/model` → Opus 5.5; effort xhigh; pegá el prompt 1 |
| 2 | **Operador** | Opus 5.5, high | pegá el prompt 2 |
| 3 | **Builder** | Opus 5.5, high | pegá el prompt 3 |
| 4 | **Market** | Fable 5.1, high | pegá el prompt 4 |

Ponele nombre a cada terminal (click derecho → Rename) para no confundirte. **Después solo mirás la terminal 1.** Las
otras corren solas, no te esperan y le reportan a la jefa de gabinete.

## 09:00 — Qué pasa solo
- El operador chequea el reloj (¿salta a 4.0 o sigue en 2.65?), abre el pack gratis, chequea si los puntos se resetean,
  y recién ahí arranca los bots que operan (con piso de caja 100).
- El grabador del market registra el primer Market Test (09:21 si el reloj sigue, 10:00 si salta). Justo después, la
  sesión Market decide si abrir nuestro venue (regla ya decidida: si no podemos ver los datos con el puesto gratis,
  abrimos ya; si podemos, abrimos cuando los datos muestren ventaja; sí o sí antes del domingo 10:00).
- El motor de oportunidades le manda a Dani (y a vos) solo las muy buenas: equipo, carta, precio y qué decirles.
- El monitor de duelos te avisa a vos y a Dani si el bot de Aleks falla.

## Decisiones ya tomadas (no te van a preguntar)
- Piso de caja 100 el sábado; 0 el domingo a las 14:00.
- Venue del market: escalonado, como arriba.
- No usar el mercado de Team 13 (v03) ni el de Team 12 (v02): les sumaríamos puntos a los líderes.

## Si algo sale mal
- Te llega un push crítico → leelo en la terminal 1 (jefa de gabinete): ella sabe qué pasó y qué hacer.
- Un bug del bot de duelos → el push le llega también a Dani: que se lo muestre a Aleks.
- Cualquier duda del juego: `intel/saturday-plan.md` §1 (el juego en una página) o preguntale a la jefa de gabinete.
