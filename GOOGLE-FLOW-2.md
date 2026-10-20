# GOOGLE-FLOW-2 — planul de generare „cântat" pentru dataset (24 generații)

Pipeline: **Google Flow (brut) → UVR (curățat) → VocalNet (TOATE vocile la UNA țintă) → etichetare → dataset**
⚠️ Etichetele se pun pe **audio-ul FINAL**, după VocalNet — niciodată pe brut.

---

## 1. Promptul (structura — se copiază identic, se schimbă DOAR blocul [MUZICA] + textul)

```
[IDENTITATE — identic literă cu literă la fiecare generație]
Solo female Romanian singer, young adult, clear bright mezzo-soprano voice,
warm slightly airy timbre, gentle natural vibrato, precise Romanian
pronunciation, THE SAME single consistent singer for the entire track.

[FORMAT]
A cappella, solo voice only. No instruments, no drums, no bass, no backing
vocals, no harmonies, no reverb, no echo, dry close-mic studio recording,
one continuous single take. Singing in Romanian language only.

[TEXT]
Sing exactly these Romanian syllables, in order, one per note:
<LIPEȘTI AICI BLOCUL DE VERSURI DIN SECTIUNEA 3>

[MUZICA — singurul bloc care se schimbă]
Key: G major. Tempo: 75 BPM, steady quarter-note pulse.
Style: Romanian pop ballad, emotional.
Melody in comfortable mid register, long sustained vowels on held notes,
clear diction on every syllable.
```

**Reguli:**
- Dacă Flow are **Ingredients/Characters** (personaje salvate) → creează cântăreața O dată, folosește-o la toate 24.
- Dacă Flowul dă mai multe variante per rulare → păstrează 1–2 bune per generație.
- Cheia e **ghid de registru Flow-ul poate derapează ±; pentru dataset ai nevoie de acoperire de pitch, nu de precizie.
- După fiecare generare, **checklist**: ☐ a cappella? ☐ aceeași voce? ☐ versurile complete, în ordine? ☐ ritm constant? Dacă apare instrument → **nu arunca: UVR separă.**

---

## 2. Tabelul celor 24 de generații

Gama țintă voce feminină: **A3–E5** · Cântecul: `CANTEC-RECLIST.md` (142 note) · ~30 porniri (cu rezerve)

| Gen | Cheie | BPM | Genul | Textul (bloc din §3) |
|---|---|---|---|---|
| G01 | D major | 65 | baladă jazz lentă | REFREN |
| G02 | D major | 65 | chanson | REFREN |
| G03 | D major | 65 | folclor melancolic | STROFA I |
| G04 | D major | 65 | baladă cu șoaptă (whispery) | REFREN |
| G05 | E major | 70 | folclor românesc | REFREN |
| G06 | E major | 70 | blues | STROFA II |
| G07 | E major | 70 | bossa | STROFA I |
| G08 | E major | 70 | pop lent | STROFA III |
| G09 | E major | 70 | baladă pop | REFREN |
| G10 | G major | 75 | pop ballad | REFREN |
| G11 | G major | 75 | folk-pop | REFREN |
| G12 | G major | 75 | pop Eurovision | STROFA I + II |
| G13 | G major | 75 | soft rock | STROFA III |
| G14 | G major | 75 | muzică pentru copii | REFREN |
| G15 | G major | 75 | pop ballad | **CÂNTECUL ÎNTREG** |
| G16 | A major | 90 | dance-pop | REFREN |
| G17 | A major | 90 | pop-rock | REFREN |
| G18 | A major | 90 | gospel | STROFA II |
| G19 | A major | 90 | latin pop | STROFA III |
| G20 | A major | 90 | dance-pop | STROFA I |
| G21 | B major | 110 | power ballad | REFREN |
| G22 | B major | 110 | rock de arenă | REFREN |
| G23 | B major | 110 | clasic/operatic | REFREN + STROFA III |
| G24 | B major | 110 | anthem (Final pe note înalte) | REFREN + FINAL |

*Acoperire: D(A3–C4) · E(C4–B4) · G(E4–D5) · A(F♯4–E5) · B(G♯4–F♯5) = A3–E5 complet.*
*BPM = sugestie de start; dacă genul cere alt tempo (ex. power ballad mai lent), ajustează în blocul [MUZICA].*

---

## 3. Blocurile de versuri (copie exact în [TEXT])

### BLOC REFREN (unități 97–117 — „hook"-ul, cel mai dens)
```
ai ei oi ui au eu ou ia
ie io iu ea eo oa uă
ăi eai uai oai ău eau
```

### BLOC STROFA I (unități 1–48)
```
a ă â e i o u î
ca ce ci co cu ga ge gi
go gu ba be bi bo bu da
de di do du fa fe fi fo
fu pa pe pi po pu ta te
ti to tu ha hi ho ja je
```

### BLOC STROFA II (unități 49–96)
```
ji jo ju la le li lo lu
ma me mi mo mu na ne ni
no nu ra re ri ro ru sa
se si so su șa șe și șo
șu ța țe ți țo țu va ve
vi vo vu za ze zi zo zu
```

### BLOC STROFA III (unități 118–142)
```
pra bra tra dra gra cra fra pla
bla fla cla sta spa șta stra ștra
ceai chiar ghid mânz sfat mult ex brân ză
```

### BLOC FINAL (după ultima notă)
```
a
```
*(linia „a" se cântă lung, note înalte — la G24 se leagă de refren)*

### BLOC CÂNTECUL ÎNTREG (G15) — lipește toate blocurile în ordine: I → II → REFREN → III → FINAL

---

## 4. Ordinea procesării (după generare)
1. **UVR**: separare/de-reverb/de-zgomot (model MDX sau DeEcho) — doar dacă e nevoie
2. **VocalNet**: TOATE clipurile (Flow **și** TTS-ul vorbit) → **aceeași voce țintă**
3. **Verificare la ureche**: aceeași voce peste tot? curat?
4. Abia apoi **etichetare** → `transcriptions.csv` (name, ph_seq, ph_dur)

## 5. Notă licență
Google ToS: folosirea ieșirilor pentru antrenarea altor modele e, de regulă, interzisă — riscul de a folosi acest plan aparține utilizatorului (notat o dată, la cererea lui).
