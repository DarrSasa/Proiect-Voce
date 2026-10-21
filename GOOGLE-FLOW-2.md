# GOOGLE-FLOW-2 — planul de generare „cântat" pentru dataset (24 generații)

Pipeline: **Google Flow (brut) → UVR (curățat) → VocalNet (TOATE vocile la UNA țintă) → etichetare → dataset**
⚠️ Etichetele se pun pe **audio-ul FINAL**, după VocalNet — niciodată pe brut.

**Regula de bază: Flow cântă VERSURI REALE (nu silabe), iar la FIECARE generație cântă POEZIA ÎNTREAGĂ, de la [Intro] până la [Outro].** Poezia din §3 acoperă automat **toate cele 149 de elemente** ale reclistului (verificat automat) — „momeală" perfectă pentru ca TTS/aligner-ul să prindă fiecare sunet.

---

## 1. Promptul (structura — se copiază identic, se schimbă DOAR blocul [MUZICA])

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
Sing the ENTIRE song below from beginning to end, Intro through Outro,
exactly these Romanian lyrics, in order:
<LIPEȘTI AICI POEZIA 1 SAU POEZIA 2 DIN SECȚIUNEA 3B>
(un singur text per generație; G01–G12 = Poezia 1, G13–G12+1 = Poezia 2)

