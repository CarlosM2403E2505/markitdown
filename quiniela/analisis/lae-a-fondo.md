# La Quiniela de LAE a fondo (22/11/2026)

Encargo de Carlos (22/11, 3:16): desmontar cómo funciona la Quiniela de SELAE y traer «profesionales de allí» a la mesa.
Fuentes de clase A: normas oficiales de La Quiniela y Elige 8 (oct. 2019, loteriasyapuestas.es), normas de 2017 (hacienda.gob.es), guía del quinielista (selae.es), aviso de suspensión de la J7 (16/09/2026) y nota de prensa de la J21 (15/11/2026). Datos: histórico oficial de LAE (`importado/quiniela-mesa/datos/historico-quiniela/hist.json`, 749 jornadas con acertantes entre 2002 y 2018) y escrutinios de 2026/27. Herramienta: `herramientas/analista_lae.py` (tests en `test_analista_lae.py`).

## 1. Quién pone los 15 partidos y cómo
- **Los elige SELAE** (norma 3.ª): 14 partidos combinables más el Pleno al 15, de competiciones autorizadas por la RFEF u otros organismos (norma 1.ª). La norma no fija cuántos de cada liga.
- **Lo que hace en la práctica** (`importado/.../patrones-seleccion-lae.md`, 2026/27):
  - manda el calendario: entran los partidos del sábado al lunes, y casi nunca los de jueves o viernes;
  - si sobra un partido, cae el de los equipos pequeños;
  - en una jornada normal de domingo pone 7 de Primera, 3 de Segunda y 4 de Liga F;
  - en las semanas europeas mete a todos los españoles y a los grandes de fuera;
  - el Pleno lleva a un grande en 8 de cada 14 jornadas, o es el último partido.
- **Sustitución** (norma 39.ª A): si antes de las 24:00 del jueves de la semana anterior SELAE sabe que un partido no se jugará, pone otro y lo anuncia.
- **Ventana de validez** (norma 38.ª): un partido solo vale si empieza entre las 12:00 del día anterior a la jornada y las 24:00 del día siguiente (hora peninsular).
- **Qué cuenta como resultado:** el marcador cuando el árbitro termina el partido, con la prórroga incluida si se juega. Si se suspende a medias, vale el marcador del momento de la suspensión, salvo que se reanude dentro de la ventana. Las anulaciones posteriores no cambian nada.
- **Partido sin resultado válido → sorteo** (norma 39.ª B): un bombo de 100 bolas con tantas bolas de cada signo como **% de pronósticos del público**. Para el Pleno se hace con bolas 0, 1, 2 y M. Ejemplo: en la J7 de 2026 se suspendió el Levante–Athletic por lluvia y se sorteó el jueves 17/09 a las 22:00.

**Para la mesa:** si LAE anuncia un sorteo, la probabilidad real de ese signo es el % del público, y es un dato de clase A. En ese caso la mesa usa `analista_lae.py sorteo jNN.json N`. Es la única vez que el % del público entra en una probabilidad, porque es el propio mecanismo del resultado.

## 2. Dinero: precio, fondos y botes
| Concepto | Norma |
|---|---|
| Precio | 0,75 € la apuesta de Quiniela; 0,50 € la de Elige 8 |
| Boleto sencillo | De 2 a 8 apuestas |
| A premios | 55 % de la recaudación |
| 14 aciertos | 16 % |
| 13 aciertos | 7,5 % |
| 12 aciertos | 7,5 % |
| 11 aciertos | 7,5 % |
| 10 aciertos | 9 % |
| Pleno al 15 (especial) | 7,5 % |
| Elige 8 | 55 % de su propio fondo |

- **El Pleno solo cobra con 14 aciertos** (norma 8.ª). Con 13 y el Pleno acertado no se cobra nada por el Pleno.
- **Botes** (normas 7.ª y 8.ª):
  - si nadie acierta 14, ese fondo pasa a la especial de la jornada que SELAE designe;
  - si nadie acierta el Pleno, su fondo pasa a la especial de una jornada que SELAE designa y anuncia;
  - si queda desierta una categoría de 13 a 11, su fondo baja a la categoría siguiente.
- **Mínimos:**
  - si una categoría paga más que la de encima, las dos se juntan y se reparten a partes iguales;
  - un premio de 11, 12 o 13 por debajo de 1 € no se paga y su fondo sube a la categoría de encima;
  - un premio de 10 por debajo de 1,50 € no se paga y su fondo pasa a la especial.
- **Retorno:** de media vuelven 0,55 € por euro. Solo se gana algo extra acertando lo que el público no juega.

## 3. Elige 8
Hay que jugar una Quiniela en método directo, elegir 8 de los 14 partidos y pagar 0,50 € por apuesta. El fondo (55 %) se reparte entre las apuestas con más aciertos, de 8 hacia abajo. En la J21 hubo 49 apuestas de 8 aciertos, que cobraron 666,36 € cada una.

