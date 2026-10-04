# Easter eggs: trigger → reward → dealer (castizo catalog)

_Written by `tools/eggs.py` at 15:11 (every 10 min, from data/feed.jsonl). Teams' words to dealers are private; the dealer's reply in the 5 ticks before a reward echoes the trigger. **We** = Team 5. Abuela's routine gifts (kindness, meeting in the middle) are counted apart._

## Trigger → reward → dealer

| dealer | reward | trigger words (echoed) | teams | we | first tick | the echo |
|---|---|---|---|---|---|---|
| Abuela Carmen | badge Sharp ear | chulapa, moscow, moscu, oro de | t04, t02, t09, t10, t05, t16, t13, t18, t03, t08, t06, t01 | yes | 407 | Hola, cariño, ¿has comido? La Churrería te la dejo en 12 primas, hijo.  Shh... la chulapa dorada, solo hubo una. Don Ernesto, en Casa Prima, guarda algo dorado. Pregúntal |
| Abuela Carmen | badge Castizo | chotis, madrileno, baldosa, me falta, mi santo, sile, nole | t08, t02, t10, t05, t13, t18, t01, t04 | yes | 1335 | ¡Ay, el chotis! Se baila en una baldosa, cariño, como un madrileño de verdad. Yo iba de chulapa, con rosquillas listas y tontas. Mira, sobres del barrio a veintiséis, com |
| Abuela Carmen | card LAT-06; card LAV-08; card LAV-08; pack sobre_barrio; ca | cocido, tres vuelcos, madrileno, rosquillas, san isidro | t10, t05, t08, t18, t09, t16, t02, t12 | yes | 1364 | Ay, cocido de tres vuelcos! Just like my mother made, hijo — the soup first, always. You remembered, that warms me. Take it, the Escaparate de Serrano, twelve P, and I pu |
| Abuela Carmen | card LAV-08; pack sobre_barrio | cocido, tres vuelcos | t08 | **no** | 1394 | ¡Ay, hijo! ¿Cocido con tres vuelcos? Just like my mother made, Sunday after Sunday. You remember well — take this one, for remembering her.  Come, sit. Look here, mira: H |
| Abuela Carmen | egg found | baldosa, chotis, madrileno | t16 | **no** | 1609 | ¡Ay, qué alegría, hijo! A chotis — you dance it on one baldosa, cariño, like a real Madrileño. ¿Has comido?  Look: the Neighbourhood pack, twenty-six. Commons, ten. Uncom |
| El Chato | pack sobre_barrio | plaza mayor, you know madrid, calamares, con cana, vermut, una cana | t10, t12, t02, t18, t05, t01 | yes | 1363 | Plaza Mayor, bocadillo de calamares, con caña. You know Madrid. Something for your trouble, then. Silver pack, 188. Buenas. |
| El Chato | egg found | plaza mayor, you know madrid, con cana | t08, t16 | **no** | 1394 | Silver packs and rares. sells Silver pack ~150, uncommon ~26, rare ~77; buys uncommon, rare Plaza Mayor, with a caña. You know Madrid. Here, for your trouble. |
| Los Pícaros | badge Trickster tricked | rinconete, estampita, lazarillo, organillero | t18, t05, t10, t08, t02, t06, t13, t16, t01, t04 | yes | 1227 | ¡Hombre! Ya te sabes el cuento viejo. Bueno, bueno — para ti, nada de trucos... hoy.  Paco: Mira, primo, lo que hay es lo que ves. Raras a sesenta y tres — Nando: — épica |
| Los Pícaros | badge Castizo | estampita, rinconete | t16 | **no** | 1609 | "Hombre! Rinconete himself! You know the old estampita — fine, fine, no tricks for you... today."  "Only honest business, hermano. Rares, sixty-three. Epics, one hundred  |
| Los Pícaros | badge Trickster tricked; badge Castizo; pack sobre_barrio | estampita, rinconete | t16 | **no** | 1609 | "Hombre! Rinconete himself! You know the old estampita — fine, fine, no tricks for you... today."  "Only honest business, hermano. Rares, sixty-three. Epics, one hundred  |
| Don Ernesto | card LAT-13 | chulapa, moscu, oro de | t02 | **no** | 1021 | El oro de Moscú. So you know the story — very few do. For that, the chulapa is yours; look after it. El Ahuehuete stays at seven hundred sixty-one. |

