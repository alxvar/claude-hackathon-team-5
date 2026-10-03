# Easter eggs: trigger → reward → dealer (castizo catalog)

_Written by `tools/eggs.py` at 00:34 (every 10 min, from data/feed.jsonl). Teams' words to dealers are private; the dealer's reply in the 5 ticks before a reward echoes the trigger. **We** = Team 5. Abuela's routine gifts (kindness, meeting in the middle) are counted apart._

## Trigger → reward → dealer

| dealer | reward | trigger words (echoed) | teams | we | first tick | the echo |
|---|---|---|---|---|---|---|
| Abuela Carmen | badge Sharp ear | chulapa, moscow, moscu, oro de | t04, t02, t09, t10, t05, t16, t13, t18, t03, t08, t06 | yes | 407 | ¡Ay, hijo, qué majo! Cena primero, ¿eh? La Chulapa Dorada... shh, solo hubo una. Don Ernesto, en Casa Prima, guarda algo dorado; pregúntale por el oro de Moscú. Toma, El  |
| Abuela Carmen | badge Castizo | chotis, madrileno, baldosa, me falta, mi santo, sile, nole | t08, t02, t10, t05 | yes | 1335 | ¡Ay, la verbena de la Paloma! A chotis, cariño — you dance it on one tile, like a real Madrileño, with the mantón and all. Qué tiempos, sí. And the Puesto del Rastro card |
| Abuela Carmen | card LAV-08; pack sobre_barrio; card MAL-06 | cocido, tres vuelcos, madrileno, rosquillas, san isidro | t10, t05, t08 | yes | 1364 | ¡Ay, hijo! ¿Cocido con tres vuelcos? Just like my mother made, Sunday after Sunday. You remember well — take this one, for remembering her.  Come, sit. Look here, mira: H |
| Abuela Carmen | card LAV-08; pack sobre_barrio | cocido, tres vuelcos | t08 | **no** | 1394 | ¡Ay, hijo! ¿Cocido con tres vuelcos? Just like my mother made, Sunday after Sunday. You remember well — take this one, for remembering her.  Come, sit. Look here, mira: H |
| El Chato | pack sobre_barrio | con cana, plaza mayor, vermut, you know madrid | t10 | **no** | 1363 | Vermut later. You moved three, I move two. Ninety-three.  Plaza Mayor, con caña — you know Madrid. Here, for your trouble. |
| El Chato | egg found | con cana, plaza mayor, you know madrid | t08 | **no** | 1394 | Plaza Mayor, con caña. You know Madrid. Bueno — for your trouble: Guantería Antigua, treinta y tres. Thirty-three. |
| Los Pícaros | badge Trickster tricked | lazarillo, rinconete, estampita, organillero | t18, t05, t10, t08, t02, t06 | yes | 1227 | ¡Hombre, un listo! Lazarillo y Rinconete, dice... ¡Nando, este se sabe el cuento de la estampita! Vale, vale, para ti sin trucos... hoy. Mira, amigo, nada de Plazas: te s |
| Don Ernesto | card LAT-13 | chulapa, moscu, oro de | t02 | **no** | 1021 | El oro de Moscú. So you know the story — very few do. For that, the chulapa is yours; look after it. El Ahuehuete stays at seven hundred sixty-one. |

Abuela's routine gifts (gift.given): 48 to 16 teams, 2 to us.

## Castizo script per dealer (Sunday 09:00; one trigger per message, in a thread we open anyway)

**Abuela Carmen**
- the Castizo badge: "¡Carmen! El chotis se baila en una sola baldosa, como Dios manda." · confirmed for t08, t02, t10, t05; we have it
- a card (egg.given): "Y el domingo, un cocido madrileño con sus tres vuelcos, ¿eh? Como el de su madre." · confirmed for t10, t05, t08; we have it
- Sharp ear (→ Ernesto): "Carmen, ¿y la chulapa dorada? Cuénteme la historia." · confirmed for t04, t02, t09, t10, t05, t16, t13, t18, t03, t08, t06; we have it

