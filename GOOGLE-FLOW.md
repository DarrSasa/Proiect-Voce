# Google Flow — prompt pentru voce ACAPELA în română

> ⚠️ **Citește întâi „Avertismente" — la final.**

---

## Promptul (șablon — completează {} )

```
Acapella solo female voice, completely dry studio recording, NO instruments,
NO beat, NO background music, NO reverb. Romanian language, crystal-clear
enunciation, every syllable pronounced separately and precisely.
One syllable per quarter note at 70 BPM, constant steady pitch, even dynamics,
same consistent female timbre for the whole take.
Sing exactly this sequence of Romanian syllables, in order, one per note:

{LISTA_DE_SILABE}

Key: {DE_EXEMPLU: G major}. Hold the final note for 4 beats.
```

### Varianta pe pas (mai scurtă, per înălțime)
```
Solo female acapella, no instruments, Romanian, dry studio sound.
Pitch: {DE_EXEMPLU: G4} as the tonal center, sing each syllable ON THE GIVEN PITCH,
one syllable = one beat, 70 BPM, precise pronunciation, identical voice throughout:
{LISTA_DE_SILABE}
```

### Cum îl folosești per înălțime (din PLAN.md)
| Pas | Cheie | Completezi în prompt |
|---|---|---|
| 2 | Sol major | `Key: G major` |
| 3 | Mi major | `Key: E major` |
| 4 | La major | `Key: A major` |
| 5 | Si major (refren) | `Key: B major` + în locul listei întregi, doar unitățile 97–117 |

### Liste de silabe — copiază direct din `RECLIST-RO.md`
Exemplu bucată: `a ă â e i o u î ca ce ci co cu ga ge gi go gu ba be bi bo bu ...`
(Blocuri de 20–40 de silabe per generație se obeyesc mai bine decât lista întreagă.)

---

## Avertismente (importante, oneste)

| # | Problema | De ce conteabă |
|---|---|---|
| 1 | **Notele exacte** — generatoarele de muzică AI nu țin pitch-ul precis cerut | Trainingul are nevoie de pitch adevărat; Flow „decoratează" melodica |
| 2 | **Silabele** — va „cânta frumos" peste listă, sarind/înmoliind silabe | Reclistul cere **fiecare** silabă exact — altfel etichetarea e imposibilă |
| 3 | **Vocea consecventă** — fiecare generare = alt timbru/altă „cântăreață" | Un model are nevoie de **UNA** singură voce constantă pe 30–60 min |
| 4 | **ToS** — verifică în Google Flow dacă ai voie să folosești ieșirile ca date de **antrenament** pentru alte modele AI; majoritatea serviciilor **interzic** | Poate invalida folosirea |
| 5 | **Etică (standardul LUNAI)** — vocile lor = persoane reale, cu consimțământ; o voce „împrumutată" de la alt AI = model derivat | Comunitatea DiffSinger refuză vocile fără sursă clară |

### Verdict
- ✅ **Folosește Flow pentru**: teste, exersat phonemizere, mock-up-uri, împărțit fraze — *practică*
- ❌ **Nu-l folosi pentru**: corpusul FINAL de training (calitate + consecvență + ToS + etică)
- ✅ **Corpusul final**: cântăreață reală (persoană umană, consimțământ) — 40 de minute, o singură sesiune

### Dacă totuși testezi — setarea care ajută
1. Aceeași descriere de voce în **fiecare** prompt (menține „același personaj")
2. Loturi mici (20–40 silabe), nu lista întreagă
3. Ascultă 100% înainte să investești timp — dacă silabele nu-s clare, oprește-te
