# PLAN — Vocea românească DiffSinger (fără accent)

Obiectiv: voce AI **nativ românească** (femeie + bărbat), calitate „LUNAI", rulată în **OpenUtau Lunai**.

---

## Faza 0 — Pregătire (30 min)
1. ✅ OpenUtau Lunai 0.2.1.0 instalat
2. Instalează **vLabeler** (etichetare: https://github.com/enovella-ru/releases sau căutare „vLabeler DiffSinger")
3. Testează MIDI: `File → Import MIDI` cu o piesă mică
4. Verifică GPU: `nvidia-smi` în CMD (1660 SUPER 6GB — da, e suportat: CUDA + DirectML)

## Faza 1 — Material (30–60 min de cântat) ★ inima proiectului
**Ce cântă:** `RECLIST-RO.md` (142 note) + `CANTEC-RECLIST.md` (cântecul cu ele)

### Planul de înălțimi (note) — tabelul tău:

| Pas | Ce | Cheie (transpoziție) |Țintă gama | Luări | Durată |
|---|---|---|---|---|---|
| 1 | **Încălzire**: scara Sol major, urcare coborâre 2 octave + pași cromatici E4→D5 | — | E4–D5 | 1 | ~5 min |
| 2 | **Cântecul — pas de bază** | **0 st (Sol major)** | E4–D5 | 2 | ~7 min |
| 3 | **Cântecul — mai jos** | **−3 st (Mi major)** | C4–B4 | 2 | ~7 min |
| 4 | **Cântecul — mai sus** | **+2 st (La major)** | F♯4–E5 | 2 | ~7 min |
| 5 | **Doar refrenul — sus** | **+4 st (Si major)** | G♯4–F♯5 | 1 | ~3 min |
| 6 | **Scară de acoperire**: toate notele A3→E5, fiecare 2 bătăți, cu „a/ă/î" | — | A3–E5 | 1 | ~5 min |
| — | Pauze + reluări minore | | | | ~5 min |
| | | | | **TOTAL** | **≈ 40–50 min** ✅ în intervalul 30–60 |

**Reguli de înregistrare:**
- WAV **44.1 kHz / mono**, fără reverb/efecte/egalizare
- Cameră liniștită (pături pe pereți = „studio" ieftin), distanță ~15–20 cm de microfon
- Aceeași voce, același timbru **în toate luările** (foarte important!)
- Un fișier WAV per luare: `reclist_G_take1.wav`, `reclist_E_take1.wav`...
- Interval de lucru vocal: A3–E5 (nu forța peste; dacă ești/vocea e mai gravă, apropie cheile de vocea reală)

### De unde vine vocea (opțiuni, în ordinea calității):
| # | Sursă | Calitate | Etică/ToS |
|---|---|---|---|
| 1 | **Cântăreață reală** (tu, o cunoștință, angajată Fiverr 10–50$) | ⭐⭐⭐⭐⭐ | ✅ Calea LUNAI (consimțământ) |
| 2 | **Vocea ta** (exercițiu — se poate antrena și pe vocea proprie) | ⭐⭐⭐⭐ | ✅ |
| 3 | Google Flow (vezi `GOOGLE-FLOW.md`) | ⭐⭐ (test) | ⚠️ Vezi avertismentele din fișier |

## Faza 2 — Etichetare (cel mai lung pas, 1–3 zile)
1. vLabeler: deschizi WAV-urile + declanșezi pe **fiecare notă** din cântec (ai secvența exactă în `CANTEC-RECLIST.md`)
2. Fiecare notă → fonemul din reclist (1–142) + durata sa
3. Ieșire: `transcriptions.csv` cu coloanele `name, ph_seq, ph_dur` (format openvpi/DiffSinger)
4. Verificare: 100% note etichetate, fără silabe sărite (2 note la „brânză"!)

## Faza 3 — Antrenare (PC-ul tău: i9-12900H / 32 GB / **GTX 1660 SUPER 6 GB**)
| Setare | Valoare (pt. 6 GB VRAM) |
|---|---|
| batch | **1–2** + gradient accumulation |
| precizie | **FP16** (mixed precision) |
| RAM | 32 GB = suficient pt. preprocessing |
| Estimare | câteva ore per model (acoustic + variance) |
| Tool | **openvpi/DiffSinger** (git clone) sau **Utai** (GUI, mai simplu) |

Pași: `binarize` → `train acoustic` → `train variance` → export → **ONNX/zip** → drag & drop în OpenUtau Lunai.

## Faza 4 — Test și iterații
1. Cântă refrenul cu vocea nouă + phonemizerul din setul ei
2. Ascultă **special**: ă/â/î, ș, ț, diftongi (ei, au, oa)
3. Dacă un sunet „rătăcește" → re-etichetezi doar notele problemă, re-antrenezi (fine-tune)

## Faza 5 — Vocea masculină
Repeti Faza 1–4 cu **voce bărbătească** (același reclist; gama: G3–C5, transpoziții −5/0/+2).

---

## Reguli de aur (standarde LUNAI)
- ✅ **Consimțământ** de la vocea înregistrată (scris, simplu: „sunt de acord cu folosirea vocii mele pentru antrenarea modelului X, non-comercial")
- ✅ Un singur cântăreț consecvent în tot materialul
- ❌ Nu materiale de pe YouTube/fără voie; nu ToS încălcate (vezi GOOGLE-FLOW.md)