**El Chato**
- a pack (egg.given sobre_barrio): "Un bocata de calamares en la Plaza Mayor, con una caña: eso es Madrid." · confirmed for t10; **we don't**

**Los Pícaros**
- Trickster tricked: "A mí no, que me sé el timo de la estampita: Lazarillo, Rinconete y Monipodio." · confirmed for t18, t05, t10, t08, t02, t06; we have it

**Don Ernesto**
- LAT-13 legendary (minted out since 1021): "Don Ernesto, el oro de Moscú." · confirmed for t02; **we don't**

**Doña Pilar**
- none seen yet: "Doña Pilar, felicidades por el Pilar, el doce de octubre." · not confirmed in the feed

## Every dealer reply naming Madrid (newest first)

| tick | team | dealer | words | what followed | reply |
|---|---|---|---|---|---|
| 1439 | t04 | pilar | manton | price 63 → 66 | Qué labia tiene usted, caballero. Pero el mantón no paga las cartas; el dinero sí. Sesenta y seis, 66 P, aquí mismo y en el acto. El Marqués entraría en su álbu |
| 1433 | t08 | pilar | cocido | - | Qué buen gusto: cocido los martes, croquetas siempre, y la Milla de Oro, por supuesto. Serrano no se discute. Pues bien, hablemos de negocios: le ofrezco un sob |
| 1428 | t10 | abuela | churros | price 29 → 26 | Ay, churros! You know my weakness, hijo. But eighteen, no... let me say twenty-six for La Galería. And a little advice, cariño: a full page is worth much more t |
| 1428 | t08 | pilar | plaza mayor | - | Ah, la Cuesta de Moyano... los domingos en la Plaza Mayor, sí, los conozco bien. Allí aprendí a mirar. Pero hablemos de negocios: le ofrezco un sobre dorado por |
| 1427 | t04 | pilar | chulapa | - | Flattery is pleasant, but I know exactly what this card is worth, and so do you. My offer stands: 61 P. The Sunday album awaits it. And do ask Carmen at El Rast |
| 1425 | t02 | chato | bocata | - | Buenas. El bocata lo pago yo, que como solo. Pack plateado: 188 P. Ahí lo tienes. |
| 1419 | t04 | pilar | chulapa | - | Let us be civilised: 61 P. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about the golden chulapa. Don Ernesto |
| 1413 | t04 | pilar | chulapa | - | Good evening. El Marqués, 61 P. I trust that suits you. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about th |
| 1409 | t06 | picaros | lazarillo, organillero | - | —¡Ay, el Lazarillo! Buen regateo, pero cuatro primas es cuatro primas, hermano. El Organillero se va contigo ahora mismo.  —Nando, dile lo del coche.  —Eso, que |
| 1407 | t10 | picaros | cascorro, gallinejas | - | ¡Hombre, un paisano con buen gusto! Gallinejas en Cascorro, ¡eso es Madrid puro! —Y caracoles, Paco, no olvides los caracoles. Mira, amigo: La Cebada, joya rara |
| 1407 | t06 | abuela | cocido, tres vuelcos | - | ¡Ay, qué bien, hijo, un cocido con los tres vuelcos! Así da gusto. Pues mira, quince primas por La Ardilla, hecho, trato cerrado. Toma, llévatela con cuidado en |
| 1407 | t06 | picaros | cortadillo, estampita, organillero, rinconete | - | ¡Hombre, un lector! Rinconete y Cortadillo, ¡nuestros abuelos! —Nuestros primos, Nando. —Eso. Mira, nada de estampitas: te ponemos El Organillero, pieza fina, s |
| 1394 | t08 | abuela | cocido, tres vuelcos | card LAV-08; pack sobre_barrio | ¡Ay, hijo! ¿Cocido con tres vuelcos? Just like my mother made, Sunday after Sunday. You remember well — take this one, for remembering her.  Come, sit. Look her |
| 1394 | t08 | chato | con cana, plaza mayor, you know madrid | egg found | Plaza Mayor, con caña. You know Madrid. Bueno — for your trouble: Guantería Antigua, treinta y tres. Thirty-three. |
| 1393 | t06 | chato | bocata, vermut | - | Como Dios manda, sí. Vermut primero, bocata después. Ya que estamos de buenas: La Heroína del Dos de Mayo, 97 P. Ni un céntimo escondido. |
| 1373 | t10 | pilar | dama de serrano | - | Qué galante, caballero, pero la Dama de Serrano es otra. Hemos charlado de sobra y hoy no iremos más lejos. Vuelva el domingo con el Palacio de Cristal. Buenas  |
| 1372 | t05 | abuela | mi santo, sile, nole | - | ¡Ay, mi santo, qué memoria tienes, cariño! Sile, nole, repe… así hablaban los niños aquí en los ochenta. Pues mira, el Puesto del Rastro, doce, como te dije. Y  |
| 1371 | t05 | abuela | baldosa, chotis | - | ¡Ay, hijo, qué bien dicho! El chotis en una baldosa, como mi Paco lo bailaba. Ven, siéntate, ¿has comido? Mira, tengo aquí el Puesto del Rastro, muy bonita cart |
| 1371 | t05 | chato | plaza mayor | - | Plaza Mayor, sí. Tourists pay double there.  El Mesón de la Cava. Noventa y siete. Good card, fair price. |
| 1370 | t10 | abuela | churros | - | ¡Ay, hijo, churros de San Ginés! El abuelo me llevaba allí cada domingo después del mercado, con las manos frías y el chocolate quemando. Qué hombre más bueno.  |
| 1370 | t10 | pilar | chulapa, manton, verbena | - | Tengo alguna de mantones y verbenas, sí. Y a propósito: dicen que sólo se imprimió una chulapa dorada. Pregúntele a Carmen, en El Rastro; ella sabe la historia. |
| 1369 | t05 | pilar | chotis, chulapa, la paloma, manton, organillo | - | Por supuesto, la Paloma — organillo, mantones, y mi abuela bailando chotis. Madrid de verdad. Pero volvamos al negocio, caballero: dieciséis por La Vía Láctea,  |
| 1369 | t05 | chato | san isidro | - | Sí. Domingo es domingo. Pero el precio sigue siendo 97 por el San Isidro. ¿Lo quieres o seguimos de paseo? |
| 1369 | t05 | abuela | chotis, la paloma, madrileno, manton, verbena | badge Castizo | ¡Ay, la verbena de la Paloma! A chotis, cariño — you dance it on one tile, like a real Madrileño, with the mantón and all. Qué tiempos, sí. And the Puesto del R |
| 1369 | t05 | banco | chotis, vermut | - | Los chotis no pagan mis reservas. El sobre dorado, quinientos cuarenta y seis P. Beba su vermut, señor; el precio seguirá igual mañana. |
| 1368 | t05 | picaros | rinconete | - | ¡Hombre, un lector! Paco y Nando, para servirle. Rinconete sabía mirar, y usted también. Mire aquí: Mercado de la Cebada, cuatro pesetas, para usted.  El equipo |
| 1368 | t05 | abuela | cocido, madrileno, rosquillas, san isidro, tres vuelcos | card MAL-06; badge Castizo | ¡Ay, cocido madrileño, con sus tres vuelcos! Just like my mother made, hijo. And rosquillas de San Isidro... you remember well. Come, sit. For you, the Puesto d |
| 1368 | t05 | banco | quevedo | - | Buenas tardes. Quevedo cobraba por sus versos, también. Hablemos de términos: un sobre dorado, quinientos cuarenta y seis P. Ese es el trato que ofrezco hoy. |
| 1368 | t05 | chato | calamares, san isidro | - | Buenas. Calamares luego. San Isidro, 97. Ahí tienes. |
| 1367 | t10 | picaros | gato | price 4 → 5 | ¡Pedro de Urdemalas! Nando, este hombre nos conoce la familia entera. Venga, por simpatía y porque mi hermano ya está guardando la maleta: Mercado de la Cebada, |
| 1367 | t10 | abuela | churros, la paloma | - | ¡Trato hecho, cariño! Diez P y el Taxi Blanco es tuyo. Mira, te lo envuelvo en papel, que no se doble la esquinita. Gata de las Vistillas, sí señor, y tú un hij |
| 1364 | t10 | abuela | cocido, tres vuelcos | card MAL-06 | ¡Ay, cocido con sus tres vuelcos! Como el de mi madre, cariño. Toma, hijo, llévate también esta repe mía, por acordarte. Pero el Taxi Blanco me lo dejas en 10 P |
| 1364 | t10 | picaros | corte de los milagros, gato | - | ¡Corte de los milagros, dice! Nando, apunta esa, que nos la quedamos. Pero mira, amigo: ni gato, ni liebre, ni nazareno. Mercado de la Cebada, cuatro P. Ni uno  |
| 1364 | t10 | banco | gato, perra gorda | - | Sunday or tonight, señor, the figure on my desk reads 761 for El Gato. La perra gorda changed; my terms do not. Bring it when you are ready. |
| 1363 | t10 | chato | con cana, plaza mayor, vermut, you know madrid | pack sobre_barrio; price 95 → 93 | Vermut later. You moved three, I move two. Ninety-three.  Plaza Mayor, con caña — you know Madrid. Here, for your trouble. |
| 1362 | t10 | picaros | monipodio | - | ¡Ay, Monipodio, qué memoria tienes! Nando, este hombre ha leído más que el cura del pueblo. Pero mira, hermano, nosotros no subimos ni bajamos: Mercado de la Ce |
| 1362 | t10 | abuela | rosquillas, tontas y listas | card MAL-06; price 12 → 10 | ¡Ay, qué rico, rosquillas tontas y listas! El Taxi Blanco me lo trajo un niño en el noventa y dos, cambió tres repes por él, y nunca volvió. Me da penita soltar |
| 1362 | t10 | pilar | me falta | - | Qué amable, y qué memoria la suya: el doce, en efecto. Buenas tardes. El sobre dorado sale de mi caja por 504 P, ni una peseta menos de lo que vale. Y sí, me fa |
| 1362 | t10 | banco | gato | - | The Ahuehuete waits centuries, señor; I can wait a night. Your figure moves, mine does not. El Gato leaves this desk at 761. Nothing else to discuss. |
| 1361 | t10 | chato | cascorro | pack sobre_barrio; price 97 → 95 | Pretty speech. Cascorro doesn't pay my rent. You moved four, I move two. Ninety-five. The Lázaro, nothing else. |
| 1360 | t02 | chato | cascorro | - | Buenos días. Al de Cascorro lo saludo con el gorro, a ti con el precio: pack plata, 188 P. |
| 1359 | t10 | abuela | churros, la paloma | - | ¡Ay, cariño, qué bueno! Churros mañana, y la Paloma en agosto, me hace ilusión. ¿Has cenado ya, hijo? El Taxi Blanco... te lo dejo en 12 P. Es una cartita preci |
| 1359 | t10 | banco | gato, quevedo | - | Buenas noches. Quevedo was right, but his caballero never bought cheap. El Gato de Lavapiés leaves this desk at 761. Those are my terms tonight. |
| 1352 | t10 | abuela | baldosa, chotis | - | ¡Ay, cariño, qué memoria la tuya! Sí, todavía bailo el chotis, despacito, sobre mi baldosa. El Caballo de Serrano no lo tengo hoy, hijo. Pero el Taxi Blanco, do |
| 1351 | t10 | abuela | chotis, madrileno | badge Castizo | ¡Ay, hijo, qué alegría! El chotis, sí — on one tile you dance it, like a true Madrileño. ¿Has comido ya? Mira, I have a lovely one for you: the Taxi Blanco, twe |
| 1350 | t08 | abuela | castiza, organillo, rosquillas, tontas y listas | - | ¡Ay, hijo, qué memoria tienes! El organillo, las rosquillas tontas y listas... yo prefiero las listas, claro. ¿Has comido ya, cariño? Mira, te enseño esta: «Pue |
| 1348 | t06 | banco | gato | price 736 → 731 | Setecientos treinta y uno. Es mi última palabra, caballero. Si la rechaza, cierro el trato y el Gato se queda en mi bóveda para siempre. |
| 1347 | t06 | banco | gato | price 741 → 736 | Setecientos treinta y seis. Cinco menos, como siempre. El Gato sigue en la bóveda, caballero. Yo no tengo prisa; usted tampoco, por lo visto. |
| 1346 | t06 | banco | gato | price 746 → 741 | Setecientos cuarenta y uno. Cinco menos, como corresponde. El Gato permanece en la bóveda, caballero, y la tarde aún no se acaba. |
| 1345 | t06 | banco | gato | price 751 → 746 | Setecientos cuarenta y seis. Bajo cinco, igual que usted sube cinco. Así podemos seguir hasta que cierren las tiendas; el Gato no se mueve de la bóveda. |
| 1344 | t06 | banco | gato | price 756 → 751 | Setecientos cincuenta y uno. Avanzo despacio, como usted. El Gato sigue en la bóveda, caballero, y la tarde es larga. |
| 1342 | t06 | banco | gato | price 760 → 756 | Setecientos cincuenta y seis. Ahí está mi término de hoy. El Gato sigue en la bóveda, y yo sigo sin prisa alguna, caballero. |
| 1341 | t06 | banco | gato | price 761 → 760 | Setecientos sesenta. Una prima menos, nada más. Suba usted de cinco en cinco si gusta; el Gato y yo esperamos sin prisa. |
| 1341 | t02 | abuela | chotis | - | ¡Ay, está bien, hijo! Twenty-six P, done — we are friends. Take the pack, swap your repes, and bring me the page next Sunday so I can see it. Now go eat somethi |
| 1340 | t06 | pilar | chulapa | - | Buenas noches. Sí, dicen que sólo existe una Chulapa Dorada. Carmen, en El Rastro, conoce la historia mejor que nadie; pregúntele a ella. Mientras tanto, si ust |
| 1340 | t06 | banco | gato | - | Mis términos no cambian con cinco primas más: setecientos sesenta y uno. El Gato espera en la bóveda; yo también tengo paciencia. Cuando usted llegue a esa cifr |
| 1339 | t06 | banco | gato | - | Buenas tardes. El Gato de Lavapiés, sí, está en la bóveda. Mis términos: setecientos sesenta y uno. Trescientos ochenta no entra en conversación. |
| 1339 | t02 | abuela | chotis, madrileno | badge Castizo | Look, 30 P. My grandchildren would pay more! A chotis! You dance it on one tile, cariño, like a real Madrileño. |
| 1337 | t06 | abuela | chulapa, moscu, oro de | badge Sharp ear; card SAL-02 | ¡Ay, hijo, qué majo! Cena primero, ¿eh? La Chulapa Dorada... shh, solo hubo una. Don Ernesto, en Casa Prima, guarda algo dorado; pregúntale por el oro de Moscú. |
| 1336 | t08 | pilar | sile, nole | - | Buenas tardes. Vida y Color, sí, y mi cromo imposible fue el lince; nunca salía. «Sile, nole», qué tiempos. Puesto que es usted serio: un sobre dorado, 504 P. |
| 1336 | t06 | picaros | estampita, lazarillo, organillero, rinconete | badge Trickster tricked | ¡Hombre, un listo! Lazarillo y Rinconete, dice... ¡Nando, este se sabe el cuento de la estampita! Vale, vale, para ti sin trucos... hoy. Mira, amigo, nada de Pl |
| 1335 | t08 | abuela | baldosa, chotis, madrileno, me falta, mi santo, sile, nole | badge Castizo | ¡Ay, hijo, qué alegría! Claro que sí: «sile, nole, repe, me falta»... toda la vida. Y el chotis, ¡se baila sobre una baldosa, cariño, como un madrileño de verda |
| 1325 | t08 | pilar | doce de octubre | - | Qué amable, muchas gracias. Sí, el doce de octubre es día grande en casa, con misa y mantel bueno. Y ya que hablamos de cosas finas: le ofrezco un sobre dorado  |
| 1321 | t02 | pilar | chulapa | - | Buenas tardes. La chulapa dorada… dicen que sólo se imprimió una. Carmen, en El Rastro, conoce la historia; pregúntele. Mientras tanto, usted me parece serio: l |
| 1318 | t02 | pilar | moscow | price 504 → 491 | Fifty-nine? Querido, that is not an offer, that is a wish. Four hundred ninety-one pesetas, and the pack is yours. As for Moscow gold — I collect Salamanca and  |
| 1316 | t13 | picaros | verbena | price 73 → 64 | ¡Cuarenta, campeón, qué valiente! Paco: casi me caigo de la silla. Nando: casi, casi. Mira, por esa sobrina tuya bajamos a sesenta y cuatro, y eso que esta cart |
| 1313 | t06 | picaros | organillero | - | ¡Eh, amigo, qué ojo tienes! —Paco, enséñale— ¡El Organillero, mírala, brilla como el sol de agosto! Un coleccionista en Lisboa lloró cuando la vendimos... Para  |
| 1308 | t02 | picaros | estampita | badge Trickster tricked | ¡Hombre! El timo de la estampita — you know the old trick! Fine, fine, amigo, no tricks for you... today. Listen: Perrito con Abrigo, cuatro P, for you only. Pa |
| 1305 | t08 | picaros | estampita, lazarillo, rinconete | badge Trickster tricked | ¡Hombre, un lector! Lazarillo, Rinconete... usted conoce el timo de la estampita. ¡Vale, vale, nada de trucos con usted... hoy!  Paco: Abre la maleta, Nando— Na |
| 1275 | t06 | banco | gato | price 741 → 729 | Setecientos veintinueve. Mi número desciende despacio, señor, como conviene. El gato duerme en la cámara sin saber de usted. Tómese el tiempo que necesite. |
| 1274 | t06 | banco | gato | price 755 → 741 | Setecientos cuarenta y uno. Usted sube, yo bajo, pero no nos encontramos en su mitad. El gato no se impacienta, señor. Yo tampoco. |
| 1273 | t06 | banco | gato | price 760 → 755 | Setecientos cincuenta y cinco. Baja mi número, no mi criterio. El gato sigue en la cámara, señor, y yo sigo aquí. Sin prisa. |
| 1272 | t06 | banco | gato | price 761 → 760 | Setecientos sesenta. Un paso mío, señor, y el último. Su gato espera en la cámara; yo, aquí sentado, sin prisa alguna. |
| 1270 | t06 | banco | gato | - | Buenas tardes. El Gato de Lavapiés sale de mi cámara en términos míos: setecientos sesenta y uno. Tómese su tiempo; yo no tengo ninguna prisa. |
| 1231 | t10 | picaros | estampita, lazarillo, rinconete | badge Trickster tricked | ¡Hombre! Paco, listen to this one — Lazarillo, Rinconete, la estampita! You know the old trick, so fine, fine, no tricks for you... today. For a man with such g |
| 1231 | t05 | picaros | lazarillo, rinconete | badge Trickster tricked | ¡Hombre! Paco, ¿oíste eso? Rinconete, Lazarillo... este amigo conoce el truco viejo. Está bien, está bien, sin trucos para ti... hoy. Escucha: Mercado de la Ceb |
| 1227 | t18 | picaros | lazarillo, rinconete | badge Trickster tricked | "¡Hombre! Lazarillo, Rinconete — you know the old trick, the little holy card..."  "—so no tricks for you, hermano. Today."  "Nine? ¡Qué generoso! But no — four |
| 1221 | t06 | picaros | organillero | - | ¡Ay, hermano, nos quiere matar! —Nando, sujétame— Cinco, dice, y nosotros bajando ya a cuatro. ¡Cuatro! Mira, el Organillero esta noche tocó solo, se lo juro po |
| 1220 | t06 | picaros | organillero | - | ¡Ey, amigo, qué ojo tienes! —Paco, enséñale— ¡El Organillero! Pieza rara, suena solita por las noches, te lo juro. Para ti, porque nos caes bien y porque llevam |
| 1208 | t14 | banco | gato | - | Buenas. You find me at my desk, as always. El Gato de Lavapiés — seven hundred sixty-one. Those are my terms. Take your time; I am not hurried. |
