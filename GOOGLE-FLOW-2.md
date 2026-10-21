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
<LIPEȘTI AICI POEZIA ÎNTREAGĂ DIN SECȚIUNEA 3 SAU 3B — o singură variantă,
aceeași la toate cele 24 de generații>

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
**Textul = poezia ÎNTREAGĂ (§3) la fiecare generație** — se schimbă doar cheia, BPM-ul și genul.

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

## 3B. POEZIA MODERNĂ (Varianta B — recomandată pentru Flow)

> **De ce Varianta B:** Varianta A are cuvinte din muzica populară (bade, moară, horă, jintiță, plai, dor…) și Google Flow tinde să genereze voci/stil **folclorice** din cauza lor. Varianta B folosește **vocabulary actual, urban**: cafea, mall, metrou, notificări, radio, balcon, ecran, vacanță, interviu… → Flow rămâne pe genul ales în [MUZICA]. **Verificată automat: 149/149** ✔️ — exact aceleași elemente ca Varianta A.

**[Intro]**
Șoapte vechi în noapte cad,
Pe sub stele, pe bulevard.
Ghidul din telefon îmi șoptește lin,
Sub o boltă înaltă, senin.

**[Verse 1]**
Pășim ușor pe căi de piatră,
Când jarul de pe grătar arde iar.
Înțelepții strâng în palme visul,
Și cerul își deschide-atinsul.

Băieții dădeau drumul la radio tare,
Cântau cu poftă, fericiți și amândoi.

Hai să bem un ceai cu zahăr,
Comanda a ajuns cu brânză și jeleu,
Un mall gigant e deschis până târziu,
Cu gura plină de povești.

Poze cu flash de pe balcon,
Blazer nou, cafea și muzica mea.
Vuietul din oraș nu tace,
Hobby-ul meu: voce, muzică, joc.
Tot mai mult răsună zumzetul în sală,
Peste treizeci de grade afară.

Clar se vede totul pe ecran,
Și țopăi pe trotuar cu pantofi noi,
Pe stradă ninge cu lumină,
Ne vedem la șase în oraș.

**[Chorus]**
O, inima mea, ce vrei acum,
Cu șoapte calde-n ochii tăi!
Prin ploaia grea ce cade-n zori,
Lumina trece peste nori.

Iubirea noastră-i un strigăt nou,
Ce răsună dulce pe pământ!
Chiar și pe stadioane cântă tare,
Mândră ca o leoaică-n soare.

**[Verse 2]**
Chemarea ta mă sună iar,
Ei ne așteptau în stația de metrou,
Cu cravata strâmbă la interviu,
Trăim o viață simplă, nouă.

Un moment și totul s-a schimbat,
Cincisprezece notificări pe noapte,
Iar eu te voi păstra în gândul meu mereu.

Ce iei la micul dejun, iubire?
Eu îți dau un sfat pe loc:
Știai tu ce simt când ești departe?

Sâmbătă fugim de-acasă-n oraș,
Și-mi e jind de-o vacanță-n doi,
Sunt liberă ca un mânz sălbatic,
Două cafele, una pentru tine,
Avioanele iau zbor spre mare,
Cu dragoste și fără efort,
La pragul casei te-așteptam,
Te port din zi în zi mai mult.

Când mergeai pe lângă râu,
Și luai telefonul lui în mână.

**[Bridge]**
Când vremurile schimbe-or fața,
Și gerul va îngheța viața,
Ne-om aminti de nopți cu soare,
De freamătul din primăvară.

Vântul șuieră printre blocuri,
Cu țurțuri lungi la geamuri,
Am șezut lângă ștrangul vechi,
Și frații mei au alte planuri.

Fie un cântec pentru tine,
Stai puțin și ascultă inima!
Fără rău și fără spaimă,
Și ștafeta luminii prinde vânt.

Împăturește-ți teama-n gând,
Și cântă liber, oricând!

**[Chorus]**
O, inima mea, ce vrei acum,
Cu șoapte calde-n ochii tăi!
Prin ploaia grea ce cade-n zori,
Lumina trece peste nori.

Iubirea noastră-i un strigăt nou,
Ce răsună dulce pe pământ!
Chiar și pe stadioane cântă tare,
Mândră ca o leoaică-n soare.

**[Outro]**
La jumătate de drum,
Lin se stinge lumina din oraș,
Pacea-și pleacă umbra peste frunte.
Trecem încet în brațele tale,
Și nici un rău nu mai există,
Șoapte vechi în noapte cad.

---

## 4. Ordinea procesării (după generare)
1. **UVR**: separare/de-reverb/de-zgomot (model MDX sau DeEcho) — doar dacă e nevoie
2. **VocalNet**: TOATE clipurile (Flow **și** TTS-ul vorbit) → **aceeași voce țintă**
3. **Verificare la ureche**: aceeași voce peste tot? curat?
4. Abia apoi **etichetare** → `transcriptions.csv` (name, ph_seq, ph_dur)

## 5. Notă licență
Google ToS: folosirea ieșirilor pentru antrenarea altor modele e, de regulă, interzisă — riscul de a folosi acest plan aparține utilizatorului (notat o dată, la cererea lui).
