# Easter eggs: trigger → reward → dealer (castizo catalog)

_Written by `tools/eggs.py` at 11:10 (every 10 min, from data/feed.jsonl). Teams' words to dealers are private; the dealer's reply in the 5 ticks before a reward echoes the trigger. **We** = Team 5. Abuela's routine gifts (kindness, meeting in the middle) are counted apart._

## Trigger → reward → dealer

| dealer | reward | trigger words (echoed) | teams | we | first tick | the echo |
|---|---|---|---|---|---|---|
| Abuela Carmen | badge Sharp ear | chulapa, moscow, moscu, oro de | t04, t02, t09, t10, t05, t16, t13, t18, t03, t08, t06, t01 | yes | 407 | Hola, cariño, ¿has comido? La Churrería te la dejo en 12 primas, hijo.  Shh... la chulapa dorada, solo hubo una. Don Ernesto, en Casa Prima, guarda algo dorado. Pregúntal |
| Abuela Carmen | badge Castizo | chotis, madrileno, baldosa, me falta, mi santo, sile, nole | t08, t02, t10, t05, t13, t18 | yes | 1335 | ¡Ay, el chotis! Sí, hijo, sobre una baldosa se baila, sin moverse, como un madrileño de verdad. Mi Paco lo bailaba así en las Vistillas. Pero tu carta en nueve... no, car |
| Abuela Carmen | card LAT-06; card LAV-08; card LAV-08; pack sobre_barrio; ca | cocido, tres vuelcos, madrileno, rosquillas, san isidro | t10, t05, t08, t18, t09, t16, t02, t12 | yes | 1364 | Ay, cocido de tres vuelcos! Just like my mother made, hijo — the soup first, always. You remembered, that warms me. Take it, the Escaparate de Serrano, twelve P, and I pu |
| Abuela Carmen | card LAV-08; pack sobre_barrio | cocido, tres vuelcos | t08 | **no** | 1394 | ¡Ay, hijo! ¿Cocido con tres vuelcos? Just like my mother made, Sunday after Sunday. You remember well — take this one, for remembering her.  Come, sit. Look here, mira: H |
| Abuela Carmen | egg found | baldosa, chotis, madrileno | t16 | **no** | 1609 | ¡Ay, qué alegría, hijo! A chotis — you dance it on one baldosa, cariño, like a real Madrileño. ¿Has comido?  Look: the Neighbourhood pack, twenty-six. Commons, ten. Uncom |
| El Chato | pack sobre_barrio | plaza mayor, you know madrid, con cana, vermut, calamares | t10, t12, t02 | **no** | 1363 | Plaza Mayor, calamares, caña bien tirada. You know Madrid. Bueno — for your trouble, the silver pack. One eighty-eight. Same as always. |
| El Chato | egg found | plaza mayor, you know madrid, con cana | t08, t16 | **no** | 1394 | Silver packs and rares. sells Silver pack ~150, uncommon ~26, rare ~77; buys uncommon, rare Plaza Mayor, with a caña. You know Madrid. Here, for your trouble. |
| Los Pícaros | badge Trickster tricked | rinconete, estampita, lazarillo, organillero | t18, t05, t10, t08, t02, t06, t13, t16, t01 | yes | 1227 | ¡Hombre, qué alegría! ¿La estampita? Ja, ese cuento viejo... Vale, vale, con usted nada de trucos, amigo — hoy no. Paco, saca el Museo Sorolla. Setenta y tres P y es suyo |
| Los Pícaros | badge Castizo | estampita, rinconete | t16 | **no** | 1609 | "Hombre! Rinconete himself! You know the old estampita — fine, fine, no tricks for you... today."  "Only honest business, hermano. Rares, sixty-three. Epics, one hundred  |
| Los Pícaros | badge Trickster tricked; badge Castizo; pack sobre_barrio | estampita, rinconete | t16 | **no** | 1609 | "Hombre! Rinconete himself! You know the old estampita — fine, fine, no tricks for you... today."  "Only honest business, hermano. Rares, sixty-three. Epics, one hundred  |
| Don Ernesto | card LAT-13 | chulapa, moscu, oro de | t02 | **no** | 1021 | El oro de Moscú. So you know the story — very few do. For that, the chulapa is yours; look after it. El Ahuehuete stays at seven hundred sixty-one. |

Abuela's routine gifts (gift.given): 48 to 16 teams, 2 to us.

