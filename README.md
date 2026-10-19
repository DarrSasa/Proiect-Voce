# Proiect Voce

**Voce AI românească nativă (DiffSinger) — fără accent — pentru OpenUtau Lunai.**

## Fișiere
| Fișier | Conținut |
|---|---|
| [`PLAN.md`](PLAN.md) | Planul complet: faza 0→5, tabelul de înălțimi, setări training pt. GTX 1660 SUPER 6GB |
| [`RECLIST-RO.md`](RECLIST-RO.md) | Reclistul fonetic: **140 unități / 142 note** — vocale, CV, diftongi, triftongi, grupuri, cuvinte-cheie |
| [`CANTEC-RECLIST.md`](CANTEC-RECLIST.md) | Cântecul care conține **toate** unitățile (Sol major, 70 BPM, ~3:10/pas) |
| [`GOOGLE-FLOW.md`](GOOGLE-FLOW.md) | Prompt gata de folosit pentru acapella în Flow + avertismente |

## Prin ce trece proiectul
```
Reclist + Cântec → Înregistrare (40–50 min, 4 transpoziții) → Etichetare (vLabeler)
→ Antrenare DiffSinger (6GB VRAM, batch mic) → ZIP → OpenUtau Lunai → VOCE ROMÂNEASCĂ
```

## Principii
- Material de la **persoane reale, cu consimțământ** (standardul LUNAI)
- Un singur cântăreț consecvent per model
- Fără materiale fără drept de autor / fără respectarea ToS

## Progres
- [x] Reclist + cântec + plan + prompt Flow
- [ ] Înregistrare material
- [ ] Etichetare vLabeler
- [ ] Antrenare model (feminin)
- [ ] Test în OpenUtau Lunai
- [ ] Model masculin
