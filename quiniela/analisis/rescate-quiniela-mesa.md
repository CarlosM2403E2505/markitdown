# Rescate de «quiniela-mesa» (11/11/2026): qué se incorpora y con qué pruebas

Cada profesional ha revisado lo suyo. **Solo se aplica lo que mejora fuera de muestra.**

## 1. Analista de selecciones + Auditor: **se cambia el modelo de selecciones**

`modelo/validacion_selecciones.py`. Partidos oficiales entre selecciones UEFA, resultado a 90':
- validación: 576 partidos (de 01/2022 a 10/2024);
- prueba: 400 partidos (de 11/2024 a 10/2026).

| Modelo | Factor de empates elegido | Log-loss en validación | **Log-loss en prueba** | X prevista en prueba |
|---|---|---|---|---|
| Elo + Poisson de 2,4 goles (nuestro, hasta la v1.6) | 0,9 | 0,903 | **0,810** (0,811 con el 0,9) | 19,8 % |
| **Poisson de selecciones (de quiniela-mesa)** | **1,0** | 0,872 | **0,795** | 21,1 % |
| Tasa base | — | — | 1,062 | — |

En la prueba hubo un 21,8 % de empates reales.

- **Gana el Poisson de selecciones.** Además, no hace falta factor de empates: el ×1,17 que usaba quiniela-mesa no está respaldado (con 1,0 la prueba sale mejor).
- **Pleno con selecciones** (`modelo/validacion_pleno_selecciones.py`): mezclar con la distribución histórica de marcadores no mejora la prueba (log-loss 2,356 sin mezcla, 2,368 con un 10 % de mezcla). Se usa el Poisson puro.
- **Datos:** martj42 hasta el 6/10/2026, con las dos ventanas de septiembre y octubre de la Nations League. Comprobados con la prensa: España 4 de 4, Inglaterra 3-0 Chequia, Francia 4-1 Bélgica e Italia 3-1 Turquía.

## 2. Pleno Specialist

- **España–Inglaterra:** pasa de 69/21/10 (Elo) a **52,7 / 24,6 / 22,6**.
- **Marcadores:** 1-0 11,9 %, **1-1 11,7 %**, 2-0 9,8 %, 2-1 9,6 % y M-0 8,5 %.
- **1-0 y 1-1 están a 0,2 puntos:** el sábado se elige el que menos juegue el público (regla de la fase 7).
- **La tabla histórica de los 498 plenos** (1-1 12,2 %, 1-0 11,0 %) apunta en la misma dirección.

## 3. Actuario

- **Registro de premios:** se añaden la J13 (europea, sin acertantes de 14) y la J14 de 2026/27 (`datos/premios.json`).
- **Hallazgo:** el valor esperado calculado con premios medios no es válido. Con la J13 daba 37,75 € por 12 €, imposible, porque los premios altos salen en las jornadas raras, justo cuando nuestras columnas aciertan menos.
  - Se retira de la calculadora.
  - Queda el dato honesto: **la Quiniela devuelve de media unos 0,55 € por euro jugado**.
  - **Corrección:** los «0,77 € por euro» dichos antes eran de este método equivocado.

## 4. Estadístico de calibración: Liga F

- Sus 79 partidos de la Liga F 2026/27 son **idénticos** a los nuestros: juntarlos no añade muestra.
- Su «k = 1,12» sale de un modelo distinto. Con el nuestro, la prueba de esta mañana (54 partidos) deja el 0,85 y el 0,90 empatados. **Se mantiene el 0,85.**

## 5. Data Analyst + Auditor: base de datos de clubes

- 23.672 partidos suyos frente a 23.671 nuestros. Ningún marcador común distinto.
- **Añadidos 4 partidos que nos faltaban**, comprobados en prensa y en laliga.com:
  - **Tenerife 2-2 Andorra** (2/11; afecta a los partidos 3 y 6);
  - Shakhtar 0-1 Sporting, Galatasaray 2-0 Stuttgart y Feyenoord 0-3 Inter (3/11).
- **Efecto en los precios de la J21:** menos de 0,3 puntos.
- **Sin comprobar todavía, no añadidos:** Sevilla 0-0 Alavés (6/11), Espanyol 0-0 Deportivo (7/11) y LASK 4-0 Slovan.
- **Nuestro Lens 1-9 Como** (4/11), que parecía un error, **es real** (Reuters).

## 6. Director, Contexto y Calendario: estudios ya medidos que se adoptan como reglas de aviso

- **Cambio de entrenador:** 49 destituciones. Antes del cese, −0,60 puntos por partido sobre lo esperado; después, +0,03 (IC −0,12 a +0,19). Es regresión a la media: **solo aviso.** Afecta en la J21 al Oviedo (Raúl González) y al Ceuta (Lobera).
- **Enfrentamientos directos:** sin mejora (0,0002 de log-loss). **Solo aviso.**
- **Árbitros:** no medibles para el 1X2.
- **Histórico de Loterías (2019–2026, 498 jornadas):**
  - signos 44 / 25 / 30;
  - media de 3,55 X por jornada;
  - P(0 X) = 2,2 % (nuestro modelo da un 2,0 % en la J21: coherente).
- **Patrones de selección de Loterías:** el día del partido decide; reparto fijo por competición; en el parón, 10 de Segunda + 4 de Liga F + el Pleno de España.
- **Pendiente de probar** en su jornada, porque en la J21 no hay Primera:
  - su factor de empates en partidos igualados de Primera (×1,20, 189 partidos);
  - su ajuste por haber jugado Europa (EURO_F 1,12, 3.434 partidos).
  Se probarán con el mismo método antes de usarlos.

## Lo que no se incorpora

- **El veto «favorito que viene de perder en Europa nunca va de sencillo»:** el usuario lo retiró el 3/11.
- **Sus empates de Segunda a ×1,08:** su propio estudio da un k de 0,93, y nosotros usamos 1,00.
- **Su Liga F antigua.**
- **Las cuotas dentro del modelo:** el usuario lo prohíbe.
