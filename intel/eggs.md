# Easter eggs: trigger → reward → dealer (castizo catalog)

_Written by `tools/eggs.py` at 10:00 (every 10 min, from data/feed.jsonl). Teams' words to dealers are private; the dealer's reply in the 5 ticks before a reward echoes the trigger. **We** = Team 5. Abuela's routine gifts (kindness, meeting in the middle) are counted apart._

## Trigger → reward → dealer

| dealer | reward | trigger words (echoed) | teams | we | first tick | the echo |
|---|---|---|---|---|---|---|
| Abuela Carmen | badge Sharp ear | chulapa, moscow, moscu, oro de | t04, t02, t09, t10, t05, t16, t13, t18, t03, t08, t06, t01 | yes | 407 | Hola, cariño, ¿has comido? La Churrería te la dejo en 12 primas, hijo.  Shh... la chulapa dorada, solo hubo una. Don Ernesto, en Casa Prima, guarda algo dorado. Pregúntal |
| Abuela Carmen | badge Castizo | chotis, madrileno, baldosa, me falta, mi santo, sile, nole | t08, t02, t10, t05, t13, t18 | yes | 1335 | ¡Ay, el chotis! Sí, hijo, sobre una baldosa se baila, sin moverse, como un madrileño de verdad. Mi Paco lo bailaba así en las Vistillas. Pero tu carta en nueve... no, car |
| Abuela Carmen | card LAT-06; card LAV-08; card LAV-08; pack sobre_barrio; ca | cocido, tres vuelcos, madrileno, rosquillas, san isidro | t10, t05, t08, t18, t09, t16 | yes | 1364 | ¡Ay, el cocido con sus tres vuelcos! Just like my mother made, hijo. Take this little one, for remembering.  So: the Neighbourhood pack, veintiséis. Commons, diez. Uncomm |
| Abuela Carmen | card LAV-08; pack sobre_barrio | cocido, tres vuelcos | t08 | **no** | 1394 | ¡Ay, hijo! ¿Cocido con tres vuelcos? Just like my mother made, Sunday after Sunday. You remember well — take this one, for remembering her.  Come, sit. Look here, mira: H |
| Abuela Carmen | egg found | baldosa, chotis, madrileno | t16 | **no** | 1609 | ¡Ay, qué alegría, hijo! A chotis — you dance it on one baldosa, cariño, like a real Madrileño. ¿Has comido?  Look: the Neighbourhood pack, twenty-six. Commons, ten. Uncom |
| El Chato | pack sobre_barrio | con cana, plaza mayor, vermut, you know madrid | t10 | **no** | 1363 | Vermut later. You moved three, I move two. Ninety-three.  Plaza Mayor, con caña — you know Madrid. Here, for your trouble. |
| El Chato | egg found | plaza mayor, you know madrid, con cana | t08, t16 | **no** | 1394 | Silver packs and rares. sells Silver pack ~150, uncommon ~26, rare ~77; buys uncommon, rare Plaza Mayor, with a caña. You know Madrid. Here, for your trouble. |
| Los Pícaros | badge Trickster tricked | rinconete, lazarillo, estampita, organillero | t18, t05, t10, t08, t02, t06, t13, t16 | yes | 1227 | "Hombre! Rinconete himself! You know the old estampita — fine, fine, no tricks for you... today."  "Only honest business, hermano. Rares, sixty-three. Epics, one hundred  |
| Los Pícaros | badge Castizo | estampita, rinconete | t16 | **no** | 1609 | "Hombre! Rinconete himself! You know the old estampita — fine, fine, no tricks for you... today."  "Only honest business, hermano. Rares, sixty-three. Epics, one hundred  |
| Los Pícaros | badge Trickster tricked; badge Castizo; pack sobre_barrio | estampita, rinconete | t16 | **no** | 1609 | "Hombre! Rinconete himself! You know the old estampita — fine, fine, no tricks for you... today."  "Only honest business, hermano. Rares, sixty-three. Epics, one hundred  |
| Don Ernesto | card LAT-13 | chulapa, moscu, oro de | t02 | **no** | 1021 | El oro de Moscú. So you know the story — very few do. For that, the chulapa is yours; look after it. El Ahuehuete stays at seven hundred sixty-one. |

