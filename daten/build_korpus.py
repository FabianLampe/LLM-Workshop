"""Phase 1 — Korpus von der Bundesagentur-Jobboerse-API ziehen.

Standalone-Variante des Codes aus notebooks/01_explore.ipynb. Schreibt nach
daten/eigener_korpus.jsonl. Nach dem Lauf das Notebook ueber dieselbe Datei
inspizieren.
"""

import base64
import json
import time
from pathlib import Path

import requests

API_BASE = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service"
HEADERS = {"X-API-Key": "jobboerse-jobsuche"}

KORPUS_PATH = Path(__file__).parent / "eigener_korpus.jsonl"

SUCHANFRAGEN = [
    {"was": "Fachinformatiker Daten- und Prozessanalyse", "size": 25},
    {"was": "Data Scientist", "size": 20},
    {"was": "Datenanalyst", "size": 20},
    {"was": "Business Intelligence", "size": 15},
    {"was": "Data Engineer", "size": 15},
]


def search(was: str, wo: str | None = None, size: int = 50, page: int = 1) -> dict:
    params = {"was": was, "page": page, "size": size}
    if wo:
        params["wo"] = wo
    r = requests.get(f"{API_BASE}/pc/v4/jobs", params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()


def detail(refnr: str) -> dict:
    hash_id = base64.b64encode(refnr.encode("utf-8")).decode("ascii").rstrip("=")
    r = requests.get(f"{API_BASE}/pc/v4/jobdetails/{hash_id}", headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()


def extrahiere_treffer(such_response: dict, suchbegriff: str) -> list[dict]:
    out = []
    for st in such_response.get("stellenangebote", []):
        out.append({
            "refnr": st.get("refnr"),
            "titel": st.get("titel") or st.get("beruf"),
            "firma": st.get("arbeitgeber"),
            "ort": (st.get("arbeitsort") or {}).get("ort"),
            "plz": (st.get("arbeitsort") or {}).get("plz"),
            "region": (st.get("arbeitsort") or {}).get("region"),
            "eintrittsdatum": st.get("eintrittsdatum"),
            "aktuelleVeroeffentlichungsdatum": st.get("aktuelleVeroeffentlichungsdatum"),
            "externeUrl": st.get("externeUrl"),
            "hashId": st.get("hashId"),
            "_suchbegriff": suchbegriff,
        })
    return out


def reichere_mit_text_an(eintrag: dict, sleep: float = 0.4) -> dict:
    try:
        d = detail(eintrag["refnr"])
    except requests.HTTPError as e:
        eintrag["text"] = ""
        eintrag["_detail_fehler"] = str(e)
        return eintrag
    eintrag["text"] = d.get("stellenbeschreibung") or ""
    eintrag["arbeitgeberdarstellung"] = d.get("arbeitgeberdarstellung")
    eintrag["branchengruppe"] = d.get("branchengruppe")
    eintrag["branche"] = d.get("branche")
    eintrag["arbeitszeitmodelle"] = d.get("arbeitszeitmodelle")
    eintrag["befristung"] = d.get("befristung")
    time.sleep(sleep)
    return eintrag


def main() -> None:
    treffer_roh: list[dict] = []
    for q in SUCHANFRAGEN:
        try:
            resp = search(was=q["was"], size=q["size"])
        except requests.HTTPError as e:
            print(f"  '{q['was']}': FEHLER {e}")
            continue
        n_max = resp.get("maxErgebnisse", 0)
        treffer = extrahiere_treffer(resp, q["was"])
        print(f"  '{q['was']}': {len(treffer)} Treffer (von {n_max} verfuegbar)")
        treffer_roh.extend(treffer)
        time.sleep(0.5)

    print(f"\nGesamt vor Dedup: {len(treffer_roh)}")

    gesehen: set[str] = set()
    treffer_dedup: list[dict] = []
    for t in treffer_roh:
        if not t["refnr"] or t["refnr"] in gesehen:
            continue
        gesehen.add(t["refnr"])
        treffer_dedup.append(t)
    print(f"Nach Dedup: {len(treffer_dedup)}")

    korpus: list[dict] = []
    for i, t in enumerate(treffer_dedup, 1):
        korpus.append(reichere_mit_text_an(t))
        if i % 10 == 0:
            print(f"  {i}/{len(treffer_dedup)} Detail-Anzeigen geladen")

    n_leer = sum(1 for k in korpus if not k.get("text"))
    print(f"\nFertig: {len(korpus)} Anzeigen, davon {n_leer} ohne Beschreibungstext.")
    korpus = [k for k in korpus if k.get("text")]
    print(f"Nach Text-Filter: {len(korpus)} Anzeigen.")

    with KORPUS_PATH.open("w", encoding="utf-8") as f:
        for eintrag in korpus:
            f.write(json.dumps(eintrag, ensure_ascii=False) + "\n")
    print(f"\n{len(korpus)} Anzeigen geschrieben nach {KORPUS_PATH}")


if __name__ == "__main__":
    main()
