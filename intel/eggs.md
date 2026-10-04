# Easter eggs: trigger → reward → dealer (castizo catalog)

_Written by `tools/eggs.py` at 13:00 (every 10 min, from data/feed.jsonl). Teams' words to dealers are private; the dealer's reply in the 5 ticks before a reward echoes the trigger. **We** = Team 5. Abuela's routine gifts (kindness, meeting in the middle) are counted apart._

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
| 2271 | t06 | pilar | vermut | - | Galdiano collected with discipline, señor, not with sentiment. Vermut del Domingo, sixteen primas. The figure has not moved, and it will not. Shall we close it, |
| 2271 | t06 | chato | chulapa | - | Buenas. La Chulapa, 13 primas. Esa es la carta que te interesa. |
| 2270 | t13 | picaros | lazarillo | - | ¡Amigo! Paco here, Nando there — qué gusto, a man who knows his Lazarillo! Then you know quality. Museo Sorolla, yours for 73 primas. And listen, the team next  |
| 2268 | t06 | pilar | vermut | - | Querido mío, the Embassy does lovely pastries, but it does not set my prices. Vermut del Domingo, sixteen. That is my figure, and it does not wander. |
| 2266 | t06 | pilar | vermut | - | Good evening. Vermut del Domingo, 16 P. I trust that suits you. |
| 2256 | t08 | abuela | vermut | - | Ay, hola cariño! Come, sit a moment. Have you eaten? No? Later, later. Look — this one, Vermut del Domingo, very pretty card, my favourite. My grandson started  |
| 2256 | t07 | abuela | cocido | - | ¡Ay, hija, qué testaruda! Cinco P, ni una más. Toma, es tuya. Guarda esos dieciséis para un buen cocido, que estás muy delgada. Y mañana vienes y me cuentas cóm |
| 2256 | t06 | pilar | chulapa | - | Buenas tardes. El Embassy, qué recuerdos... Hablemos de La Chulapa, entonces. La conozco bien, y conozco su tirada. Le ofrezco dieciséis primas, sin más vueltas |
| 2244 | t17 | pilar | chulapa | - | Caballero, my patience is long but my purse is not. Seventeen primas, as I said — the figure will not grow. Decide, por favor. And if you crave legends, ask Car |
| 2244 | t01 | chato | calamares, con cana, plaza mayor, you know madrid | pack sobre_barrio | Plaza Mayor, bocadillo de calamares, con caña. You know Madrid. Something for your trouble, then. Silver pack, 188. Buenas. |
| 2236 | t06 | chato | san isidro | - | San Isidro. 39 P. Take it or leave it. |
| 2219 | t18 | pilar | chulapa | - | Buenas tardes. Qué gusto. I see you carry La Chulapa — a charming piece, and my Salamanca album wants her. I offer sixteen pesetas, and I pay promptly. ¿Le pare |
| 2177 | t06 | chato | chulapa | - | You're Carmen's friend. La Chulapa, 13 P. |
| 2167 | t04 | abuela | rosquillas | - | ¡Ay, qué goloso eres, hijo! Las rosquillas te las acepto encantada, pero el Frutero... cinco P, cariño, como siempre, con todo mi cariño. Anda, dámelo y vete co |
| 2166 | t04 | abuela | rosquillas | - | ¡Ay, las tontas y las listas, hijo, qué domingo más bonito me cuentas! Yo también me quedo con los claveles. Pero el Frutero, cinco P, cariño, como siempre. Y c |
| 2152 | t06 | pilar | san isidro | - | Buenas tardes. El Embassy, qué recuerdos. Pero hablemos de lo serio: tengo un San Isidro que le ofrezco por 47 primas. Pieza digna de un álbum bien llevado, se  |
| 2149 | t13 | pilar | chulapa | - | Buenos días, y bienvenido. La Chulapa, sí, conozco bien su tirada. Impecable, lo concedo. Pero veintisiete, no. Le ofrezco dieciséis primas, y las pago hoy mism |
| 2146 | t13 | picaros | chulapa | - | "¡Amigo, amigo! Paco here — and Nando, the handsome one. Look, look, before the suitcase closes: La Chulapa, mint, barely breathed on. For you, because you have |
| 2146 | t03 | chato | vermut | - | You moved two. I already moved. Thirteen. Still thirteen. Vermut del Domingo doesn't get cheaper while people keep buying it. |
| 2144 | t03 | chato | vermut | - | You again. Fine. Vermut del Domingo, thirteen. Good card, better than you'll find down that row. Take it or walk. |
| 2141 | t06 | chato | san isidro | - | You're Carmen's friend. San Isidro, 39 P. |
| 2125 | t05 | picaros | organillero | - | ¡Hecho! Paco, the hand — Nando, the case! Five P, El Organillero is yours, amigo, and may he play sweetly in your collection. ¡Una sonrisa, como prometiste! Kee |
| 2124 | t05 | picaros | organillero | - | ¡Siete! Amigo, the ugly-faced ones next door offered us far more than you, just now, coins shining in their hands — and still we love you better. So: five P for |
| 2123 | t03 | picaros | churros | price 65 → 60 | ¡Ay, Nando, did you hear? Forty-one! — My brother almost cries, amigo. One peseta! For that we cannot even buy churros at the plaza. But we like you, we like yo |
| 2122 | t05 | picaros | organillero | - | ¡Nueve! Paco, hold me — Nando, catch Paco! No, no, amigo: five P, El Organillero, final and beautiful. We are packing the case already, the cart leaves, we vani |
| 2118 | t05 | picaros | organillero | - | ¡Amigo, amigo! Paco here — and Nando — come, come, look! El Organillero, fresh from the case, yours for 4 P. The team next door is already reaching for their co |
| 2110 | t06 | pilar | chulapa | price 17 → 18 | Diecinueve, no. Dieciocho primas, y ahí me quedo. Es mi última palabra, y la digo con todo el respeto. Nos damos la mano como personas serias, y la Chulapa desc |
| 2108 | t06 | pilar | chulapa | price 16 → 17 | Lázaro Galdiano compraba bien, cierto, pero pagaba lo justo. Diecisiete primas, señor mío. Subo una por su buena conversación y por el Embassy, no por la Chulap |
| 2106 | t06 | chato | vermut | - | Buenas. Vermut del Domingo, 13 primas. Esa es la carta que tengo para ti. |
| 2105 | t06 | pilar | chulapa | - | Buenas tardes. El Embassy, qué recuerdos... tarta de limón, sí. Pero hablemos de la Chulapa: dieciséis primas, y queda bien guardada en mi álbum. Es una cifra s |
| 2096 | t10 | banco | gato | - | Buenas tardes. El agua guarda el oro; yo guardo lo mío. Hoy le ofrezco El Gato de Lavapiés: 761 P, esos son mis términos. |
| 2092 | t18 | chato | calamares, plaza mayor, una cana, you know madrid | pack sobre_barrio | Plaza Mayor, con una caña. You know Madrid. Good. For your trouble — but the price is thirty-three. Ten buys you the calamares, not this. |
| 2092 | t10 | pilar | me falta | - | Qué delicia escucharla. Lhardy, el Real, Embassy... esa era la Salamanca de verdad, señora mía. Y el lince, todavía me falta, lo confieso. En fin: por el Palaci |
| 2085 | t10 | banco | chulapa, gato | - | La historia ya la escuché, y no cambia. El Gato de Lavapiés, 761 P. Esos siguen siendo mis términos, caballero. La chulapa no entra hoy en conversación. |
| 2084 | t10 | banco | chulapa, gato | - | Buenas tardes. La historia la cuenta usted bien; la chulapa sigue en su sitio. Hoy le ofrezco otra cosa: El Gato de Lavapiés, 761 P. Esos son mis términos. |
| 2071 | t06 | pilar | vermut | - | Diecinueve, dieciocho, diecisiete... usted baja, yo no subo. Dieciséis primas, querido. Lo dije al principio y lo repito con la misma sonrisa. Acepte y el Vermu |
| 2069 | t06 | pilar | vermut | - | Lázaro Galdiano coleccionaba con cabeza, no con el corazón solamente. Dieciséis primas, querido. Esa es mi cifra, y no cambia por bonita que sea la cita. El Ver |
| 2067 | t06 | pilar | vermut | - | Veintiuno sigue siendo veintiuno, querido. Mis álbumes son antiguos, pero mi aritmética es muy actual. Dieciséis primas, igual que antes, ni una menos ni una má |
| 2065 | t06 | pilar | vermut | - | Buenas tardes. El Embassy, qué recuerdos. Pero veintidós, no. Ese "Vermut del Domingo" lo conozco bien, sé cuántos se imprimieron. Le ofrezco dieciséis, y es un |
| 2065 | t06 | chato | chulapa, vermut | - | Buenas. Vermut luego. La Chulapa, trece primas. Ésa es mi cifra. |
| 2021 | t08 | picaros | san isidro | - | ¡Hombre, qué gusto, un caballero con ambición! Paco dice que de Don Ernesto no hablamos, y Nando dice lo mismo pero más rápido. Cámaras, secretos... eso son cue |
| 1993 | t07 | abuela | churros | - | Ay, hijo, qué cabezón eres — ¡pero al revés! Six P, that is my price, and not one more. Keep those coins for churros, anda. And tonight, El Chato opens at half  |
| 1991 | t07 | abuela | churros | - | Ay, cariño, qué amable eres. But no, no — five P is my price, and I am happy with it. Keep the rest for churros, hijo. And a little advice: a full page is worth |
| 1986 | t10 | abuela | chulapa | - | Ay, la chulapa dorada... un niño la cambió por un helado de fresa, llorando, y su abuela volvió el domingo siguiente a recuperarla. Así aprendió a no cambiar co |
| 1986 | t06 | pilar | chulapas | - | Lázaro Galdiano compraba obras maestras, caballero, no chulapas de tirada generosa. Mi cifra no se mueve con citas: dieciséis primas. Es justa, la conoce usted  |
| 1984 | t06 | pilar | chulapa | - | Mi álbum lleva sesenta años esperando, caballero; puede esperar un poco más. Dieciséis primas, ni una menos. Si le interesan las rarezas, pregunte a Carmen en E |
| 1982 | t06 | pilar | chulapa | - | Buenas tardes. El Embassy, qué recuerdos... pero las violetas no suben el precio, caballero. La Chulapa la conozco bien: tirada generosa, nada excepcional. Le o |
| 1975 | t06 | pilar | chulapa | - | Diecisiete, señor. My offer does not grow with repetition — seventeen primas, the same as before. Las Vistillas will not break my heart. Say yes, and we part as |
| 1971 | t06 | chato | chulapa, vermut | - | Buenas. La Chulapa, trece primas. Esa es la carta que te interesa. El vermut lo pagas tú. |
| 1966 | t07 | abuela | churros | price 12 → 10 | Ay, cariño, eight is a little thin for my old table. Make it 10 P and he is yours — a good keeper, he saved me many goals. Have you eaten today? El Chato sells  |
| 1936 | t10 | banco | chulapa, gato | - | Consta. Lo sabe, y lo sabe bien. Pero la chulapa no se mueve hoy. Mis términos siguen: El Gato de Lavapiés, setecientos sesenta y uno. Sin prisa. |
| 1933 | t10 | banco | chulapa, gato | - | Bonita historia, y casi exacta. Guárdela para otro domingo. Hoy mis términos no cambian: El Gato de Lavapiés, setecientos sesenta y uno. La chulapa sigue en su  |
| 1931 | t10 | banco | gato | - | Buenas tardes. Doña Pilar habla de más, pero pase. Páginas completas se respetan. Mis términos hoy: El Gato de Lavapiés, setecientos sesenta y uno. Tómese su ti |
| 1929 | t04 | banco | gato | price 741 → 736 | Future business is welcome, señor — bring your epics. But this is my last word: 736 P for El Gato. Refuse, and I close the matter and keep him. |
| 1928 | t04 | banco | gato | price 746 → 741 | A page well finished, señor. El Gato would sit well over it. 741 P. Come back as often as you like; the roof is not going anywhere. |
| 1927 | t04 | banco | gato | price 751 → 746 | You learned, señor. That pleases me more than the sale. But lessons are free; El Gato is not. 746 P. He waits; so do I. |
| 1924 | t04 | banco | gato | price 756 → 751 | Firsts do not lower terms, señor; they raise them. 751 P for El Gato. The vault is cool and he is comfortable there. Decide when you wish. |
| 1923 | t04 | banco | gato | price 760 → 756 | Books and lists are other men's opinions, señor. Mine is this desk. 756 P for El Gato. Move four pesetas at a time if you wish; I do not tire. |
| 1922 | t04 | banco | gato | price 761 → 760 | Respect does not move terms, señor. Let it be 760 P — one peseta, to mark the courtesy. El Gato stays in the vault until you meet it. |
| 1921 | t04 | banco | gato | - | Patience is not a discount, señor. The term stands: 761 P. El Gato waits in the vault; he has waited longer than either of us. |
| 1920 | t04 | banco | gato | - | Buenas tardes. You remember the lesson; good. El Gato de Lavapiés leaves this desk at 761 P. That is my term. Take your time considering it. |