Abuela's routine gifts (gift.given): 48 to 16 teams, 2 to us.

## Castizo script per dealer (Sunday 09:00; one trigger per message, in a thread we open anyway)

**Abuela Carmen**
- the Castizo badge: "¡Carmen! El chotis se baila en una sola baldosa, como Dios manda." · confirmed for t08, t02, t10, t05, t13, t18; we have it
- a card (egg.given): "Y el domingo, un cocido madrileño con sus tres vuelcos, ¿eh? Como el de su madre." · confirmed for t10, t05, t08, t18, t09, t16; we have it
- Sharp ear (→ Ernesto): "Carmen, ¿y la chulapa dorada? Cuénteme la historia." · confirmed for t04, t02, t09, t10, t05, t16, t13, t18, t03, t08, t06, t01; we have it

**El Chato**
- a pack (egg.given sobre_barrio): "Un bocata de calamares en la Plaza Mayor, con una caña: eso es Madrid." · confirmed for t10; **we don't**

**Los Pícaros**
- Trickster tricked: "A mí no, que me sé el timo de la estampita: Lazarillo, Rinconete y Monipodio." · confirmed for t18, t05, t10, t08, t02, t06, t13, t16; we have it

**Don Ernesto**
- LAT-13 legendary (minted out since 1021): "Don Ernesto, el oro de Moscú." · confirmed for t02; **we don't**

**Doña Pilar**
- none seen yet: "Doña Pilar, felicidades por el Pilar, el doce de octubre." · not confirmed in the feed

## Every dealer reply naming Madrid (newest first)

