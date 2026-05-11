# Make-or-Buy-Memo — Frontier-LLM-Annotation der restlichen 78 Anzeigen

**Adressat:** Projektleitung FIDP-Pipeline
**Empfehlung:** _[Make / Buy / Hybrid]_ — _einzeiliger Kern-Satz_
**Datum:** _YYYY-MM-DD_

---

## 1. Empfehlung

_z. B.: „Hybrid — Frontier annotiert alle 78 Anzeigen vollautomatisch, ich reviewe stichprobenartig 15 Anzeigen (≈20 %), gezielt auf den Feldern mit κ < 0.6."_

## 2. Begründung an meinen κ-Werten

| Feld | κ (Mensch ↔ Frontier, n=12) | Frontier-Vertrauen | Empfehlung pro Feld |
|---|---|---|---|
| `homeoffice` | _0.xx_ | _Stufe (hoch/moderat/niedrig)_ | _Frontier / Mensch / Hybrid_ |
| `vertragsart` | _0.xx_ | _ | _ |
| `erfahrungslevel` | _0.xx_ | _ | _ |
| `gehalt_min_eur` | _Stichprobe_ | _ | _ |
| `skills_top3` | _Stichprobe_ | _ | _ |

_Kommentar zur Tabelle: 2–3 Sätze, was die κ-Werte konkret bedeuten — wo Frontier-Output direkt nutzbar ist, wo Review nötig._

## 3. Schwellwert-Logik

_Konkret: ab welchem κ-Wert akzeptiere ich Frontier ohne Review? Wo liegt meine Schwelle?_

_z. B.: „Für unkritische Reporting-Aggregate (Skill-Häufigkeiten) reicht κ ≥ 0.6. Für Recruiting-Filter (Homeoffice, Erfahrungslevel) brauche ich κ ≥ 0.75 — sonst Mensch-Review."_

_Was müsste anders sein, damit ich anders entscheide?_

_z. B.: „Wenn n > 50 (statt 12) und die κ-Werte stabil bleiben, würde ich auch bei 0.55 Frontier alleine zulassen — bei n=12 sind die κ-Werte zu volatil (eine Anzeige Differenz ≈ 8 Pt)."_

## 4. Risiko-Sicherung

Falls meine Empfehlung falsch liegt, was geht schief?

_z. B.: „Wenn Frontier auf `homeoffice` systematisch zu großzügig ist (alles wird `teilweise`), dann ist mein Recruiting-Filter unzuverlässig — Kandidat:innen filtern die Stellen nach 'remote' und finden zu viel Müll."_

**Stichproben-Kontrolle:**
- _z. B. „Jede 5. Frontier-Annotation manuell reviewen → 16 von 78 Anzeigen. Bei > 2 Korrekturen pro 16 → systematisches Problem, Pipeline pausieren und neu prompt-tunen."_

**Validator-Schritt:**
- _„`python annotation/validate.py annotation/frontier_gold_full.csv` zwingend vor Persistenz — Schema-Verletzungen blocken den Import in die Reporting-DB."_

## 5. Was ich aus Phase 5 gelernt habe

_2–3 Sätze: was war das überraschendste Disagreement? Welche Schema-Lücke hat Frontier sichtbar gemacht? Wo war ich selbst unsicher und Frontier hat mir geholfen, das Schema schärfer zu lesen?_

---

_Quellen: `notebooks/04_frontier_compare.ipynb` (κ-Tabelle, Disagreement-Liste), `annotation/meine_gold.csv`, `annotation/frontier_gold.csv`._
