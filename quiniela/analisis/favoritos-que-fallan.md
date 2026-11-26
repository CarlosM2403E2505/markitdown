# ¿Por qué falla un favorito claro? (caso Rayo, J23) · 22/11/2026

`modelo/favoritos_fallan.py`: 877 partidos de Primera y Segunda (julio de 2024 a noviembre de 2026) en los que la mesa daba al favorito entre el 45 y el 70 % (cuota de 1,45 a 2,20), con probabilidades fuera de muestra. Se separa la selección (2024-25) de la validación (2025-27). Football-data.co.uk está bloqueado desde el contenedor, así que la prueba usa los resultados que ya tiene la mesa.

| Situación del favorito | 2024-25: daba / ganó | 2025-27: daba / ganó | X que salió frente a la dada | ¿Se repite? |
|---|---|---|---|---|
| Todos (local) | 53 / 54 | 52 / 53 | 25→28 · 25→24 | Calibrado |
| Jugó en Europa hace 4 días o menos | 57 / 46 | 58 / 63 | — | No (cambia de signo) |
| Juega en Europa en 4 días o menos | 55 / 52 | 57 / 68 | — | No |
| Europeo contra no europeo (EURO_F) | 55 / 55 | 58 / 62 | — | Calibrado |
| **Mala forma (5 puntos de 15 o menos)** | **50 / 49** | **51 / 46** | **26→30 · 26→29** | **Sí, en las dos mitades (débil: z −0,2 y −1,3)** |
| Rival en buena forma (10 de 15 o más) | 52 / 40 | 53 / 54 | 25→38 · 24→21 | No |

**Conclusión:**
- Con el modelo actual, que ya lleva la X templada, el favorito de entre el 45 y el 70 % **gana lo que la mesa dice**: daba un 53 % y ganó un 53-54 %. Un favorito del 54 % pierde o empata 46 veces de cada 100. Eso no es un error: es lo que significa ese porcentaje.
- Ni Europa entre semana ni la forma del rival separan de verdad: lo que sale en una mitad no se repite en la otra.
- La única señal que se repite en las dos mitades es que **el favorito llegue en mala forma**: gana menos y empata más. El **Rayo llegaba así**, con 5 puntos de 15 (1, 1, 0, 3 y 0).
- La señal es débil, así que **no cambia la probabilidad**. Solo obliga a cubrir más ese partido.

**Regla codificada** (`reglas_mesa.py`, R3): si el favorito tiene menos del 70 % y llega con 5 puntos o menos en sus 5 últimos partidos de liga (campo `forma_favorito`), se le aplica el tope del tramo de abajo. Con el Rayo (54 %), el 1 habría ido como mucho en el 60 % de las columnas, no en el 75 %. Tests en `herramientas/test_reglas_mesa.py`.