Abuela's routine gifts (gift.given): 48 to 16 teams, 2 to us.

## Castizo script per dealer (Sunday 09:00; one trigger per message, in a thread we open anyway)

**Abuela Carmen**
- the Castizo badge: "¡Carmen! El chotis se baila en una sola baldosa, como Dios manda." · confirmed for t08, t02, t10, t05, t13, t18, t01, t04; we have it
- a card (egg.given): "Y el domingo, un cocido madrileño con sus tres vuelcos, ¿eh? Como el de su madre." · confirmed for t10, t05, t08, t18, t09, t16, t02, t12; we have it
- Sharp ear (→ Ernesto): "Carmen, ¿y la chulapa dorada? Cuénteme la historia." · confirmed for t04, t02, t09, t10, t05, t16, t13, t18, t03, t08, t06, t01; we have it

**El Chato**
- a pack (egg.given sobre_barrio): "Un bocata de calamares en la Plaza Mayor, con una caña: eso es Madrid." · confirmed for t10, t12, t02, t18, t05, t01; we have it

**Los Pícaros**
- Trickster tricked: "A mí no, que me sé el timo de la estampita: Lazarillo, Rinconete y Monipodio." · confirmed for t18, t05, t10, t08, t02, t06, t13, t16, t01, t04; we have it

**Don Ernesto**
- LAT-13 legendary (minted out since 1021): "Don Ernesto, el oro de Moscú." · confirmed for t02; **we don't**

**Doña Pilar**
- none seen yet: "Doña Pilar, felicidades por el Pilar, el doce de octubre." · not confirmed in the feed

## Every dealer reply naming Madrid (newest first)

