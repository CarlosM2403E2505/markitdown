"""Descarga y parseo de resultados de la UEFA Women's Champions League (fase liga) desde Wikipedia.

Fuente: en.wikipedia.org, subpáginas "..._league_phase" (wikitext, plantillas {{Football box}}).
Marcadores a 90' (Wikipedia da el resultado del tiempo reglamentario en la fase liga).
Escribe datos/champions_f.json. Uso: python3 modelo/champions_f_datos.py
"""
import json, os, re, urllib.request, ssl

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = "/tmp"
# nombre corto normalizado por club (para casar con la quiniela)
def corto(nombre):
    n = re.sub(r"\{\{[^}]*\}\}", "", nombre)            # quita {{fbaicon|GER}}
    n = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]+)\]\]", r"\1", n)  # [[A|B]] -> B, [[A]] -> A
    n = re.sub(r"\s*\(women\)|\s*W\.F\.C\.|\s*Women|\s*\(F\)|'+", "", n).strip()
    mapa = {"Bayern Munich": "Bayern", "Internazionale": "Inter Milan", "Inter Milan": "Inter Milan",
            "Paris Saint-Germain": "Paris Saint-Germain", "Olympique Lyonnais": "Lyon", "Lyon": "Lyon", "OL Lyonnes": "Lyon",
            "Manchester City": "Manchester City", "BK Häcken": "Häcken", "Häcken": "Häcken",
            "OH Leuven": "OH Leuven", "Oud-Heverlee Leuven": "OH Leuven", "Servette": "Servette", "Servette Chênois": "Servette",
            "AS Roma": "Roma", "Roma": "Roma", "SL Benfica": "Benfica", "Benfica": "Benfica",
            "Juventus": "Juventus", "Chelsea": "Chelsea", "Arsenal": "Arsenal", "Barcelona": "Barcelona",
            "Real Madrid": "Real Madrid", "VfL Wolfsburg": "Wolfsburg", "Wolfsburg": "Wolfsburg",
            "Twente": "Twente", "St. Pölten": "St. Pölten", "Vålerenga": "Vålerenga",
            "Atlético Madrid": "Atlético Madrid", "Austria Wien": "Austria Wien", "FK Austria Wien": "Austria Wien"}
    return mapa.get(n, n)


def parse(path, temporada):
    s = open(path, encoding="utf-8", errors="ignore").read()
    t1 = re.findall(r"\|\s*team1\s*=\s*(.+)", s)
    sc = re.findall(r"\|\s*score\s*=\s*(\d+)\s*[\u2013-]\s*(\d+)", s)
    t2 = re.findall(r"\|\s*team2\s*=\s*(.+)", s)
    out = []
    for a, (gl, gv), b in zip(t1, sc, t2):
        out.append({"temporada": temporada, "local": corto(a), "visitante": corto(b),
                    "goles_local": int(gl), "goles_visitante": int(gv)})
    return out


def main():
    part = []
    for season, tag in (("2026%E2%80%9327", "2026-27"), ("2025%E2%80%9326", "2025-26")):
        p = os.path.join(TMP, f"lp_{season}.txt")
        if os.path.exists(p):
            part += parse(p, tag)
    json.dump({"fuente": "en.wikipedia.org, '..._UEFA_Women's_Champions_League_league_phase' (wikitext), descargado 17/11/2026",
               "partidos": part}, open(os.path.join(R, "datos", "champions_f.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(part), "partidos ·", dict(Counter(x["temporada"] for x in part)))
    eq = sorted({x["local"] for x in part} | {x["visitante"] for x in part})
    print(len(eq), "equipos:", eq)


if __name__ == "__main__":
    main()