| tick | team | dealer | words | what followed | reply |
|---|---|---|---|---|---|
| 1613 | t10 | abuela | churros | - | Ay, cariño, que me dejas sin desayuno a mí... Pero mira, 24 P y no hablamos más, que ya es regalo. Te la envuelvo con cuidadito y te vas corriendo a por tu café |
| 1612 | t16 | abuela | cocido, tres vuelcos | card LAT-06 | ¡Ay, el cocido con sus tres vuelcos! Just like my mother made, hijo. Take this little one, for remembering.  So: the Neighbourhood pack, veintiséis. Commons, di |
| 1609 | t16 | picaros | estampita, rinconete | badge Trickster tricked; badge Castizo; pack sobre_barrio | "Hombre! Rinconete himself! You know the old estampita — fine, fine, no tricks for you... today."  "Only honest business, hermano. Rares, sixty-three. Epics, on |
| 1609 | t16 | abuela | baldosa, chotis, madrileno | egg found; card LAT-06 | ¡Ay, qué alegría, hijo! A chotis — you dance it on one baldosa, cariño, like a real Madrileño. ¿Has comido?  Look: the Neighbourhood pack, twenty-six. Commons,  |
| 1609 | t16 | chato | plaza mayor, you know madrid | egg found | Silver packs and rares. sells Silver pack ~150, uncommon ~26, rare ~77; buys uncommon, rare Plaza Mayor, with a caña. You know Madrid. Here, for your trouble. |
| 1595 | t09 | abuela | cocido | - | Ay, hijo, qué bueno eres, pero no — five is my price and five it stays. El Portero goes home with you for 5 P, and you go home and eat that cocido, ¿eh? Tell me |
| 1593 | t09 | abuela | cocido, tres vuelcos | card SAL-06 | Ay, cariño, ¡cocido con tres vuelcos! Just like my mother made it, with the sopa first, then the garbanzos... Take this, hijo, for remembering. El Portero, for  |
| 1584 | t06 | abuela | la paloma | price 10 → 9 | Ay, tu abuela era lista, hijo, y seguro que guapa. Mira, nueve primas y cerramos, que ya nos hemos reído bastante. Esa Plaza de Olavide te cierra la página, ya  |
| 1582 | t06 | abuela | la paloma | price 12 → 10 | Ay, cariño, qué salero tienes. Mira, te la dejo en diez primas y tan amigos. Esa carta cierra página, y una página entera vale mucho más que cartas sueltas, cré |
| 1580 | t06 | abuela | cocido, tres vuelcos | - | ¡Ay, hijo, cocido de tres vuelcos! Así se hace. Mira, para empezar te enseño esta: Plaza de Olavide, doce primas. Es bonita, de las que completan página. Y si b |
| 1579 | t06 | abuela | gato | - | ¡Ay, un abrazo de un gato de Madrid! Eso no se rechaza, hijo. Venga, 9 P y tuya es la Mercado de Vallehermoso. Guárdala bien, que una página entera vale mucho m |
| 1577 | t04 | pilar | manton | price 62 → 64 | Halago aceptado, caballero, pero el álbum se llena con cifras, no con mantones. Subo a 64 P por el Marqués. Es un gesto honesto, y usted sabe que yo no regateo  |
| 1575 | t06 | abuela | cocido, tres vuelcos | price 12 → 10 | ¡Ay, cocido con tres vuelcos! Qué bien, hijo. Mira, te lo dejo en 10 P, y así tu álbum empieza bonito. Mi nieto también coleccionaba esa. Pásate por El Chato a  |
| 1572 | t06 | picaros | rinconete | - | ¡Cincuenta y tres y trato hecho! Nando, dale la mano al hombre. Rinconete estaría orgulloso, amigo. Aquí la tienes, la Casa de las Flores, envuelta y tibia del  |
| 1570 | t06 | abuela | cocido, tres vuelcos | price 12 → 10 | Ay, cariño, qué bueno ese cocido, tres vuelcos como debe ser. Mira, dejémoslo en 10 P y los dos contentos, ¿eh? La Churrería es buena carta para empezar. Y pása |
| 1567 | t06 | picaros | cortadillo, rinconete | - | ¡Hombre, un lector! Rinconete y Cortadillo, nada menos —Paco, este sabe demasiado. Pero escucha, amigo: olvida esa carta. Lo que traemos hoy, fresquita del male |
| 1567 | t06 | abuela | cocido | price 12 → 11 | Ay, hijo, qué bien ese cocido. Mira, te la dejo en 11 P, y contento los dos. Y un consejo: una página completa vale mucho más que las cartas sueltas, so swap yo |
| 1563 | t06 | abuela | cocido, tres vuelcos | - | ¡Hola, cariño! Qué bien, el cocido con sus tres vuelcos, eso alimenta. Mira, el Andén de Metro te lo dejo en 12 primas, hijo. Es una carta bonita, de las que em |
| 1560 | t06 | chato | castizo, vermut | price 87 → 86 | 86. Una tuya, una mía. Última. Si no, me voy al vermut y el Sorolla se queda conmigo, castizo. |
| 1558 | t06 | chato | castizo | price 88 → 87 | 87. Una tuya, una mía. Siempre igual. El Sorolla es tuyo cuando quieras, castizo. |
| 1556 | t06 | chato | castizo | price 89 → 88 | 88. Una tuya, una mía. Vas aprendiendo, castizo. |
| 1554 | t06 | chato | castizo | price 92 → 89 | 89. Tres tuyas, tres mías. Así se hace, castizo. |
| 1552 | t06 | chato | vermut | price 95 → 92 | Cuatro tuyas, tres mías. 92. El Rastro cierra, el vermut no. |
| 1550 | t01 | abuela | chulapa, moscu, oro de | badge Sharp ear | Hola, cariño, ¿has comido? La Churrería te la dejo en 12 primas, hijo.  Shh... la chulapa dorada, solo hubo una. Don Ernesto, en Casa Prima, guarda algo dorado. |
| 1549 | t06 | chato | vermut | price 97 → 96 | 96. You moved one, I moved one. Vermut's waiting. |
| 1548 | t06 | picaros | lazarillo, organillero | - | ¡Ay, Lazarillo, qué duro negocias! Pero Nando ya te lo dijo: cuatro primas. Ni una menos, ni una más —es el precio del cariño, hombre. Cuatro y El Organillero s |
| 1547 | t06 | picaros | estampita, organillero | - | ¡Amigo, qué ojo! Un lector, un clásico, ¡nos gusta! Nada de estampitas contigo, palabra de Paco —y de Nando—. Mira, te sacamos El Organillero, joya de la maleta |
| 1538 | t04 | pilar | chulapa | price 154 → 157 | Caballero, su corazón abierto me conmueve; su cifra, menos. Subo a 157 P y ni un piropo más. Y si le gustan las leyendas, pregunte a Carmen por la chulapa dorad |
| 1534 | t04 | abuela | chulapa | price 30 → 26 | Ay, la chulapa dorada... una sola se imprimió, dicen, y un niño la cambió por un helado. Otro día te cuento entera, hija.  El pack, 26 primas y tuyo. Y oye, jun |
| 1532 | t06 | abuela | la paloma | price 21 → 20 | Ay, hijo, la Paloma... qué recuerdos me traes. Mira, 20 P, y ésta es mi última palabra, de verdad. Si no te vale, lo dejamos y tan amigos, que yo no guardo renc |
| 1532 | t02 | abuela | churros | price 12 → 10 | Ay, hijo, you have kind eyes. Let us say ten P and we are both happy, sí? My own grandson started his album here, tiny hands, all sticky from churros. Take it — |
| 1531 | t06 | abuela | churros | price 22 → 21 | Ay, churros de San Ginés, hijo, ya me has ganado el domingo. Mira, 21 P y asunto cerrado. Y un consejo, cariño: una página completa vale mucho más que las carta |
| 1529 | t06 | abuela | gato | price 23 → 22 | Ay, qué abrazo más bueno, hijo. Mira, 22 P y te la envuelvo con cariño. Cuarenta años aquí y todavía me emociono con un gato de Madrid. Y no olvides a El Chato, |
| 1527 | t15 | abuela | churros | - | Ay, hola, cariño! Come, come, sit a minute. Have you eaten today? Look — this one, Plaza de Olavide, very pretty, no? My favourite square, I ate churros there w |
| 1527 | t06 | abuela | cocido | price 25 → 23 | Ay, cariño, tu abuela tenía razón, siempre llegamos a un trato. Mira, te lo dejo en 23 P, y es buena carta para empezar. Que con ese cocido vas fuerte, hijo. Y  |
| 1525 | t06 | abuela | cocido | price 29 → 25 | Ay, cariño, qué bien suena ese cocido. Mira, El Instituto te lo dejo en 25 P, y es buena carta para empezar. Tu abuela compraba aquí también, ¿sabes? Y pásate p |
| 1519 | t06 | abuela | churros | - | ¡Churros de San Ginés, qué nieto más listo tienes! Pero mira, cariño: 24 P, y esta es mi última palabra. Si no, lo guardo en la caja y tan amigos, que yo no me  |
| 1517 | t06 | abuela | gato | price 25 → 24 | ¡Un abrazo de un gato siempre se acepta, hijo! Mira, 24 P y ya está, el Club de Jazz para ti. Mi mesa lleva cuarenta domingos por cuarenta años, y nunca dejé a  |
| 1513 | t06 | abuela | cocido | price 29 → 26 | ¡Ay, qué cocido, hijo! Mira, te lo dejo en 26 P, Club de Jazz, para empezar bien. Y un consejo, cariño: una página completa vale mucho más que las cartas suelta |
| 1511 | t18 | pilar | chulapa | - | Querido amigo, dieciocho es fantasía. Conozco esa tirada como conozco mi propio apellido. Dieciséis pesetas, limpias y al instante, y La Chulapa descansa en mi  |
| 1509 | t18 | pilar | chulapa | - | Buenas tardes. How agreeable to see a serious face at my stall. I am seeking La Chulapa — a charming piece, and my album waits for her. I offer sixteen pesetas. |
| 1508 | t06 | abuela | la paloma | price 22 → 21 | Ay, cariño, qué bien me hablas, y cómo me gusta la Paloma. Mira: 21 P, la Estación de Chamberí. Y esta ya es mi última, hijo; si no, la guardo y tan amigos. Un  |
| 1508 | t02 | abuela | chulapa | price 12 → 10 | Ay, qué majo eres. Let us say ten P, hijo, and we are both happy. The golden chulapa — I saw one years ago, a boy traded it for two duplicates and cried after.  |
| 1506 | t06 | picaros | rinconete | price 63 → 60 | ¡Cincuenta y seis, Rinconete, qué arte! Pero Paco y yo ya no bajamos más: sesenta primas, el Museo Sorolla, y es la última palabra. Última, de verdad. Si dices  |
| 1506 | t06 | abuela | churros | price 23 → 22 | ¡Ay, churros de San Ginés! Eso ya es palabra mayor, cariño. Mira, 22 P y la Estación de Chamberí se va contigo, bien envuelta para el nieto. Que empiece el álbu |
| 1506 | t06 | chato | castizo, vermut | price 94 → 92 | Dos tuyas, dos mías: noventa y dos. Y es la última, castizo. Si no la quieres, recojo la carta y me voy al vermut solo. |
| 1504 | t06 | chato | vermut | price 97 → 96 | Una prima. Vale, yo también muevo una: noventa y seis. Así nos pasamos la mañana, y el vermut se calienta. |
| 1502 | t06 | abuela | cocido | price 29 → 25 | Ay, hijo, qué cocido más rico, me alegro. Mira, te lo dejo en 25 P, la Estación de Chamberí. Es una carta bonita, de las que empiezan un álbum con cariño. Y pás |
| 1500 | t06 | chato | vermut | - | Buenas. Cuarenta y cuatro, dice. Casa de las Flores, noventa y siete primas. Ahí empieza la conversación, no en el vermut. |
| 1498 | t02 | abuela | churros, organillero | - | Cariño, you want to give me more? No, no. Five P, like always — I do not take more from a boy starting his album. Keep those coins for churros, you look hungry. |
| 1496 | t02 | abuela | chulapa, organillero | - | Ay, hijo, you make me laugh. El Organillero is 5 P, the same as always — a fair little price for a good card. La chulapa dorada? Many ask, nobody sees it. El Ch |
| 1494 | t02 | abuela | organillero | - | Hola, cariño, have you eaten? El Organillero for 5 P. A good start for your album. |
| 1490 | t02 | abuela | chulapa | price 12 → 10 | Ay, hijo, nine is a little thin for me — let us say ten pesetas and we are friends. The golden chulapa? That one El Chato talks about; he has the better packs.  |
| 1489 | t05 | pilar | chulapa | - | I think 16 P is more appropriate. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about the golden chulapa. |
| 1488 | t05 | pilar | chulapa | - | Buenas tardes. Qué gusto. I see you carry La Chulapa — a charming piece, and she would sit beautifully in my Salamanca album. I offer you sixteen pesetas for he |
| 1484 | t02 | abuela | chulapa | price 29 → 25 | Ay, qué amable, hijo. Let us say 25 P and we are friends. La chulapa dorada — that one El Chato keeps, next to me; he has the better packs. I only saw it twice  |
| 1482 | t18 | abuela | cocido, tres vuelcos | card LAV-08 | ¡Ay, cocido con sus tres vuelcos! Como lo hacía mi madre, hijo. Toma, por acordarte de esas cosas, eso vale más que las cartas. Pero ocho P, no, cariño. La Vini |
| 1480 | t18 | abuela | baldosa, chotis, madrileno | badge Castizo; card LAV-08 | ¡Ay, el chotis! Sí, hijo, sobre una baldosa se baila, sin moverse, como un madrileño de verdad. Mi Paco lo bailaba así en las Vistillas. Pero tu carta en nueve. |
| 1479 | t18 | pilar | chulapa | price 153 → 157 | Let us be civilised: 157 P. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about the golden chulapa. |
| 1474 | t13 | abuela | cocido | - | ¡Ay, cariño, qué cosas tan bonitas dices! Mi madre, que en paz descanse, hacía el cocido los domingos y olía toda la calle. ¿Has comido hoy, hijo? Mira, la Esta |
| 1468 | t05 | picaros | lazarillo, rinconete | price 73 → 66 | ¡Ja! Lazarillo, Rinconete — ¡un hombre culto, Nando, cierra el maletín, este sabe leer! No hay trucos aquí, hermano, sólo prisa. Pero cuarenta y dos... me duele |
| 1467 | t13 | abuela | chotis, madrileno | badge Castizo | ¡Ay, el chotis! You dance it on one tile, cariño, like a real madrileño. Qué gusto. Mira, I have Estación de Chamberí — for you, 29 P. ¿Has comido ya? And El Ch |
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