## Castizo script per dealer (Sunday 09:00; one trigger per message, in a thread we open anyway)

**Abuela Carmen**
- the Castizo badge: "¡Carmen! El chotis se baila en una sola baldosa, como Dios manda." · confirmed for t08, t02, t10, t05, t13, t18; we have it
- a card (egg.given): "Y el domingo, un cocido madrileño con sus tres vuelcos, ¿eh? Como el de su madre." · confirmed for t10, t05, t08, t18, t09, t16, t02, t12; we have it
- Sharp ear (→ Ernesto): "Carmen, ¿y la chulapa dorada? Cuénteme la historia." · confirmed for t04, t02, t09, t10, t05, t16, t13, t18, t03, t08, t06, t01; we have it

**El Chato**
- a pack (egg.given sobre_barrio): "Un bocata de calamares en la Plaza Mayor, con una caña: eso es Madrid." · confirmed for t10, t12, t02; **we don't**

**Los Pícaros**
- Trickster tricked: "A mí no, que me sé el timo de la estampita: Lazarillo, Rinconete y Monipodio." · confirmed for t18, t05, t10, t08, t02, t06, t13, t16, t01; we have it

**Don Ernesto**
- LAT-13 legendary (minted out since 1021): "Don Ernesto, el oro de Moscú." · confirmed for t02; **we don't**

**Doña Pilar**
- none seen yet: "Doña Pilar, felicidades por el Pilar, el doce de octubre." · not confirmed in the feed

## Every dealer reply naming Madrid (newest first)

