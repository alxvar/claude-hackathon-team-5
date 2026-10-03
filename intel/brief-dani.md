# Dani — brief del sábado (leelo primero)

## El juego en 30 segundos
100 puntos: Negociación 30 (duelos + dealers + trades entre equipos) · Market-making 30 · Jueces 40. El viernes vale 20%,
sábado 40%, domingo 40%, y todo es relativo: si otros suben y nosotros no, bajamos.
Cada carta vale distinto para cada equipo. **Una carta repetida nos vale casi nada a nosotros y muchísimo a un equipo al
que le falta para completar una página** (completar una página da un bonus grande). Ahí está tu trabajo.

## Tus 3 trabajos
1. **09:00, mesa de organizadores**: las 8 preguntas de abajo. Anotá las respuestas en `team/dani.md` apenas las tengas.
2. **Corredor de páginas en la sala** (desde ~10:00): te llegan alertas al celular. Vas, hablás con ese equipo, y listo.
3. **La historia para los jueces (40%)**: a las 09:30 averiguá el formato del jurado; screenshot de la pantalla grande al
   cierre de cada día; con Lucas, borrador del pitch durante Duels I (11:30-13:05).

## Las alertas: cómo funcionan (vos no tenés que correr nada)
- **Setup, 1 minuto**: instalá la app **ntfy** (iPhone o Android) → "Subscribe to topic" → escribí el nombre del canal
  que te pasa Lucas a las 08:45. Activá las notificaciones con sonido. Listo.
- El sistema de Lucas mira el mercado cada 30 segundos y **solo te avisa cuando es una muy buena oportunidad** (como mucho
  ~3 por hora): un equipo que está bastante abajo nuestro necesita una carta que a nosotros no nos sirve, o tiene una carta
  que nos cierra una página. **La oferta ya está publicada a nombre de ese equipo** antes de que te llegue la alerta.
- Cada alerta te dice: **a qué equipo ir, qué carta, a qué precio, qué decirles** (en español y en inglés) y **qué tienen
  que decirle a su agente** para aceptarla.

## Qué hacer cuando llega una alerta
1. Buscá al equipo (el número está en la alerta; la pantalla grande muestra los equipos).
2. Decí la frase de la alerta con tus palabras. Ejemplo: *"Les falta la LAV-02 para cerrar Lavapiés, ¿no? Se la dejamos
   publicada a su nombre a 40. La ven en El Rastro, la aceptan y cierran la página."*
3. **Si desconfían** (es normal, competimos): no tienen que confiar en nosotros. La oferta está publicada y la pueden revisar
   antes de aceptar; ellos ganan puntos con el trade. Si no saben cómo, que le digan a su agente la línea de la alerta, por
   ejemplo: *"Accept offer 1234 on El Rastro."*
4. Anotá en una línea en `team/dani.md`: hora · equipo · carta · aceptaron o no · qué dijeron. Eso nos enseña.

## Qué NO hacer
- **No inventes precios ni prometas nada** que no esté en la alerta. Si piden otro precio, anotalo y avisá a Lucas.
- **No digas qué cartas necesitamos nosotros** fuera de lo que dice la alerta (si saben que la necesitamos, suben el precio).
- **No vayas sin alerta** a ofrecer cosas: si lo hacemos cada 2 minutos, los otros equipos aprenden y nos copian.

## Alertas de duelos (para Aleks)
También te pueden llegar alertas del monitor de duelos (ej. "el duelist no aceptó una oferta dentro del límite"). Si Lucas
está ocupado, mostrásela a Aleks.

## Las 8 preguntas para la mesa (09:00)
1. ¿El reloj del sábado sigue en la hora 2.65 o salta a 4.0? ¿Corre el Market Test de la hora 3.0 y en qué round?
2. ¿`neg_points`, el ladder y los puntos de duelo se reinician en cada round?
3. ¿Hay un tope de puntos por trade? Nuestra compra que completó una página dio exactamente +50 cuando esperábamos ~89.
4. Ladder: ¿qué define el "rango de precio" de un dealer (apertura, precio de lista o el límite secreto)? Nuestros 3 deals
   con El Chato no movieron `ladder_points`.
5. Market: ¿cómo se reparten los puntos entre el Market Test y el valor creado en nuestro venue? ¿Cómo escalan entre el
   puesto gratis (mitad) y el promedio del top 3? ¿Si cerramos un venue vuelve el puesto gratis? ¿El bench cobra fee?
6. ¿Aceptar en un duelo cuenta contra el límite de 1 accept por tick del equipo? ¿Los duelos cuentan en las 6 conversaciones?
7. Jueces: ¿formato, hora, duración, criterios? ¿Miran el repo?
8. Niveles 3-5: ¿cuándo y cómo se desbloquean? ¿El "precio de bienvenida" de Abuela se reinicia cada día?

## Quién hace qué
- **Lucas**: decide; sus sesiones de Claude operan el mercado, los dealers y el market-making.
- **Aleks**: el bot de duelos.
- **Vos**: la mesa, la sala (con alertas) y la historia.

## Primer prompt para tu Claude Code
> Sos el Claude Code de Dani en el Team 5. Leé intel/brief-dani.md y PLAN.md "RIGHT NOW" (Dani). Ayudame con las preguntas
> de la mesa y a anotar respuestas en team/dani.md; corregí en dashboard/server.py la regla "never the top 3" por "top 4 y
> páginas solo a equipos 10+ puntos abajo". No toques el juego.
