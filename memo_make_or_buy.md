# Make-or-Buy-Memo — Frontier-LLM-Annotation der restlichen 78 Anzeigen

**Adressat:** Projektleitung FIDP-Pipeline
**Empfehlung:** **Hybrid** — ChatGPT annotiert alle 78 Anzeigen vollautomatisch; ich reviewe gezielt nur die zwei Felder mit κ < 0.6 (`homeoffice`, `erfahrungslevel`), nicht das ganze Schema.
**Datum:** 2026-06-04

---

## 1. Empfehlung

Hybrid mit feld-spezifischer Aufteilung, **nicht** pauschal "Frontier macht alles" oder "Mensch macht alles". Der Frontier-Lauf ist billig und schnell (12 Anzeigen in einem Chat-Turn → 78 in ~4 Turns), also lasse ich ihn den kompletten ersten Durchlauf über alle 6 Felder machen. Das menschliche Review konzentriere ich auf die zwei Felder, bei denen mein κ unter der Vertrauensschwelle liegt — statt alle 78 × 6 Felder von Hand nachzukontrollieren, nur 78 × 2. Das spart ~⅔ des Hand-Aufwands und schützt trotzdem die schwachen Felder.

**Annotator-Wahl: ChatGPT, nicht Claude.** ChatGPT hatte auf beiden strittigen Feldern das höhere κ (`homeoffice` 0.507 vs. 0.385, `erfahrungslevel` 0.526 vs. 0.363). Claude untertreibt `erfahrungslevel` systematisch auf `nicht_genannt`, wo ChatGPT und ich `mid` hatten (refnr `13644-307612-S`, `12265-489382_JB5131539-S`, `14036-0005680f46a001-S`).

## 2. Begründung an meinen κ-Werten

| Feld | κ (ich ↔ ChatGPT, n=12) | Frontier-Vertrauen | Empfehlung pro Feld |
|---|---|---|---|
| `vertragsart` | **1.0** (12/12) | hoch | **Frontier allein**, kein Review |
| `erfahrungslevel` | 0.526 (9/12) | moderat | Frontier + Mensch-Review dieses Felds |
| `homeoffice` | 0.507 (9/12) | moderat–niedrig | Frontier + Mensch-Review dieses Felds |
| `gehalt_min_eur` | Stichprobe (selten belegt) | niedrig | Frontier als Vorschlag, Stichprobe |
| `skills_top3` | Stichprobe (Set-Match subjektiv) | moderat | Frontier für Aggregate, kein Per-Ad-Review |

**Kommentar:** `vertragsart` ist direkt nutzbar — κ=1.0 bei *beiden* Modellen, das Feld kommt sauber aus dem strukturierten API-Feld plus Text. Bei `homeoffice` und `erfahrungslevel` liegt das Frontier im *moderaten* Bereich (Landis & Koch), und der Fehler ist nicht zufällig, sondern **gerichtet**: das Frontier setzt zu oft `nicht_genannt`. Bei `homeoffice` sagten ChatGPT *und* Claude `nicht_genannt`, wo ich `ja`/`teilweise` hatte (`16724-0062809539-S`, `18896-8565435-S`) — die Anzeige nennt Homeoffice nur als Benefit-Stichwort, das Frontier liest das strenger als ich. `gehalt_min_eur` traf das Frontier in 0 von 1 belegten Fällen (`11949-17196786-S`: Gold 55000, beide Modelle leer) — bei so dünner Belegung ist κ nicht aussagekräftig, daher Stichprobe statt κ-Entscheid.

## 3. Schwellwert-Logik

Meine Schwellen, gestaffelt nach Nutzung des Felds:

- **κ ≥ 0.8 → Frontier ohne Review** (nur `vertragsart` erfüllt das).
- **0.6 ≤ κ < 0.8 → Frontier + 20 %-Stichprobe.**
- **κ < 0.6 → Mensch-Review dieses Felds auf allen 78** — `homeoffice` (0.507) und `erfahrungslevel` (0.526) fallen hierunter.

Für **Recruiting-Filter** (Kandidat:in filtert "nur Remote", "nur Senior") ziehe ich die Latte auf κ ≥ 0.75, weil ein falsch gesetztes Feld direkt die Trefferliste verfälscht. Für **Reporting-Aggregate** (Skill-Häufigkeit über alle Anzeigen) reicht κ ≥ 0.6, weil sich gerichtete Einzelfehler über 78 Anzeigen teilweise rausmitteln.

**Was müsste anders sein, damit ich anders entscheide?** Bei n=12 ist eine einzige abweichende Anzeige ≈ 8,3 Pt κ — die Werte sind volatil. Würde ich auf n > 50 kalibrieren und `homeoffice`/`erfahrungslevel` blieben stabil über 0.6, würde ich auch dort von Vollreview auf 20 %-Stichprobe runtergehen. Bei n=12 traue ich der Stabilität nicht genug, um die schwachen Felder unbeaufsichtigt laufen zu lassen.

## 4. Risiko-Sicherung

**Wenn meine Empfehlung falsch liegt:** Das Frontier ist auf `homeoffice` systematisch zu *streng* (`nicht_genannt` statt `teilweise`). Übernähme ich das ungeprüft, würde ein Recruiting-Filter "zeige Homeoffice-Stellen" reale Homeoffice-Anzeigen **rauswerfen** (False Negatives) — Kandidat:innen sehen passende Stellen nicht. Das ist genau die Fehlrichtung, die mein κ-Befund zeigt, deshalb steht `homeoffice` auf Vollreview.

**Stichproben-Kontrolle:**
- Jede 5. Frontier-Annotation manuell reviewen → 16 von 78 Anzeigen. Bei > 2 Korrekturen pro 16 → systematisches Problem, Pipeline pausieren und Prompt für Block 5.1 nachschärfen.

**Validator-Schritt:**
- `python annotation/validate.py annotation/frontier_gold_full.csv` zwingend vor Persistenz — Schema-Verletzungen (das Frontier erfindet gerne Werte wie `homeoffice="möglich"`) blocken den Import in die Reporting-DB. Mein Konvertier-Skript in `04_frontier_compare.ipynb` mappt die häufigsten Verletzungen automatisch, der Validator fängt den Rest.

## 5. Was ich aus Phase 5 gelernt habe

Das überraschendste Disagreement war, dass **beide** Frontier-Modelle auf `homeoffice` dieselbe Abweichung machten wie mein Annotations-Partner in Phase 2 (κ Mensch↔Mensch dort nur 0.122): `nicht_genannt`, wo ich `ja`/`teilweise` annotiert hatte. Das ist kein Halluzinations-Befund, sondern ein **Schema-Befund** — mein Schema definiert nicht scharf genug, ob "Homeoffice" als bloßes Benefit-Stichwort schon `teilweise` zählt. Dass Mensch, ChatGPT und Claude alle an derselben Stelle auseinanderlaufen, zeigt: die Lücke liegt im Schema, nicht im Annotator. Frontier hat mir damit geholfen, mein eigenes Schema schärfer zu lesen, statt es nur als unzuverlässig abzustempeln.

---

_Quellen: `notebooks/04_frontier_compare.ipynb` (κ-Tabelle, Disagreement-Liste), `annotation/frontier_kappa_chatgpt_claude.csv`, `annotation/frontier_disagreements_vs_gold.csv`, `annotation/meine_gold.csv`, `annotation/frontier_gold_chatgpt.csv`, `annotation/frontier_gold_claude.csv`._