**Decisión de la mesa: no entra.**
- Con el tope de 18 € y 24 sencillas no queda presupuesto: cada Elige 8 quita una apuesta de 0,75 €.
- Devuelve el mismo 55 %.
- No se puede jugar en reducidas ni en condicionadas.

## 4. Lo que dice el histórico (749 jornadas oficiales, 2002-2018)
| Hallazgo | Dato |
|---|---|
| Cada **X** del resultado | Deja los acertantes de 14 en ×0,56, así que el premio sube unas **1,8 veces** |
| Cada **2** del resultado | Deja los acertantes en ×0,68, así que el premio sube unas **1,5 veces** |
| Con 4 o menos signos que no son 1 | Unos 48 acertantes de 14 por millón de euros y premio mediano de 5.700 € |
| Con 8 signos que no son 1 | 1,7 acertantes por millón y premio mediano de 103.000 € |
| Con 10 o más signos que no son 1 | Bote (nadie acierta 14) en el 25-78 % de las jornadas |
| Bote de 14 en total | 104 de 853 jornadas (12 %) |
| Pleno con acertantes de 14 | Lo acierta una mediana del 30 % de los que tienen 14; en el 19 % de esas jornadas no lo acierta nadie |
| Premio de 13 | Mediana de 1.380 € (la mitad central, entre 380 y 5.137 €). En 2026: 158 € (J19), 165 € (J14) y 6.796 € (J13) |
| Secuencia de signos | No hay patrón (estudio de `historico-quiniela-1972-2026.md`): ni por casilla ni por la jornada anterior |
| Jornadas europeas de 2026 | Cerca de 1 M€ de recaudación. Cuando ganan los favoritos el 14 paga poco: J5, 270 acertantes a 590 € |

**Conclusión:** el público juega sobre todo unos, y lo que menos juega es la X. Acertar una X que la mesa ve y el público no es lo que más hace subir el premio. Esto confirma, desde el lado del dinero, la regla de la mesa de no dejar escapar las X (§1.9 y §1.13).

**Límite:** por decisión de Carlos (§1.12), el % del público no cambia ningún signo ni sirve para desempatar. Por eso este estudio no toca el boleto: solo informa.

## 5. Ejemplo: J21 contra el público (`analista_lae.py valor jornadas/j21/j21.json --recaudacion 1586225`)
- **El público sobrejugaba** a Almería (84 % frente al 61 % de la mesa), Tenerife (78 % frente a 49 %), Eibar (75 % frente a 54 %) y Granada (55 % frente a 43 %).
- **La mesa veía más** a los locales de Liga F (por ejemplo, Real Sociedad F: 58 % frente a 39 %).
- **Comprobación del modelo de premios:**
  - el resultado real tenía un producto del público de 7,1·10⁻⁷;
  - suponiendo apuestas independientes salían 1,5 acertantes, y hubo 4;
  - de ahí el factor de correlación de 2,5, que se recalibra con cada escrutinio.

## 6. Profesionales nuevos de la mesa (criterios comprobables)
| Rol | Equivale en LAE a… | Qué hace, con criterio fijo | Veto |
|---|---|---|---|
| **Analista LAE (reglamento y calendario)** | Departamento de juego de SELAE, que compone la jornada y aplica la norma 39.ª | (1) Coteja la lista oficial con el calendario y marca los partidos fuera de la ventana de la norma 38.ª. (2) Busca avisos de LAE de suspensión, sustitución o sorteo. Solo con aviso oficial (clase A) aplica `analista_lae.py sorteo` con p = 1. Con alerta meteorológica oficial lo avisa, pero no mueve el precio. (3) Comprueba que el boleto cumple la norma: 0,75 €, de 2 a 8 apuestas por boleto sencillo, ≤ 18 € en total, Pleno con 0, 1, 2 o M y el Pleno en todas las apuestas. (4) Anota si hay bote anunciado y para qué jornada | **Sí**, si el boleto incumple una norma |
| **Analista de Premios (valor frente al público)** | Escrutinio de SELAE y mesa de pagos | (1) Con el % LAE (quiniela15 o eduardolosilla), da por partido la razón mesa/público; ≥ 1,25 con P ≥ 20 % es «con valor» y ≤ 0,80 en el favorito del público es «sobrejugado». (2) Da para cada columna los acertantes de 14 esperados y el premio si acierta. (3) Informa de cuántas X del boleto son X «con valor». (4) Después de cada jornada, añade el escrutinio a `datos/premios.json` y recalibra el factor de correlación (en el test se acepta entre 2 y 6 acertantes en la J21). **Nunca cambia un signo ni el Pleno** (§1.12) | No |

**Al Auditor se le añaden tres comprobaciones:**
- el informe del Analista LAE trae la conformidad con la norma;
- si hubo aviso de sorteo, el partido usa la mezcla;
- la entrega no dice que el Pleno cobre sin 14.
