"""Genera la página «Pronósticos definitivos» (artefacto del proyecto) a partir del JSON de una jornada.

Solo dos tablas, sin explicaciones: el boleto de 18 € y las sencillas.

Uso:
    python3 pronosticos_definitivos.py jornadas/j23/j23.json salida.html --estado provisional --hora "vie 20/11 16:30"
    python3 pronosticos_definitivos.py jornadas/j23/j23.json salida.html --estado definitivo --hora "sáb 21/11 10:30"

Las sencillas son `columnas_individuales` más `columna_novena` si existe.
Criterio de publicación: el definitivo se publica 2 h 15 min antes del primer partido.
"""
import argparse
import html
import json

CSS = """
<title>Pronósticos definitivos</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;500;600&display=swap">
<style>
/* Layout: dos hojas de boleto apiladas, cuadrícula 1·X·2 como en el impreso de la Quiniela */
:root{
  --bg:#f3f5f2; --paper:#ffffff; --ink:#1b2420; --muted:#5f6b65; --line:#d5dcd7;
  --mark:#c8102e; --mark-ink:#ffffff; --cell:#eef2ef; --prov:#b26b00; --prov-bg:#fff3dc; --def:#1d7a46; --def-bg:#e2f4e9;
  --f-display:"Barlow Condensed","Arial Narrow",system-ui,sans-serif; --f-body:"Inter",system-ui,-apple-system,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#121614; --paper:#1a201d; --ink:#e7ece9; --muted:#9aa6a0; --line:#2f3833;
  --mark:#e0364f; --mark-ink:#ffffff; --cell:#232b27; --prov:#f0b34a; --prov-bg:#3a2c12; --def:#5cc98a; --def-bg:#163525; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#121614; --paper:#1a201d; --ink:#e7ece9; --muted:#9aa6a0; --line:#2f3833;
  --mark:#e0364f; --mark-ink:#ffffff; --cell:#232b27; --prov:#f0b34a; --prov-bg:#3a2c12; --def:#5cc98a; --def-bg:#163525; color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:14px}
.wrap{max-width:860px;margin:0 auto;padding-block:20px 40px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:20px}
header{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 14px}
h1{font-family:var(--f-display);font-size:30px;font-weight:700;margin:0;letter-spacing:.01em;text-wrap:balance}
.meta{color:var(--muted);font-size:13px}
.pill{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:3px 10px;border-radius:999px}
.pill.provisional{color:var(--prov);background:var(--prov-bg)}
.pill.definitivo{color:var(--def);background:var(--def-bg)}
section{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 0 6px;min-width:0}
h2{font-family:var(--f-display);font-size:20px;font-weight:600;margin:0 14px 10px;letter-spacing:.02em}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
th,td{padding:6px 8px;border-top:1px solid var(--line);text-align:center;white-space:nowrap}
thead th{border-top:none;font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
td.n{color:var(--muted);width:28px}
td.p,th.p{text-align:left;white-space:normal;min-width:150px}
.box{display:inline-grid;place-items:center;width:28px;height:26px;border-radius:5px;background:var(--cell);color:var(--muted);font-weight:600;font-family:var(--f-display);font-size:16px}
.box.on{background:var(--mark);color:var(--mark-ink)}
.sg{font-family:var(--f-display);font-size:17px;font-weight:600}
tr.pleno td{border-top:2px solid var(--ink)}
.score{font-family:var(--f-display);font-size:18px;font-weight:700;color:var(--mark)}
th.grp{border-left:2px solid var(--line)}
td.c9,th.c9{border-left:2px solid var(--line)}
</style>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("salida")
    ap.add_argument("--estado", choices=["provisional", "definitivo"], required=True)
    ap.add_argument("--hora", required=True, help="hora peninsular de la versión, p. ej. 'sáb 21/11 10:30'")
    a = ap.parse_args()

    d = json.load(open(a.json, encoding="utf-8"))
    e = html.escape
    partidos = {p["n"]: p["partido"] for p in d["partidos"]}
    pleno = d["pleno"]
    boleto = d["boleto_provisional"]
    cols = list(d["columnas_individuales"])
    if d.get("columna_novena"):
        cols.append(d["columna_novena"])
    n_bol1 = min(8, len(cols))

    out = [CSS, '<div class="wrap">']
    out.append(
        f'<header><h1>Jornada {d["jornada"]} · {e(d["fechas"])}</h1>'
        f'<span class="pill {a.estado}">{a.estado}</span>'
        f'<span class="meta">Actualizado {e(a.hora)} (hora peninsular)</span></header>'
    )

    # Tabla 1: boleto de 18 €
    out.append(f'<section><h2>Boleto {e(boleto["tipo"].lower())} · {boleto["apuestas"]} apuestas · {boleto["coste"]:.0f} €</h2><div class="scroll"><table>')
    out.append('<thead><tr><th>Nº</th><th class="p">Partido</th><th>1</th><th>X</th><th>2</th></tr></thead><tbody>')
    for n in range(1, 15):
        s = boleto["signos"][str(n)].split()
        cells = "".join(f'<td><span class="box{" on" if x in s else ""}">{x}</span></td>' for x in "1X2")
        out.append(f'<tr><td class="n">{n}</td><td class="p">{e(partidos[n])}</td>{cells}</tr>')
    out.append(f'<tr class="pleno"><td class="n">P15</td><td class="p">{e(pleno["partido"])}</td><td colspan="3"><span class="score">{e(boleto["pleno"])}</span></td></tr>')
    out.append("</tbody></table></div></section>")

    # Tabla 2: sencillas
    coste = len(cols) * 0.75
    out.append(f'<section><h2>Sencillas · {len(cols)} apuestas · {coste:.2f} €'.replace(".", ",") + "</h2><div class=\"scroll\"><table>")
    head = '<thead>'
    if len(cols) > n_bol1:
        head += f'<tr><th></th><th class="p"></th><th colspan="{n_bol1}">Boleto 1</th><th class="grp" colspan="{len(cols) - n_bol1}">Boleto 2</th></tr>'
    head += '<tr><th>Nº</th><th class="p">Partido</th>' + "".join(
        f'<th{" class=\"c9\"" if i == n_bol1 else ""}>C{i + 1}</th>' for i in range(len(cols))) + "</tr></thead><tbody>"
    out.append(head)
    for n in range(1, 15):
        cells = "".join(f'<td class="sg{" c9" if i == n_bol1 else ""}">{c[n - 1]}</td>' for i, c in enumerate(cols))
        out.append(f'<tr><td class="n">{n}</td><td class="p">{e(partidos[n])}</td>{cells}</tr>')
    cells = "".join(f'<td class="{"c9" if i == n_bol1 else ""}"><span class="score">{e(boleto["pleno"])}</span></td>' for i in range(len(cols)))
    out.append(f'<tr class="pleno"><td class="n">P15</td><td class="p">{e(pleno["partido"])}</td>{cells}</tr>')
    out.append("</tbody></table></div></section></div>")

    open(a.salida, "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    main()