| tick | team | dealer | words | what followed | reply |
|---|---|---|---|---|---|
| 1890 | t06 | picaros | estampita, lazarillo, rinconete | - | ¡Ay, qué culto nos sale el cliente! Lazarillo, Rinconete... Paco, este sabe leer. Nada de estampitas, hombre, aquí todo limpio. Mira esta joya: La Casa Encendid |
| 1885 | t14 | pilar | chulapa | price 61 → 62 | I think 62 P is more appropriate. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about the golden chulapa. |
| 1872 | t06 | chato | vermut | - | 13. Same as before. Vermut's waiting. |
| 1870 | t06 | chato | chulapa | - | La Chulapa. 13 P. Take it or leave it. |
| 1852 | t06 | picaros | estampita | - | ¡Ay, qué listo nos ha salido el cliente! Paco, mira, este ha leído libros. — ¡Y por eso le tratamos bien, hombre! Nada de estampitas, aquí todo a la luz: La Cas |
| 1847 | t10 | abuela | churros, me falta | - | Ay, hijo, churros no me faltan, que mi vecina me trae cada domingo. Pero esta carta vale cinco, y cinco te doy, de corazón. Llévatelos ahora y vuelve cuando qui |
| 1842 | t06 | pilar | chulapa | - | Nineteen primas, señor. I told you I would not move again, and I am a woman of my word. Twenty is your invention, not La Chulapa's worth. Accept nineteen, and s |
| 1841 | t06 | pilar | chulapa | price 18 → 19 | Nineteen primas, señor. That is where I stand, and I do not move again tonight. La Chulapa belongs in my album — but on my terms, not those of your lemon tart. |
| 1839 | t06 | pilar | chulapa | price 17 → 18 | Twenty-two, señor? No. Eighteen primas — and that is the last courtesy I extend this evening. La Chulapa will sit beautifully in my album, but not at any price  |
| 1837 | t06 | pilar | chulapa | price 16 → 17 | Lázaro Galdiano also knew when a thing was worth no more. Seventeen primas, señor — a courtesy, not a concession. La Chulapa deserves my album, but my album is  |
| 1836 | t06 | pilar | chulapa | - | The Embassy's lemon tart is charming, señor, but it does not alter the value of La Chulapa. My figure remains 16 primas. I know this card's print run precisely, |
| 1834 | t06 | pilar | chulapa | - | Good evening. La Chulapa, 16 P. I trust that suits you. |
| 1829 | t02 | pilar | chulapa | price 16 → 17 | Twenty-nine, still theatre, querido. I will stretch to seventeen pesetas — that is courtesy, not negotiation. And if you like stories, ask Carmen at El Rastro a |
| 1827 | t08 | picaros | plaza mayor | price 54 → 50 | ¡Cuarenta! Nando, sujétame que me caigo otra vez. Mira, guapo, tú regateas como un abuelo en la Plaza Mayor, y eso me gusta. Cincuenta P y la Heroína del Dos de |
| 1824 | t08 | picaros | plaza mayor | price 59 → 54 | ¡Ay, qué memoria tienes, amigo! Nando, este sí que lee. Pero escucha: ésta es la última Heroína que queda en todo Madrid, te lo juro por mi abuela. No hay otra, |
| 1818 | t12 | banco | chulapa | - | That is Spain's gold, señor, not mine. The golden chulapa has its own story, and you have not told it. La Reina de la Movida: seven hundred sixty-one. Unchanged |
| 1814 | t06 | picaros | organillero | - | ¡Cinco, dice! Paco, cierra… no, espera. Amigo, los de la caseta de al lado la quieren ya, vinieron dos veces. Pero tú nos caes mejor, qué le vamos a hacer. El O |
| 1814 | t02 | chato | calamares, plaza mayor, you know madrid | pack sobre_barrio | Plaza Mayor, calamares, caña bien tirada. You know Madrid. Bueno — for your trouble, the silver pack. One eighty-eight. Same as always. |
| 1812 | t06 | picaros | organillero | - | ¡Nando, cuéntaselo! Hace un momento otro equipo nos ofreció mucho más por El Organillero, y aquí seguimos contigo, que nos caes bien. Cuatro primas, amigo. Esa  |
| 1811 | t06 | picaros | organillero | - | ¡Siete! Paco, ¿has oído? Nando, dile. Amigo, El Organillero sale en cuatro primas y ni una menos, que ya es precio de hermano. Mira, un señor en Burgos pagó el  |
| 1809 | t12 | chato | plaza mayor, you know madrid | pack sobre_barrio | Plaza Mayor, bocadillo, caña bien tirada. You know Madrid. Bien, something extra in the bag for your trouble. Mercado de la Paz. Thirty-three. Still thirty-thre |
| 1808 | t06 | picaros | organillero | - | ¡Ah, un lector! Paco, este sabe de clásicos. Nando, saca El Organillero… ¡cuatro primas, amigo, y es tuyo! Y escucha: ayer mismo dejaron de imprimirla. Ya no sa |
| 1806 | t08 | picaros | monipodio | - | ¡Ja! Monipodio, la Celestina... primos lejanos, amigo, muy lejanos. Nosotros somos honrados —Paco, dile. Honradísimos. Y mira qué tenemos: el Museo Lázaro Galdi |
| 1805 | t08 | abuela | organillero, verbena | - | ¡Ay, hijo, qué hambre me das! Torrijas y horchata, como las verbenas de San Cayetano, con la parpusa bien puesta. ¿Pero tú has comido ya?  Mira, para ti: El Org |
| 1805 | t08 | chato | vermut | - | Casa Amadeo, sí. Los caracoles y el vermut. Hablas como de aquí. Fuente de la Alcachofa, 33 P. Esa es la oferta. |
| 1803 | t18 | pilar | chulapa | - | Querido, insisto: soy yo quien vende hoy. El Teatro Valle-Inclán, El Retiro puro, dieciséis pesetas. Un precio justo, y usted lo sabe. Por cierto, pregunte a Ca |
| 1794 | t12 | abuela | cocido, tres vuelcos | card SAL-06 | Ay, cocido de tres vuelcos! Just like my mother made, hijo — the soup first, always. You remembered, that warms me. Take it, the Escaparate de Serrano, twelve P |
| 1792 | t01 | abuela | chulapa | - | ¡Buenas, cariño! Qué alegría verte. ¿Has comido ya? Mira, la Estación de Chamberí te la dejo en 29 primas, y te completa la página bonita. La chulapa dorada...  |
| 1764 | t10 | chato | churros | - | Buenas. Bonita ruta. La Chamberí vale 33 P. Los churros te los pagas tú. |
| 1760 | t10 | pilar | barquillos | - | Qué evocación tan bonita, caballero: los barquillos junto al Palacio de Cristal, mi padre, las tardes de Embassy. Pero los álbumes no se pagan con meriendas. El |
| 1760 | t02 | abuela | chulapa | - | Ay, hijo, that old biscuit tin... Antonio kept his chulapa dorada in it for years, under the table with the cables. But today I have this Neighbourhood pack, 30 |
| 1745 | t04 | pilar | cocido | price 66 → 67 | Las brujas de Goya las conozco de memoria, señor mío, y el Parque Florido también. Pero el pincel no cambia la tirada: 67 P, mi palabra final de hoy. Acepto el  |
| 1738 | t05 | picaros | rinconete | price 64 → 59 | ¡Cuarenta! Nando, sujétame que me caigo. Amigo, that card survived cannons and we survived worse — but forty? Mira, por ti, porque me caes bien y tienes labia d |
| 1737 | t06 | picaros | organillero | - | ¡Ay, Nando, que nos sale listo el caballero! Mira, amigo: cinco ya las pide cualquiera, pero El Organillero vale lo que vale. Cuatro primas, ni una menos, y te  |
| 1735 | t06 | picaros | organillero | - | ¡Amigo, qué ojo! Un lector, un clásico — ¡nos gusta! Paco, saca la maleta... ¡rápido, que el tren no espera! Mira esto: El Organillero, una joya que suena bonit |
| 1734 | t02 | chato | plaza mayor | - | Plaza Mayor. Tourist prices, but the caña saves you. Bueno — silver pack, 188 P. |
| 1733 | t02 | abuela | cocido, tres vuelcos | card RET-07 | Ay, hijo, cocido con tres vuelcos! Just like my mother made, Sundays, the whole house smelling of it. You remember well. Come, sit, have you eaten? Here, look — |
| 1732 | t04 | pilar | cocido | price 63 → 66 | Lo que pagué por El Marqués lo recuerdo yo, señor mío, y no era eso. Nada de mercadillo: 66 P, dicho con toda seriedad. El Lázaro Galdiano junto a su vecino, y  |
| 1726 | t08 | pilar | barquillero | - | Qué memoria más dulce, señor. Yo guardo los pavos reales y el barquillero, sí — y aquellas noches de Florida Park. Un alma así merece algo bueno: le ofrezco un  |
| 1726 | t04 | pilar | cocido | price 61 → 63 | Qué amable, y acepto el cocido con gusto; la sobremesa sí la pago aparte. Pero el cromo tiene su precio justo, y lo conozco. Suba usted un poco de su lado: 63 P |
| 1712 | t13 | picaros | lazarillo | - | —¡Amigo, qué gusto! ¿Lazarillo de tu barrio? ¡Entonces eres de los nuestros!  —Mira, mira: Samosas de la Plaza, diez primas. Una ganga, ¿eh, Nando?  —¡Una ganga |
| 1687 | t07 | abuela | churros | - | ¡Ay, hija mía! You keep pushing money at me like my nephew at Christmas. Five P, El Tatuador is yours. Take the rest and buy churros, or a good packet from El C |
| 1686 | t07 | abuela | churros | - | Ay, cariño, you want to pay me more than I ask! No, no. Five P, that is the price, and not one more. Keep your coins for churros, hijo. And listen — El Chato, n |
| 1666 | t01 | picaros | oro de | price 73 → 67 | ¡Descabellado no, amigo, pero casi! Mire, Nando ya está cerrando la maleta: 67 y se la lleva. Oro de verdad, mi madre lloró cuando la vimos. Y dese prisa, que a |
| 1659 | t01 | picaros | estampita | badge Trickster tricked | ¡Hombre, qué alegría! ¿La estampita? Ja, ese cuento viejo... Vale, vale, con usted nada de trucos, amigo — hoy no. Paco, saca el Museo Sorolla. Setenta y tres P |
| 1650 | t10 | abuela | cocido | price 29 → 25 | Ay, el tren fantasma de Chamberí... mi madre juraba que lo oyó una noche, hijo. Mira, te dejo La Galería en 25 P, y en paz. Doña Pilar de Salamanca viene los sá |
| 1648 | t10 | abuela | churros, cocido | - | ¡Ay, hijo, churros de San Ginés! Qué bueno eres. Siéntate, que el cocido espera. Tres páginas enteras ya, qué orgullo me das. Este de Salamanca es La Galería, c |
| 1642 | t06 | picaros | organillero | - | —¡Cinco dice! —Paco, que este hombre aprendió del ciego. Mira, amigo, no podemos bailar más: El Organillero, cuatro primas, como dijimos. —Ni una menos, ni una  |
| 1640 | t06 | picaros | cortadillo, organillero, rinconete | - | ¡Hombre, un lector! Rinconete y Cortadillo, nada menos. —Nando, que éste sabe. —Entonces nada de humo, amigo. Mira: El Organillero, cuatro primas. Cuatro, y te  |
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