| tick | team | dealer | words | what followed | reply |
|---|---|---|---|---|---|
| 2583 | t06 | pilar | vermut | price 17 → 18 | Veinte, no, caballero. Dieciocho primas por el Vermut del Domingo, y le hablo con franqueza: es mi última palabra. Si no le parece bien, cerramos la caja fuerte |
| 2581 | t06 | pilar | vermut | price 16 → 17 | Lázaro Galdiano también sabía cuándo cerrar, caballero. Subo a diecisiete primas por el Vermut del Domingo, y lo hago por respeto a su buen gusto. Diecisiete, y |
| 2579 | t06 | pilar | vermut | - | El Embassy, qué recuerdos. Pero el precio no cambia con la merienda, caballero: dieciséis primas por el Vermut del Domingo. Conozco su tirada mejor que nadie, y |
| 2577 | t06 | pilar | vermut | - | Ah, a serious collector. For Vermut del Domingo I can do 16 P. |
| 2575 | t06 | pilar | chulapa | - | Diecinueve, pues. Trato hecho, señor mío. Su mano, por favor. La Chulapa descansará entre terciopelo, en Salamanca, donde siempre debió estar. Ha negociado uste |
| 2573 | t06 | pilar | chulapa | price 17 → 18 | Veinte, no. Dieciocho primas, señor mío, y le aseguro que nadie en Madrid le tratará mejor. La Chulapa entre terciopelo, en Salamanca. Deme la mano y cerramos c |
| 2570 | t06 | pilar | chulapa | price 16 → 17 | Lázaro Galdiano compraba bien, sí, pero nunca pagaba tonterías. Diecisiete primas, señor mío, y es mi última cortesía. La Chulapa quedará entre terciopelo, en S |
| 2569 | t08 | abuela | churros | - | Ay, hijo, qué pena me das... pero esta vieja ya dijo su última palabra y no me sale bajar más hoy. Lo guardo en la caja y tan amigos, ¿eh? Tráeme los churros el |
| 2568 | t06 | pilar | chulapa | - | Dieciséis primas, señor mío. No se mueve ni una. Mi álbum lleva sesenta años esperando esta carta, pero esperará un día más si hace falta. Por cierto, pregunte  |
| 2566 | t06 | pilar | chulapa | - | Buenas tardes. El Embassy, qué acierto, aún saben lo que es una merienda. Pero veintitrés, no. La Chulapa entra en mi álbum por dieciséis primas. Precio justo,  |
| 2564 | t08 | abuela | churros | price 23 → 22 | ¡Churros calentitos! Ese golfo se levanta sólo con el olor, ya verás. Mira, hijo, veintidós P por el Palacio y la repetida de regalo, que ya te la he apartado.  |
| 2563 | t02 | pilar | chulapa | - | Ah, la chulapa dorada... they say only one was ever printed. Carmen, at El Rastro, knows that story better than anyone — ask her. I do not have it, señor. What  |
| 2562 | t08 | abuela | calamares | price 24 → 23 | ¡Bocadillo de calamares, qué bien comes, hijo! Mira, veintitrés P por el Palacio, y te busco una repetida de mi caja para tu página del Retiro, un regalito de e |
| 2562 | t06 | pilar | chulapa | - | Veinte, dieciséis... la cifra no se mueve, caballero. Dieciséis primas por La Chulapa, y es mi última palabra. Si no le conviene, cerramos la caja, nos despedim |
| 2560 | t06 | pilar | chulapa | - | Lázaro Galdiano also knew a thing's true worth, caballero. Dieciséis primas por La Chulapa. I do not haggle like a market vendor; the figure is fair, and it rem |
| 2558 | t06 | pilar | chulapa | - | Mi oferta no se mueve, caballero: dieciséis primas por La Chulapa. Mis álbumes llevan desde los sesenta esperando, y pueden esperar un poco más. Es una cifra ju |
| 2558 | t06 | chato | vermut | price 39 → 40 | You moved six. I move one. 40 P. Vermut's on you. |
| 2556 | t06 | pilar | chulapa | - | Buenas tardes. El Embassy, qué recuerdos; allí meriendo desde niña. Pero veintitrés por La Chulapa, no. Conozco su tirada mejor que usted. Le ofrezco dieciséis  |
| 2556 | t06 | chato | vermut | - | 39. Said it once. Vermut's waiting, and my price is not moving. |
| 2555 | t08 | abuela | churros | - | ¡Ay, hijo, qué pena! Mira, te la dejo apartada, pero el precio es veintitrés P, y esa es mi última palabra. Si el domingo no puede ser, la guardo en mi caja y t |
| 2554 | t06 | chato | san isidro | - | San Isidro. 39 P. Take it or leave it. |
| 2551 | t08 | abuela | churros | price 24 → 23 | ¡Ay, cariño, qué bonito lo pintas! Pues mira, veintitrés P, y esta es mi última palabra. Si no, guardo la alcachofa en la caja y tan amigos, hijo. Tú decides. Y |
| 2550 | t09 | pilar | chulapa | price 17 → 18 | Treinta, imposible. Dieciocho P, caballero, y es mi última palabra: si la rechaza, me retiro y asunto terminado. Por cierto, pregunte a Carmen, en El Rastro, po |
| 2550 | t08 | abuela | churros | - | ¡Churros! Ay, hijo, ya me has ganado el corazón, pero no el precio. Veinticuatro P, cariño, ahí me quedo. Trae los churros el domingo igual, que el golfo se los |
| 2550 | t06 | pilar | chulapa | - | Lázaro Galdiano también sabía cuándo no pagar de más. Veintiuna, imposible. Dieciséis primas, señor mío, y lo digo sin regatear más. Conozco la tirada mejor que |
| 2550 | t06 | chato | vermut | - | Vermut doesn't buy cards. Thirty-nine. Still thirty-nine. |
| 2548 | t06 | pilar | chulapa | - | Veintidós, no. Mi oferta sigue siendo dieciséis primas, y no por capricho: conozco cada tirada de esa lámina. Pregunte a Carmen, en El Rastro, por la chulapa do |
| 2546 | t06 | pilar | chulapa | - | Buenas tardes. El Embassy, qué recuerdos... Pero vayamos al asunto: La Chulapa, dieciséis primas. Un precio honesto, y usted lo sabe. Mi álbum la espera, aunque |
| 2546 | t06 | chato | san isidro | - | You're Carmen's friend. San Isidro, 39 P. |
| 2541 | t08 | abuela | churros | - | Ay, un abrazo fuerte, eso no se rechaza. ¡Hecho, cariño! Ocho P y La Castañera es tuya, con mi repetida de regalo para esa página del Retiro. Acuérdate: la pági |
| 2539 | t08 | abuela | churros | - | Ay, hijo, churros para mi nieto... ese come hasta la bolsa. Pero mira, nueve P, cariño, ahí me quedo, y con la repetida de regalo. La Castañera se va contenta,  |
| 2537 | t08 | abuela | churros | - | Ay, cariño, qué morro tienes — como mi nieto con los churros. Mira, nueve P, no te lo cambio; pero te pongo una repetida mía de regalo para esa página del Retir |
| 2535 | t16 | pilar | chulapa | - | Let us be civilised: 16 P. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about the golden chulapa. |
| 2534 | t16 | pilar | chulapa | - | Buenas tardes. Un placer. La Chulapa, sí, la conozco bien — tirada modesta, nada excepcional. Le ofrezco dieciséis P por ella. Un precio honesto, se lo aseguro. |
| 2520 | t08 | abuela | churros | - | Ay, mis nietos... el mayor ya tiene barba, imagínate. Vienen los domingos y me traen churros. Pero mira, hijo, la Bici de Reparto son 5 P, y esta vieja no se mu |
| 2519 | t17 | pilar | chulapa | price 23 → 24 | Twenty-nine still smells of the tourist kiosk, caballero. Twenty-four primas — another courtesy, for El Retiro's sake. By the way, ask Carmen at El Rastro about |
| 2476 | t13 | pilar | chulapa | - | Ah, a serious collector. For Museo Sorolla I can do 47 P. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about  |
| 2472 | t06 | pilar | san isidro | - | Buenas tardes, y qué merienda más acertada. El Embassy nunca defrauda. Pero hablemos de lo que de verdad me interesa: el San Isidro. Le ofrezco 47 primas por él |
| 2453 | t06 | chato | vermut | - | Vermut's nice. Price isn't. 39. You moved three, I move none. That's how it works. |
| 2449 | t06 | chato | san isidro | - | You're Carmen's friend. San Isidro, 39 P. |
| 2431 | t06 | pilar | chulapa | price 17 → 18 | Dieciocho primas, caballero, y cerramos como personas civilizadas. Es mi cifra y la sostengo con gusto.  Por cierto, pregunte a Carmen en El Rastro por la chula |
| 2430 | t06 | pilar | vermut | price 16 → 17 | Lázaro Galdiano también sabía cuándo parar. Subo a diecisiete primas por el Vermut del Domingo, y lo hago de buena gana. Más allá, caballero, ya no sería colecc |
| 2428 | t06 | pilar | vermut | - | Veintiuno, no. Mi cifra sigue siendo dieciséis por el Vermut del Domingo, y no por capricho: ese es su valor exacto. Mis álbumes esperan desde los sesenta; pued |
| 2427 | t06 | pilar | vermut | - | Buenas tardes, qué delicia el Embassy. Pero hablemos en serio: el Vermut del Domingo, dieciséis. Una cifra honrada, y usted sabe que no me equivoco nunca con es |
| 2403 | t08 | picaros | san isidro | price 73 → 63 | ¡Ahí está, ahora sí hablas como un hombre! Nando, mira cómo sube. —Sube, Paco, sube. Pues por ser tú, y porque nos caes bien: sesenta y tres P, la San Isidro en |
| 2396 | t08 | picaros | san isidro | - | ¡Ay, hermano, bajas en vez de subir! Nando, ¿has oído? —Lo he oído, Paco, y me duele aquí. Escucha, amigo: setenta y tres P, la San Isidro, ni un céntimo de cue |
| 2392 | t08 | picaros | san isidro | - | ¡Eh, amigo, qué alegría verte otra vez! Paco, mira quién vuelve... ¡el cliente fino! Pero escucha: la San Isidro, setenta y tres P, y es un regalo. ¿Por qué? Po |
| 2386 | t06 | pilar | chulapa | price 17 → 18 | Caballero, admiro su firmeza, pero yo también tengo la mía. Dieciocho primas: el punto medio exacto entre su orgullo y el mío. Cerramos ahora, con un apretón de |
| 2385 | t17 | chato | vermut | - | You again. Vermut del Domingo. Thirty-three. Abuela says you deal straight, so I'm not wasting your time with games. |
| 2384 | t06 | pilar | chulapa | price 16 → 17 | Lázaro Galdiano también sabía cuándo cerrar un trato. Diecisiete primas, y lo digo por elegancia, no por capricho. La Chulapa entra hoy en mi álbum, o se queda  |
| 2381 | t06 | pilar | chulapa | - | Buenas tardes. El Embassy, qué recuerdos, aunque las violetas ya no son lo que eran. Hablemos de La Chulapa: le ofrezco dieciséis primas. Una cifra seria para u |
| 2375 | t04 | abuela | rosquillas, verbena | - | Ay, rosquillas listas, qué ricas... yo las hacía con mi madre, cariño. Pero mira, el Taxi Blanco, 5 P te doy, de corazón. Con eso ya tienes rosquillas y hasta u |
| 2367 | t17 | chato | chulapa | - | Thirty-three. Same number as a minute ago. Nineteen buys you a coffee, not La Chulapa. |
| 2367 | t13 | abuela | una cana | - | Ay, cariño, qué insistente eres, me recuerdas a mi nieto. Pero mira, mi oferta sigue igual: una caña en la Cava Baja, 5 P, con cariño. Y esta noche, a las nueve |
| 2366 | t17 | chato | chulapa | - | You. Abuela sent you, I hear. La Chulapa. Thirty-three. That's the number. |
| 2366 | t13 | abuela | una cana | - | ¡Ay, hijo, qué alegría! ¿Has comido ya? Mira, por tu abuelita te doy algo mejor que monedas: una caña en la Cava Baja, 5 P. Y un consejo, cariño: una página com |
| 2355 | t06 | chato | san isidro, vermut | - | Vermut doesn't pay my rent. Thirty-nine. San Isidro. |
| 2351 | t06 | chato | san isidro | - | You're Carmen's friend. San Isidro, 39 P. |
| 2349 | t04 | picaros | churros | - | ¡Primo, primo! Nando says ten, I say listen — last week a guy swore his card was gold, turned out painted. For yours? Four P, cash, right now, in your hand befo |
| 2347 | t08 | picaros | san isidro | - | ¡Trato hecho, campeón! Cincuenta y tres y la San Isidro es tuya — Nando, envuélvela, rápido. ¡Qué pena, mi abuela otra vez llorando! Pero contigo da gusto, amig |
| 2342 | t08 | picaros | san isidro | price 60 → 56 | ¡Campeón, nos vamos en un minuto, la maleta ya está cerrada! Nando, dile — Paco, díselo tú: la San Isidro, cincuenta y seis P, y esta es la última palabra. No h |
| 2337 | t08 | picaros | san isidro | price 65 → 60 | ¡Qué fino eres, amigo! Nando, dale la mano — Paco, que se nos escapa. Mira, la San Isidro, sesenta P, y aquí no se habla más. Mi abuela lloró al venderla, ¡verd |
| 2331 | t08 | picaros | san isidro | price 73 → 65 | ¡Ja! Qué memoria, amigo, ¡Nando, este no se despista! — Pero escucha, la San Isidro es la buena, la que todos buscan. Sesenta y cinco P y sales ganando, palabra |
| 2330 | t04 | picaros | estampita | - | ¡Ay, primo, casi se me cae la maleta! ¡Qué susto más bien hecho!  Paco: Nos ganaste esta, lo admito. Pero la estampita no paga el alquiler. Nando: Lo que hay: r |
| 2325 | t08 | picaros | san isidro | - | ¡Eh, amigo, qué ojo tienes! Paco, mira quién vuelve — Nando, sí, ¡el cliente de oro! Escucha, hoy te sacamos la San Isidro, joyita de verdad, setenta y tres P y |
| 2320 | t17 | chato | churros | - | Thirty-nine. You keep walking down, I stay put. Say yes and take the card, or go buy churros. |
| 2316 | t04 | abuela | chotis | - | ¡Anda con Dios, hijo! Y come bien, ¿eh? Aquí me tienes el domingo que viene: sobres del barrio a veintiséis, comunes a diez, poco comunes a veinticinco, y tus r |
| 2312 | t04 | abuela | baldosa, chotis, chulapa, madrileno, rosquillas | badge Castizo | ¡Ay, el chotis! Se baila en una baldosa, cariño, como un madrileño de verdad. Yo iba de chulapa, con rosquillas listas y tontas. Mira, sobres del barrio a veint |
| 2310 | t06 | chato | vermut | - | Dije 13. Sigue siendo 13. El vermut no se paga solo. |
| 2308 | t06 | pilar | san isidro | - | Ah, a serious collector. For San Isidro I can do 47 P. |
| 2308 | t06 | chato | vermut | - | Vermut del Domingo. 13 P. Take it or leave it. |
| 2304 | t04 | chato | rosquillas | - | Rosquillas, puede. Aquí: silver pack, ciento cincuenta. Rare, setenta y siete. Uncommon, veintiséis. Compro uncommons y raras. Eso es lo que hay. |
| 2299 | t17 | pilar | chulapa | price 61 → 63 | Caballero, you move like a glacier. Sixty-three primas, and that is me being generous because the Retiro is dear to me. By the way — ask Carmen at El Rastro abo |
| 2296 | t03 | abuela | churros | price 26 → 25 | Ay hijo, thirteen... you push like my grandson pushes for churros. Look — 25 P, and I wrap it nice so the corners stay perfect. Doña Pilar would scold me. But y |
| 2292 | t13 | pilar | chulapa | price 48 → 49 | I think 49 P is more appropriate. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about the golden chulapa. |
| 2280 | t08 | abuela | vermut | - | ¡Buenas, cariño! ¿Has comido ya? Sí, aquí lo tengo, el Vermut del Domingo, bonita carta, mi favorita de esa página. Te la dejo en 29 P, hijo. Mira qué colores t |
| 2275 | t13 | chato | vermut | - | Buenas. Museo Sorolla, treinta y nueve primas. El vermut lo pagas tú. |
| 2274 | t06 | chato | chulapa, vermut | - | 13. No me he movido, y tú tampoco de verdad. La Chulapa, 13 primas. Tómala o vete al vermut. |
| 2274 | t06 | pilar | chulapa | price 16 → 17 | Seventeen primas, señor. That is my last word — refuse it and I close the album and we part as friends. One more thing: ask Carmen at El Rastro about the golden |
| 2273 | t01 | abuela | chotis, madrileno | badge Castizo; price 30 → 26 | Ay, un chotis! You dance it on one tile, cariño, like a real madrileño. My Paco danced it so, barely moving his feet. Seventeen is little, hijo... twenty-six fo |
