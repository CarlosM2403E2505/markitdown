# Autopsia de rojos (regla R8, 26/11/2026)

Carlos, 26/11: «Aprendan de los errores todos y cada uno de los miembros de la mesa. A partir de ahora cada uno, después de cada rojo, va a profundizar por qué fallaron los partidos». Y añade un miembro nuevo, el **Periodista deportivo**, que reúne la mirada de todas las profesiones de la mesa y se encarga de esto.

## 1. Qué es un rojo

Un partido es **rojo** cuando el signo real:
- no va en el boleto principal (reducida o boleto de 18 €), o
- va en menos del 25 % de las sencillas jugadas.

El **Pleno** fallado también es rojo. Solo cuenta lo jugado de verdad (`jugado_real` de la jornada).

## 2. Cuándo y quién

- **Cuándo:** la mañana siguiente a cada partido rojo (o en el escrutinio, si cae antes). Sin esperar al final de la jornada.
- **Periodista deportivo (nuevo, miembro 12):** lanza el prompt de Google (§5) sobre cada rojo, comprueba los datos (solo clase A y B, sin Marca, Sport, Mundo Deportivo ni L'Équipe), rellena la ficha de hechos y redacta la autopsia de la mesa. Lleva el registro `datos/autopsias.json`.
- **Cada miembro** contesta su pregunta fija (§3) en una línea, con un veredicto: **varianza** o **fallo nuestro**, y si es fallo nuestro, qué hipótesis medible propone.

## 2b. Lo que se investiga SIEMPRE en cada autopsia (Carlos, 26/11)

1. **¿Sale una regla nueva?** Cada autopsia termina con «regla nueva: sí/no» y, si sí, la hipótesis medible (H1, H2…) en `datos/autopsias.json`.
2. **Por qué falló, a fondo:** todas las causas posibles, no solo la primera (táctica, bajas, árbitro y VAR, estado físico, calendario, motivación, clima y campo, puntería).
3. **Por qué LAE eligió ese partido** (Analista LAE): calendario de la ventana (norma 38.ª), si es grande o equipo español, si es el último partido (Pleno), y qué dice el histórico LAE de partidos parecidos (`datos/lae_historico.json`, 609 jornadas con Pleno).
4. **El Pleno, siempre**, acierte o falle: marcador real frente al nuestro, puesto del real en nuestra lista de 16, y comparación con el histórico LAE del mismo tipo de partido.

## 3. La pregunta fija de cada miembro

| Miembro | Pregunta tras el rojo |
|---|---|
| Investigador | ¿Había una baja, rotación, lesión o noticia de clase A/B antes del partido que no entró en el precio? |
| Matemático | ¿Qué P daba la mesa al signo real y qué decía el intervalo? ¿Es un fallo raro (P < 10 %) o normal? |
| Físico | ¿Cuadra el xG real con los goles esperados del modelo (λ)? ¿Quién dominó de verdad? |
| Compilador | ¿Estaban bien los datos de entrada (liga, fecha, alineación probable, partidos recientes)? |
| Trader | ¿Cómo se movió la cuota desde la apertura al cierre? ¿El mercado vio algo que nosotros no? |
| Risk Manager | ¿En cuántas columnas iba el signo real? ¿Cumplieron R3 y la protección de fijos? ¿Un solo partido tumbó todo? |
| Científico de datos | ¿Se repite el patrón en el registro de autopsias (misma causa, mismo tramo de P, misma competición)? |
| Director | ¿Se decidió bien con lo que se sabía antes del partido? |
| Auditor | ¿Los hechos son de clase A/B, están comprobados y no se ha cambiado ninguna regla sin prueba? |
| Analista LAE | ¿Por qué eligió LAE este partido y qué dice su histórico de partidos parecidos? ¿Afecta alguna norma (aplazamiento, horario, sorteo)? |
| Analista de Premios | ¿Cuánto cuesta este rojo en premio esperado (cuántas columnas de 12-14 aciertos tumbó)? |
| Periodista deportivo | ¿Qué pasó en el campo? Goles con minuto, xG, expulsiones, penaltis y VAR, lesiones durante el partido, rotaciones, crónica en dos frases. |

## 4. De la lección al ajuste (determinista)

1. **Clasificación del rojo** (la hace el Periodista con la ficha, sin opinión):
   - **Varianza:** el favorito de la mesa ganó el xG por 0,5 o más, sin expulsión propia ni lesión clave antes del gol decisivo, y sin baja ni rotación de clase A/B que no se hubiera visto.
   - **Causa identificable:** todo lo demás, con una etiqueta fija: `baja_no_vista`, `rotacion`, `expulsion`, `penalti_var`, `lesion_en_partido`, `rival_superior_xg`, `dato_entrada`, `cobertura_boleto`.
2. Cada rojo se apunta en `datos/autopsias.json` (jornada, partido, P de la mesa y de las casas del signo real, xG, columnas que lo llevaban, clasificación, etiqueta, fuente).
3. **Ninguna regla cambia por un solo partido.** Una etiqueta se convierte en propuesta de ajuste cuando se repite **5 veces o más**. Entonces el Científico de datos la prueba fuera de muestra con el histórico (como R3b, R5b o la X templada) y **solo entra si mejora** (log-loss o aciertos reales). El Auditor lo firma.
4. Los rojos por **varianza** no cambian nada: se suman a la prueba de calibración por tramos de P (se revisa con 30 casos o más).
5. Todo cambio aprobado se escribe en `analisis/reglas-mesa.md`, en `CLAUDE.md §3` y en la app (Novedades).

## 5. Prompt para Google (detalles de un partido terminado)

Se pega en Google (modo IA) o lo usa la mesa con el buscador. Uno por partido rojo; cambia lo que va entre corchetes.

```
Partido terminado: [LOCAL] – [VISITANTE], [COMPETICIÓN], [FECHA]. Resultado: [MARCADOR].

Busca y resume SOLO hechos comprobados de este partido. Usa fuentes oficiales (web de la competición o de los clubes), agencias y medios con datos concretos: UEFA, LaLiga, ESPN, BBC, Sky Sports, The Analyst (Opta), FotMob, Sofascore, Flashscore, AS, El País, Relevo, Gazzetta, Kicker. NO uses Marca, Sport, Mundo Deportivo ni L'Équipe. Nada de redes sociales ni foros.

Dame, en este orden y en español:
1. Goles: minuto, autor y cómo fue (jugada, córner, penalti, propia puerta).
2. xG de cada equipo y remates (totales y a puerta).
3. Expulsiones (minuto y motivo), penaltis (pitados, fallados, anulados) y decisiones del VAR.
4. Lesiones o cambios forzados durante el partido (minuto y jugador).
5. Alineaciones titulares y rotaciones: titulares habituales que empezaron en el banquillo o no jugaron, y por qué.
6. Bajas que ya había antes del partido.
7. Crónica en tres frases: quién dominó, qué decidió el resultado.

Para cada dato pon la fuente (nombre de la web). Si un dato no aparece, escribe «no consta». No inventes nada.
```

## 6. Primera autopsia: J24 (europea, 24-25/11)

Rojos de lo jugado (Reducida 1 + 32 sencillas): **4 empates y el Pleno**. Fuentes: The Analyst (Opta), Sky Sports, Flashscore, ESPN (clase B), leídas el 26/11.

| Partido | Real | P mesa / casas del signo real | Columnas con el signo | Lo que pasó | Clasificación |
|---|---|---|---|---|---|
| Arsenal – Dortmund | 1-1 (X) | 22 % / 20 % | 1 de 32 | Gyökeres 10', Beier 55'. xG 2,34 a 0,92; 30 remates, 4 a puerta. Raya se lesionó (entró Kepa, Sky) | Varianza |
| Man. City – Nápoles | 2-2 (X) | 17 % / 15 % | 0 de 32 | Højlund 55', Bouaddi 67', Lang 76', Cherki 85'. xG 1,41 a 0,61; 5 paradas de Milinković-Savić. City encaja primero en 7 de sus 10 últimos | Varianza |
| PSG – Roma | 2-2 (X) | 22 % / 20 % | 6 de 32 | Hermoso 5', Zabarnyi 31', dos penaltis (Dembélé y Malen, este tras VAR por mano de Vitinha). Roma con 6 cambios. xG no consta | Causa: `penalti_var` |
| Sporting – Man. United | 2-2 (X) | 23 % / 26 % | 5 de 32 | Dos penaltis y un gol en propia puerta (Kaique 82'); partido caótico (ESPN, sin crónica completa) | Causa: `penalti_var` (pendiente de completar con el prompt) |
| Pleno Atlético – Viking | 2-0 | 2-0: 7,1 % (M-1: 17,1 %) | 0 | Grimaldo y Julián en 25 minutos; penalti anulado por fuera de juego; Viking sin ocasiones claras y con 10 al final | Varianza |

**Lo que dice cada miembro (resumen):**
- **Matemático:** la mesa esperaba 2,3 empates en los 12 partidos de Champions y salieron 4. La P de 4 o más era del 18 % (casas, 17,5 %). No es un fallo raro del modelo.
- **Físico:** en Arsenal y City el favorito ganó el xG de largo (2,34-0,92 y 1,41-0,61). El precio era correcto; el empate fue de puntería.
- **Trader:** mesa y casas coincidían en los cuatro (diferencia ≤ 3 puntos). El mercado no vio nada que no viéramos.
- **Investigador:** no había bajas de clase A/B sin precio. La lesión de Raya fue durante el partido.
- **Risk Manager:** el problema es de **cobertura**: el empate de City no iba en ninguna columna y el de Arsenal en una. Con 4 X a la vez, la mejor columna se queda en 9-10.
- **Científico de datos:** primera entrada del registro. Hipótesis H1 (`cobertura_boleto`): con favoritos de 55-75 % en Champions, llevar la X en al menos tantas columnas como su P (City 17 % → 5 de 32). Se prueba cuando haya 5 casos y con el histórico europeo de LAE (`datos/lae_historico.json`).
- **Analista de Premios:** en una jornada con 4 X el premio de 13 y 14 es más alto; cubrir alguna X tiene más valor en premio que en aciertos.
- **Auditor:** datos de clase B comprobados en dos fuentes en Arsenal y City; Sporting – United pendiente de crónica completa. Ninguna regla cambia hoy.
- **Periodista deportivo:** dos de los cuatro empates llegaron con penaltis y VAR, algo que ningún modelo prevé. Los otros dos son mala puntería del favorito.

**Veredicto de la mesa:** 3 rojos de varianza y 2 con causa (`penalti_var`). Ninguna regla cambia hoy. Se abre la hipótesis H1 de cobertura de la X y se apunta todo en `datos/autopsias.json`. Celta y Crystal Palace (jueves) pasan por la autopsia si salen rojos.

### El Pleno, a fondo (J24 y lo que llevamos)

- **Lo que llevamos:** J19 fallado (0-2), J21 fallado (2-M), J22 fallado (2-M), **J23 acertado (1-1)**, J24 fallado (2-0); J20 sin registrar. Esperábamos unos 0,6 aciertos en 5 (la elección más probable ronda el 11-17 %) y llevamos 1. **No es mala suerte excepcional: el Pleno es difícil por naturaleza.** En el histórico LAE (609 jornadas), el marcador más repetido, 1-1, sale solo el 11,2 % de las veces.
- **Lo que sí sale medible (hipótesis H2, prioridad):** para Atlético – Viking la mesa daba al Atlético **3 goles o más en el 47 %** de los casos (M-0, M-1, M-2, M-M). En el histórico LAE de europeas con un grande en casa, el local mete 3 o más en el **32 %** (18 de 56). Si la mesa infla los goles del grande en casa, el Pleno se va a «M» cuando lo normal es 1-0, 2-0 o 2-1 (juntos, un 32 % con grande en casa). Se prueba la calibración de P(local ≥ 3) fuera de muestra **antes del Pleno de la J25**; solo cambia si mejora.
- **Por qué LAE eligió Atlético – Viking como Pleno:** es la pauta de LAE en semanas europeas: mete a los españoles y a los grandes, y pone a un grande en el Pleno en 8 de cada 14 jornadas. (dato de `lae-a-fondo.md`, clase A sobre el histórico; el porqué exacto de esta jornada no consta). Con un grande en casa, el histórico dice 2-1, 1-0 o M-1 por este orden.

### Revisión con Flashscore (Carlos, 26/11 21:46)

Carlos aportó resultado, xG, tarjetas, alineaciones y la crónica de Opta/AFP de los cuatro empates. Cambia lo siguiente:

| Partido | xG Flashscore | Lo nuevo | Clasificación |
|---|---|---|---|
| Arsenal – Dortmund | 2,83 a 1,15 | 6 titulares habituales en el banquillo (Eze, Merino, Saliba, Timber, Havertz, Calafiori); palo de Rice; gol del Dortmund anulado. **Raya era baja previa**, no se lesionó en el partido (corrige lo de Sky) | Varianza + `rotacion_favorito` |
| Man. City – Nápoles | 1,35 a 0,71 | Foden, Doku, Dias, Kovačić y Aït-Nouri suplentes; el Nápoles, con 8 bajas, marcó primero dos veces | Varianza + `rotacion_favorito` |
| PSG – Roma | **1,73 a 2,65 (más la Roma)** | Dembélé, Marquinhos y Zaire-Emery suplentes; dos penaltis | **Causa: `rival_superior_xg`** (antes `penalti_var`) |
| Sporting – Man. United | 2,52 a 1,08 | El Sporting, favorito de la mesa, mereció ganar; tres penaltis, dos goles anulados, roja a Tielemans | Varianza (`penalti_var`) |

- **Investigador:** las bajas previas (Raya, Saka, Doué, Kvaratskhelia, Lobotka, Šeško) ya estaban en `bajas_2411.json`: no hubo baja sin ver.
- **Matemático:** que empaten tres favoritos concretos tiene alrededor del 0,5 %, pero lo que cuenta es que salgan 4 X o más entre los 12, y eso tenía un **18 %**. Jornada dura, no imposible.
- **Hipótesis H3 (nueva, 3 casos):** favorito de Champions con 4 o más titulares en el banquillo. Solo sirve si hay un aviso de rotación antes del definitivo, porque las alineaciones salen 1 h antes.
- **H1 (cobertura de la X)** ya la cubre la regla **Seguro de favoritos** (26/11, `analisis/seguro-favoritos.md`).
- **Diferencias con el informe de Carlos:** la mesa daba al 1 un 60 % (Arsenal), 70 % (City) y 54 % (PSG); el 69/75/69 % se parece más a las casas. El Pleno jugado fue **M-1**, no M-0 (`jugado_real` de la J24).
