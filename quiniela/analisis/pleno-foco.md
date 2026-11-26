# Foco en el Pleno al 15 (método estable de la mesa)

El objetivo final del proyecto es el Pleno. Esta es la verdad honesta y el método con el que la mesa trabaja por él.

## La verdad
- **El Pleno es un solo partido con marcador exacto** (16 categorías: 0-0, 0-1, 0-2, 0-M, 1-0 … M-M). El resultado más probable de un partido ronda el **11-13 %**. Nadie acierta el marcador exacto de forma fiable.
- **Nuestro registro hasta hoy** (`datos/pleno_registro.json`): J19 fallado (0-2), J21 fallado (España perdió), J20 sin registrar, J22 pendiente. **No hemos acertado ninguno de los verificables.** Es lo normal, no un fallo del método.
- Por eso el dinero se juega en los 14 signos; el Pleno es la guinda. **Nunca se persigue** (ni más gasto, ni combinadas).

## Qué SÍ hace la mesa por el Pleno
1. **El mejor modelo para ese partido concreto:** clubes (Primera T=1,15), selecciones (modelo validado) o Champions femenina, según toque.
2. **Elegir el marcador más probable del modelo** (fase del Pleno), y mostrar el top-5 con su probabilidad.
3. **Valor frente al público** (informativo): se estima cuánto juega el público cada marcador (con los % de goles de LAE) para ver cuáles pagan más si aciertas. No cambia la elección (anexo H), pero se informa.
4. **Registrar y aprender:** cada jornada se anota la elección y el resultado en `pleno_registro.json`. Con suficientes jornadas se medirá si acertamos el Pleno por encima del azar.

## Regla
- Pleno = **marcador más probable del modelo**. Si dos están a menos de 0,5 puntos, se informa de los dos y se elige el de más valor frente al público, dejándolo escrito.
