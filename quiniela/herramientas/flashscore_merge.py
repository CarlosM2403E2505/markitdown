#!/usr/bin/env python3
"""Añade a datos/euro_jNN.json los resultados leídos en Flashscore.es (Claude in Chrome, 22/11/2026).
Entrada: carpeta con <liga>.txt (fecha|local|visitante|gl|gv separados por ';'). Nombres de Flashscore → dataset.
Sin duplicados: un partido ya presente (mismos equipos y marcador, ±3 días) no se añade.
Uso: python3 herramientas/flashscore_merge.py datos/euro_j23.json carpeta datos/euro_j24.json"""
import json, os, sys, glob, unicodedata
from datetime import date
MAP = {
 "Brighton": "brighton hove albion", "Coventry": "coventry city", "Hull": "hull city", "Ipswich": "ipswich town",
 "Leeds Utd": "leeds united", "Manchester City": "man city", "Manchester Utd": "man united",
 "Augsburgo": "augsburg", "Bayer Leverkusen": "leverkusen", "Bayern Múnich": "bayern", "Borussia Dortmund": "dortmund",
 "Borussia M'gladbach": "borussia monchengladbach", "Colonia": "koln", "Eintracht Fráncfort": "frankfurt",
 "Friburgo": "freiburg", "Hamburgo": "hamburger", "Mainz": "fsv mainz", "RB Leipzig": "leipzig",
 "AC Milan": "milan", "Bolonia": "bologna", "Nápoles": "napoli",
 "Angers": "angers sco", "Brest": "stade brestois", "Stade Rennais": "rennes", "Estrasburgo": "strasbourg alsace",
 "Marsella": "marseille", "Niza": "nice", "Paris FC": "paris", "Troyes": "es troyes", "Mónaco": "monaco",
 "Cambuur": "cambuur leeuwarden", "Den Haag": "ado den haag", "Excelsior": "sbv excelsior", "G.A. Eagles": "go ahead eagles",
 "Nijmegen": "nec", "Sittard": "fortuna sittard", "Willem II": "willem ii tilburg", "Zwolle": "pec zwolle", "AZ Alkmaar": "az alkmaar",
 "Estoril": "gd estoril praia", "Estrela": "estrela da amadora", "Marítimo": "cs maritimo", "Oporto": "porto", "SC Braga": "braga",
 "Vitória Guimaraes": "vitoria guimaraes",
 "Brno": "zbrojovka brno", "Liberec": "slovan liberec", "Ostrava": "banik ostrava", "Plzen": "viktoria plzen",
 "Slavia Praga": "slavia praha", "Sparta Praga": "sparta praha", "Zlin": "fastav zlin",
 "Antwerp": "royal antwerp", "Beveren": "waasland beveren", "Charleroi": "sporting charleroi", "Club Brujas": "brugge",
 "Círculo Brujas": "cercle brugge", "KV Mechelen": "mechelen", "Leuven": "oud heverlee leuven", "Lommel SK": "lommel",
 "RAAL La Louviere": "raal louviere", "Royale Union SG": "union sg", "St. Lieja": "standard liege",
 "St. Truiden": "sint truidense vv", "Waregem": "zulte waregem", "Westerlo": "kvc westerlo",
 "Amedspor": "amed", "Başakşehir": "istanbul basaksehir", "Erzurumspor": "bb erzurumspor", "Rizespor": "caykur rizespor",
 "Banska Bystrica": "dukla banska bystrica", "Dun. Streda": "dac", "Komarno": "kfc komarno", "Michalovce": "mfk zemplin michalovce",
 "Podbrezova": "zeleziarne podbrezova", "Ruzomberok": "mfk ruzomberok", "Skalica": "mfk skalica", "Trnava": "spartak trnava",
 "Zilina": "msk zilina",
 "Araz": "araz naxc van pfk", "Kapaz": "kapaz pfk", "Neftci Baku": "neftci pfk", "Sabah FC": "sabah", "Shamakhi": "samax",
 "Sumqayit": "sumgay t", "Turan": "turan tovuz", "Gabala": "gabala", "Imisli FK": "imisli", "Safa Baku": "safa baku",
 "Ch. Odesa": "chernomorets odessa", "Kryvbas": "kryvbas kryvyi rih", "Livyi Bereg": "livyi bereh", "Veres-Rivne": "veres",
 "Zorya": "zorya lugansk", "Epitsentr": "epitsentr", "FC Kharkiv": "fc kharkiv", "Kudrivka": "kudrivka", "Bukovyna": "bukovyna",
 "Aalesund": "aalesunds", "Bodo/Glimt": "bodo glimt", "HamKam": "hamarkameratene", "Sandefjord": "sandefjord fotball",
 "Sarpsborg 08": "sarpsborg", "Tromsø": "tromso il",
 "Alavés": "deportivo alaves", "Athletic Club": "athletic bilbao", "Atlético de Madrid": "atletico", "Celta de Vigo": "celta",
 "Deportivo de A Coruña": "deportivo coruna", "Espanyol": "espanyol barcelona", "R. Racing Club": "racing santander",
 "Real Betis": "betis",
}
TEMP = {"no.1": "2026"}
def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().replace(".", "").strip()
def main(src, carpeta, dst):
    d = json.load(open(src, encoding="utf-8")); ms = d["matches"]
    ya = {}
    for m in ms: ya.setdefault((m["home"], m["away"], m["hg"], m["ag"]), []).append(date.fromisoformat(m["date"]))
    nuevos = 0; por = {}
    for f in sorted(glob.glob(os.path.join(carpeta, "*.txt"))):
        lg = os.path.basename(f)[:-4]
        for r in open(f, encoding="utf-8").read().strip().split(";"):
            fe, h, a, hg, ag = r.split("|"); h = MAP.get(h, norm(h)); a = MAP.get(a, norm(a)); hg, ag = int(hg), int(ag)
            k = (h, a, hg, ag)
            if any(abs((date.fromisoformat(fe) - x).days) <= 3 for x in ya.get(k, [])): continue
            ms.append({"home": h, "away": a, "date": fe, "hg": hg, "ag": ag, "competition": f"{lg}:{TEMP.get(lg, '2026-27')}", "fuente": "flashscore.es (22/11/2026)"})
            ya.setdefault(k, []).append(date.fromisoformat(fe)); nuevos += 1; por[lg] = por.get(lg, 0) + 1
    ms.sort(key=lambda m: m["date"])
    json.dump(d, open(dst, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"{nuevos} partidos nuevos:", por, "| total", len(ms))
if __name__ == "__main__":
    main(*sys.argv[1:4])