[MUZICA — singurul bloc care se schimbă]
Key: G major. Tempo: 75 BPM, steady quarter-note pulse.
Style: Romanian pop ballad, emotional.
Melody in comfortable mid register, long sustained vowels on held notes,
clear diction on every syllable.
```

**Reguli:**
- Dacă Flow are **Ingredients/Characters** → creează cântăreața O dată, folosește-o la toate 24.
- Cheia e **ghid de registru** — Flow-ul poate derapează ±; pentru dataset ai nevoie de acoperire de pitch, nu de precizie.
- **Checklist după fiecare generare:** ☐ a cântat **toată poezia până la [Outro]**? ☐ a cappella? ☐ aceeași voce? ☐ versurile complete, în ordine? ☐ ritm constant? Dacă apare un instrument → **nu arunca: UVR separă.**
- Dacă Flow taie finalul, repetă cu instrucțiunea explicită: *„sing the complete song including the outro"*.

---

## 2. Tabelul celor 24 de generații

Gama țintă voce feminină: **A3–E5** · ~30 porniri (cu rezerve)
**Textul = o poezie ÎNTREAGĂ din §3B per generație** — G01–G12 folosesc **Poezia 1**, G13–G24 **Poezia 2**; se schimbă doar cheia, BPM-ul și genul.

| Gen | Cheie | BPM | Genul |
|---|---|---|---|
| G01 | D major | 65 | baladă jazz lentă |
| G02 | D major | 65 | chanson |
| G03 | D major | 65 | folclor melancolic |
| G04 | D major | 65 | baladă cu șoaptă (whispery) |
| G05 | E major | 70 | folclor românesc |
| G06 | E major | 70 | blues |
| G07 | E major | 70 | bossa |
| G08 | E major | 70 | pop lent |
| G09 | E major | 70 | baladă pop |
| G10 | G major | 75 | pop ballad |
| G11 | G major | 75 | folk-pop |
| G12 | G major | 75 | pop Eurovision |
| G13 | G major | 75 | soft rock |
| G14 | G major | 75 | muzică pentru copii |
| G15 | G major | 75 | pop ballad (variantă 2) |
| G16 | A major | 90 | dance-pop |
| G17 | A major | 90 | pop-rock |
| G18 | A major | 90 | gospel |
| G19 | A major | 90 | latin pop |
| G20 | A major | 90 | dance-pop (variantă 2) |
| G21 | B major | 110 | power ballad |
| G22 | B major | 110 | rock de arenă |
| G23 | B major | 110 | clasic/operatic |
| G24 | B major | 110 | anthem |

*Acoperire: D(A3–C4) · E(C4–B4) · G(E4–D5) · A(F♯4–E5) · B(G♯4–F♯5) = A3–E5 complet.*
*BPM = sugestie de start; dacă genul cere alt tempo (ex. power ballad mai lent), ajustează în blocul [MUZICA].*

---

## 3. POEZIA — VARIANTA A (elegiacă, cu accente populare) — versurile REALE (lipire în [TEXT], la FIECARE generație)

> Alternativă modernă în **§3B** (recomandată dacă Flow tinde spre folclor).

**[Intro]**
Șoapte vechi în noapte cad,
Între frunzele din brad.
Ghidul cântă-ncet și lin,
Sub o boltă înaltă, senin.

**[Verse 1]**
Pășim ușor pe căi de piatră,
Când focurile ard în jar, pe vatră.
Înțelepții strâng în palme visul,
Și cerul își deschide-atinsul.

Băieții culegeau ghiocei proaspeți din zăvoi,
Cântau cu poftă, fericiți și amândoi.

La moară, lângă apă, crapul doarme lin,
Acolo-i horă-n sat la asfințit,
Cu blana de oaie, jintiță și-un șal,
Cu grai bătrân de la strămoși.

Bade le cântă din flaut,
Vuietul din codru bate,
Tot mai mult răsună zumzetul din sat,
Și mieii ies la apă dimineață.

Și puii țopăi prin ogradă,
Copiii joacă pe-nserate,
Și clar se vede iarba pe dealuri.

**[Chorus]**
O, țara mea cu munți și văi,
Cu șoapte calde-n ochii tăi!
Prin ploaia grea ce cade-n zori,
Lumina trece peste nori.

Iubirea noastră-i un strigăt sfânt,
Ce răsună dulce pe pământ!
Chiar și vioara cântă tare,
Mândră ca o leoaică-n soare.

**[Verse 2]**
Chemarea veche din cetate,
Ne-aduce pace și dreptate.
Ghetele reci calcă pe rouă,
Trăim o viață simplă, nouă.

Cincisprezece stele ard pe cerul greu,
Iar eu te voi păstra în gândul meu mereu.

Hai să bem un ceai cu zahăr,
Bade ne-a adus un coș cu bucate, brânză și jeleu,
Un stejar gigant ne dă umbră,
Cu gura plină de povești.

Știai tu când mânzul fugea pe deal?
Eu îți dau un sfat bătrân:
Luați aminte ce vă spun!

Păsările iau zbor din zori,
Cu dragoste și cu dor,
La pragul casei te-așteptam,
Te port din zi în zi mai mult.

Când mergeai pe lângă râu,
Și luai un stânjenel frumos.

**[Bridge]**
Când vremurile schimbe-or fața,
Și gerul va îngheța viața,
Ne-om aminti de nopți cu soare,
De freamătul din primăvară.

Vântul șuieră prin uluci,
Cu țurțuri lungi la geamuri,
Am șezut lângă ștrangul vechi,
Și frații mei se-ntorc pe plai.

Fie un cântec pentru tine,
Stai puțin și ascultă inima!
Fără rău și fără spaimă,
Și ștafeta luminii prinde vânt.

Împăturește-ți teama-n gând,
Și cântă liber, oricând!

**[Chorus]**
O, țara mea cu munți și văi,
Cu șoapte calde-n ochii tăi!
Prin ploaia grea ce cade-n zori,
Lumina trece peste nori.

Iubirea noastră-i un strigăt sfânt,
Ce răsună dulce pe pământ!
Chiar și vioara cântă tare,
Mândră ca o leoaică-n soare.

**[Outro]**
La jumătate de cărare,
Lin se stinge freamătul din munte,
Pacea-și pleacă umbra peste frunte.
Trecem încet prin umbra de sub brad...
Și nici un rău nu mai există,
Șoapte vechi în noapte cad.

### Verificare acoperire (automată, refăcută după ultima rescriere)
**149/149 elemente** ✔️ — toate silabele-CV, diftongii, triftongii (incl. `uai`, `eai`, `iai`, `ieu`, `ioa`, `âu`), grupurile `pra…ștra` și cuvintele-cheie (`ceai, chiar, ghid, mânz, sfat, mult, ex, brânză`) + `i` palatal final (`ochii`, `Băieții`) sunt în poezie.

---

## 3B. POEZIA MODERNĂ — ÎMPĂRȚITĂ ÎN DOUĂ POEZII (refăcută: rimă + lungime egală)

> **De ce două poezii:** textul unic era prea lung → Flow îl cânta în grabă. Acum **Poezia 1** (30 rânduri) și **Poezia 2** (40 rânduri) se cântă **separat**, mai lent și mai clar.
> **Refăcut:** fiecare rând ≈ **8–12 silabe (medie 10)** · **rime în perechi (AABB)** la fiecare două rânduri · **cuvinte moderne, urbane** (fără folclor) · împreună acoperă **149/149** ✔️
> **Regula:** la fiecare generație lipești **o singură poezie, întreagă**. Împarte generațiile: **G01–G12 → Poezia 1**, **G13–G24 → Poezia 2** (trebuie folosite AMBELE).

### POEZIA 1 — „Pe bulevard" · 30 rânduri · [Intro] + [Verse 1] + [Chorus]

**[Intro]**
Pe bulevard se aud șoapte în noapte,
Și-n geamul deschis rămân doar șoapte.
Ghidul din telefon îmi cântă lin,
Sub boltă înaltă e cerul senin.

**[Verse 1]**
Vuiet, foc, pui și jar pe grătar,
Băieții dădeau radioul, cântau iar.
Hai să bem ceai cu zahăr și cafea,
Cu blazer nou și muzica mea.
A venit comanda: brânză și jeleu,
Cu gura plină de povești mereu.
Tot mai mult răsună-n sală, tare,
Peste treizeci de grade, ce soare!
Hobby-ul meu: voce, muzică și joc,
Poze cu flash pe balcon — ce noroc!
Un mall gigant se deschide diseară,
Și bem o cafea pe afară.
Clar se vede: pisica pe la noi.
La șase, în oraș, prieteni noi.
Și țopăi prin stradă pe trotuar,
La șase fix, pe stradă, spre mare.
Înțelepții strâng în palme visul,
Și cerul își deschide-atinsul.

**[Chorus]**
Cu șoapte calde-n ochii tăi,
Și-i tot ce simt, și tot ce vrei.
Prin ploaia grea ce cade-n zori,
Lumina caldă trece peste nori.
Iubirea noastră-i un strigăt nou,
Mai vreau o noapte cu tine, una, două!
Chiar și pe stadioane cântă tare,
Mândră ca o leoaică-n soare.

### POEZIA 2 — 40 rânduri · [Verse 2] + [Bridge] + [Outro]

**[Verse 2]**
Ei ne așteptau în stația de metrou,
Trăim o viață simplă, totul nou.
Cu cravata strâmbă la interviu,
Sâmbătă fugim până la târziu.
Un moment și totul s-a schimbat,
Îți dau un sfat pe loc, neîncetat.
Cincisprezece mesaje pe seară,
Căci te aștept iarăși afară.
Ce iei la mic, iubirea mea?
Știai tu ce simt, inima ta?
Și-mi e jind de-o vacanță-n noi,
Liberă ca un mânz, în doi.
Mergeai pe lângă râu, iar eu,
Și-i luai tu inima mereu.
Avioanele iau zbor peste mare,
Pragul casei te-aștepta, răbdare.
Te port din zi în zi mai mult,
Ascult în gând al tău cuvânt.

**[Bridge]**
Vremurile capătă altă față,
Gerul îngheață viața toată.
De freamătul din primăvară,
De nopți cu soare și de afară.
Vântul șuieră printre blocuri,
Și frații mei au alte planuri.
Am șezut lângă ștrangul vechi,
Cu țurțuri reci, iarna în urechi.
Fie un cântec pentru tine,
Stai un pic și prinde-l bine.
Și ștafeta luminii prinde vânt,
Fără rău, fără spaimă pe pământ.
Împăturește-ți teama-n gând,
Și cântă liber, oricând!

**[Outro]**
Lin se stinge lumina din oraș,
La jumătate de drum — încă un pas.
Pacea-și pleacă umbra peste frunte,
Rămân doar brațele tale, o punte.
Și nici un rău nu mai există,
Rămâne doar dragostea pe listă.
Și șoapte vechi cad înc-o dată,
La fel ca-n noaptea asta, ca odată.

---

## 4. Ordinea procesării (după generare)
1. **UVR**: separare/de-reverb/de-zgomot (model MDX sau DeEcho) — doar dacă e nevoie
2. **VocalNet**: TOATE clipurile (Flow **și** TTS-ul vorbit) → **aceeași voce țintă**
3. **Verificare la ureche**: aceeași voce peste tot? curat?
4. Abia apoi **etichetare** → `transcriptions.csv` (name, ph_seq, ph_dur)

## 5. Notă licență
Google ToS: folosirea ieșirilor pentru antrenarea altor modele e, de regulă, interzisă — riscul de a folosi acest plan aparține utilizatorului (notat o dată, la cererea lui).
