# GHID COMPLET DE ÎNCEPĂTOR — Bancă vocală românească DiffSinger
### De la fișierele tale .wav până la antrenarea modelului pe GPU

> **Cum folosești ghidul:** parcurgi etapele în ordine (1 → 10). Fiecare pas are: **Ce e** → **De unde descarci** → **Cum lucrezi** → **Rezultat așteptat**. Comenziile se copiază ca atare în Command Prompt (cmd). Înlocuiește `D:\BANCA-VOCE` cu unitatea ta, dacă nu ai D:.
> **Ai blocat un pas?** Salvează unde ai rămas și întreabă-mă — trecem împreună.

---

## 0. ÎNAINTE DE TOATE: răspunsul la întrebarea cu GPU-ul

**„Pe GPU-ul meu merge și la calitate maximă?" — DA. Iar calitatea NU depinde de placa video.**

| | GTX 1660 SUPER 6 GB (a ta) | GPU închiriat (24–48 GB) |
|---|---|---|
| Calitatea modelului final | ✅ **Aceeași** — dacă datele și setările sunt aceleași | ✅ Aceeași |
| Viteză | Mai lent — învățare în **zile**, cu lot (batch) mic și FP16 | Mult mai rapid — **ore** |
| Ce decide calitatea | **Datele + etichetele + configurația**, nu GPU-ul | la fel |
| Când folosești | Testări, configurare, primul antrenament complet | Când vrei viteză sau liniște (nu pornește PC-ul tău) |

- **Ce face GPU-ul:** viteza și cât de mult încap simultan. **Ce NU face:** nu adaugă calitate. Un model antrenat pe1660 SUPER cu aceleași date și același număr de pași = același model ca pe un A100.
- **Pe placa ta:** merge cu rețeta **FP16 (precizie pe jumătate) + warm-start** (pornești de la un model deja învățat, îl adaptezi) — lotul se micșorează ca să încapă pe 6 GB. E testat că merge.
- **Recomandarea mea:** configurezi și testezi **pe PC-ul tău** (binarizare, teste scurte de 10–20 min); **runda lungă de antrenare** o poți face pe un GPU închiriat dacă nu ai răbdare cu zilele. Sau integral pe a ta — se poate, doar durează.
- **Adrese de închiriat** (când vei dori): https://vast.ai · https://runpod.io · https://lambdalabs.com — cauți GPU cu ≥24 GB VRAM (ex. RTX 4090), cost orientativ ~0,3–0,8 $/oră. Procedura: creezi cont → alegi imagine „PyTorch" → urci arhiva cu datele tale (zeci de MB) → rulezi aceleași comenzi ca acasă → descarci fișierele `*.ckpt` (modelul) la final.

---

## 1. HARTA DRUMULUI

```
[9 fișiere + materialele]        ETAPA 1: curățare (Acoustica/RX/FL) — FĂCUTĂ
        ↓                        ETAPA 2: export final: mono, 44,1 kHz, WAV 16-bit
   wav-uri finale
        ↓                        ETAPA 3: tăiere în segmente (AudioSlicer)
   segmente .wav
        ↓                        ETAPA 4: transcriere text (.txt) cu Whisper română
        ↓                        ETAPA 5: aliniere forțată (MFA + bundle românesc) → TextGrid
        ↓                        ETAPA 6: transcriptions.csv (script inclus)
        ↓                        ETAPA 7: verificare (vLabeler / OpenUTAU)
        ↓                        ETAPA 8: instalare DiffSinger
        ↓                        ETAPA 9: binarizare (wav+csv → fișiere pentru GPU)
        ↓                        ETAPA 10: antrenare (GPU) → apoi inferență
```

---

## 2. TABELUL DE DESCĂRCĂRI (toate adresele într-un loc)

| # | Program | Adresă | De ce îl trebuie |
|---|---|---|---|
| 1 | Miniforge (conda) | https://conda-forge.org/download/ | Instalează MFA (aliniatorul) |
| 2 | Python 3.10+ | https://www.python.org/downloads/ | Rulezi scripturile și DiffSinger; **bifăză „Add to PATH" la instalare** |
| 3 | Git | https://git-scm.com/download/win | Copiază repo-urile de pe GitHub |
| 4 | AudioSlicer (GUI) | https://github.com/flutydeer/audio-slicer/releases | Tăiere automată după liniști; **descarci release, rulezi `slicer-gui.exe`** |
| 5 | faster-whisper | `pip install faster-whisper` (după Python) | Transcriere audio → text, în română |
| 6 | **Bundle-ul românesc MFA** | https://berkeley.box.com/s/6wzfd6yzzybqzx3u1fpvjabv05jjlblh | Dicționar + model acustic + G2P **pentru română** (18.252 cuvinte) |
| 7 | MFA (prin conda) | vezi Etapa 5 | Alinierea forțată |
| 8 | DiffSinger (openvpi) | https://github.com/openvpi/DiffSinger | Binarizarea + antrenamentul |
| 9 | vLabeler | **l-ai deja**: `C:\MY_TOOLS\vLabeler` | Verificarea etichetelor |
| 10 | OpenUTAU | https://openutau.com/ | Verificarea finală / folosirea vocii |
| — | ffmpeg (opțional) | https://www.gyan.dev/ffmpeg/builds/ | Doar dacă vreun tool cere; whisper-ul din ghid nu-l cere |

*Surse oficiale: instalarea MFA ([distribuție conda, Miniforge](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html)), bundle-ul [Romanian MFA Bundle](https://sites.google.com/berkeley.edu/julian-vargo/linguistics-software), structura setului ([MakeDiffSinger](https://github.com/openvpi/MakeDiffSinger)).*

---

## 3. STRUCTURA DE FOLDERE (faci o singură dată)

Deschide **cmd** și rulează (schimbă unitatea dacă e nevoie):

```cmd
mkdir D:\BANCA-VOCE
mkdir D:\BANCA-VOCE\01_curat          &:: wav-urile tale finale curățate
mkdir D:\BANCA-VOCE\02_segmente       &:: ieșirea AudioSlicer
mkdir D:\BANCA-VOCE\03_corpus\ioana   &:: MFA vrea: un folder „vorbitor" cu wav + txt
mkdir D:\BANCA-VOCE\04_aliniat         &:: ieșirea MFA (TextGrid)
mkdir D:\BANCA-VOCE\05_dataset\raw\wavs  &:: setul final DiffSinger
mkdir D:\BANCA-VOCE\06_binar           &:: ieșirea binarizării
mkdir D:\BANCA-VOCE\07_modele          &:: modelele antrenate (.ckpt)
mkdir D:\BANCA-VOCE\scrise             &:: scripturile .py din acest ghid
```

Vei copia manual: **wav-urile finale** în `01_curat`.

---

## 4. ETAPA 1–2 — Audio final (verificare, nu prelucrare nouă)

**Ce e:** ai terminat curățarea (Acoustica/RX/FL). Acum doar verifici că fișierele care intră în set sunt corecte.

**Cum lucrezi:**
1. Toate wav-urile finale din `01_curat` trebuie să fie: **mono, 44.100 Hz, WAV 16-bit** (export cu dither, cum am stabilit).
2. Verifică cu comanda de verificare pe care ți-am dat-o-o (cea care zice `NUME | CANALE | BITI`): rulezi cmd în `01_curat` și trebuie să vezi peste tot `1 MONO | 16`.
3. **Reguli:** același lanț de prelucrare și aceiași parametri la TOATE fișierele persoanei; fără muzică pe fundal; segmentele să nu aibă ecou remarcabil.

**Rezultat așteptat:** un folder `01_curat` în care scriptul de verificare nu raportează niciun `2 STEREO` și niciun `24` (24 e doar pentru copiile de lucru, nu pentru setul final).

---

## 5. ETAPA 3 — Tăierea în segmente (AudioSlicer)

**Ce e:** AudioSlicer taie automat înregistrările lungi în bucăți mici (fraze), **după liniști** (detectare RMS). Fiecare bucată = viitorul exemplar de antrenament.

**De unde descarci:** https://github.com/flutydeer/audio-slicer/releases → ultima versiune → arhivă → o dezarhivezi.

**Cum lucrezi:**
1. Rulezi `slicer-gui.exe`.
2. Selectezi folderul de intrare: `D:\BANCA-VOCE\01_curat` (sau subfolderele cu ele).
3. Selectezi folderul de ieșire: `D:\BANCA-VOCE\02_segmente`.
4. Setări recomandate pentru voce (dacă nu vrei să te complici, lasă valorile implicite și ajustezi după ascultare):
   - **Threshold (prag de liniște):** −40 dB (implicit) — dacă taie prea rar, urcă spre −35; prea des, coboară spre −45.
   - **Min length:** 2000–5000 ms (segmentul minim; sub 2 s evită bucățele inutile).
   - **Max silence:** ~500 ms (câtă liniște se păstrează la capete).
5. Apesezi **Slice** și aștepți.

**Verificare (obligatorie, manuală):** asculți rapid `02_segmente` — **dacă vreo tăietură a rupt un cuvânt în două**, ștergi segmentul ăla și-l retaiezi în Acoustica (selectezi zona → export selection). La volumul tău de fișiere sunt zeci–câteva sute de segmente: o trecere cu căști, ~10–15 minute.

**Rezultat așteptat:** `02_segmente\*.wav` — multe fișiere scurte, fiecare cu o frază întreagă.

---

## 6. ETAPA 4 — Transcrierea în text (Whisper, română)

**Ce e:** Whisper = inteligență artificială de recunoaștere vocală. Îți scrie **textul** spus/cântat în fiecare segment, într-un fișier `.txt` lângă wav. (MFA are nevoie de text ca să poată alinia.)

**Instalare (o singură dată):**
1. Instalezi Python de la https://www.python.org/downloads/ — **cu bifă „Add Python to PATH"**.
2. Deschizi cmd și rulezi:
```cmd
pip install faster-whisper
```

**Script — salvează-l ca `D:\BANCA-VOCE\scrise\transcrie_whisper.py`:**
(deschizi Notepad → lipsești codul → File → Save As → nume: `transcrie_whisper.py`, tip: *All Files*, encoding: **UTF-8**)

```python
# transcrie_whisper.py
# Rulare:  python transcrie_whisper.py D:\BANCA-VOCE\02_segmente
import sys, os, glob
from faster_whisper import WhisperModel

folder = sys.argv[1]
model = WhisperModel("small", device="cpu", compute_type="int8")  # mai bun: "medium" (mai lent)

wavs = sorted(glob.glob(os.path.join(folder, "*.wav")))
if not wavs:
    print("Nu am gasit .wav in", folder); sys.exit(1)

for wav in wavs:
    out = os.path.splitext(wav)[0] + ".txt"
    if os.path.exists(out):
        print("[deja]", os.path.basename(out)); continue
    segments, info = model.transcribe(wav, language="ro", beam_size=5)
    text = " ".join(s.text.strip() for s in segments).strip()
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(os.path.basename(wav), "->", text)

print("GATA:", len(wavs), "fisiere")
```

**Cum lucrezi:**
```cmd
cd /d D:\BANCA-VOCE\scrise
python transcrie_whisper.py D:\BANCA-VOCE\02_segmente
```
- Aștepți (pe CPU durează, depinde de numărul de segmente; se oprește și reiei de unde a rămas — cele deja transmise sunt sărite).
- **Pe cântat**, Whisper greșește mai des decât pe vorbit. De-asta: **verifici fiecare `.txt` în Notepad și corectezi textul** ca să corespundă exact ce auzi. E singura muncă „pe literă" din tot ghidul — merită, că de textul ăsta depind etichetele.

**Rezultat așteptat:** lângă fiecare `segment.wav` există `segment.txt` cu versul românesc corect.

---

## 7. ETAPA 5 — Alinierea forțată (MFA + bundle-ul românesc)

**Ce e:** MFA (Montreal Forced Aligner) „potrivește" automat textul pe audio și îți spune **exact cât durează fiecare fonem** (sunet). Cu bundle-ul românesc, pronunțiile vin din dicționarul românesc — **fără accente străine**.

### 7.1 Instalare MFA (o singură dată)

1. Instalezi **Miniforge** de la https://conda-forge.org/download/ (executorul Windows → Next până la capăt).
2. Deschizi **cmd** și rulezi, pe rând (comenzi oficiale din [documentația MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html)):

```cmd
conda create -n aligner -c conda-forge montreal-forced-aligner -y
conda activate aligner
mfa --help
```
Dacă `mfa --help` afișează lista de comenzi → MFA e instalat.

### 7.2 Instalarea modelelor românești

1. Descarci bundle-ul de la linkul din tabel (Box): **Romanian MFA Bundle**.
2. Dezarhivezi — conține fișiere `.zip` pentru: **dicționar**, **model acustic**, **G2P**.
3. Creezi (dacă nu există) folderul modelelor MFA și copiezi acolo arhivele:
```cmd
mkdir "%USERPROFILE%\Documents\MFA\pretrained_models\acoustic"
mkdir "%USERPROFILE%\Documents\MFA\pretrained_models\dictionary"
mkdir "%USERPROFILE%\Documents\MFA\pretrained_models\g2p"
```
   copiezi `.zip`-ul cu modelul acustic în `...\acoustic\`, dicționarul în `...\dictionary\`, g2p în `...\g2p\`.
4. Verifici că MFA le vede:
```cmd
conda activate aligner
mfa model download acoustic        &:: (fără nume) afișează lista modelelor instalate
mfa model download dictionary      &:: la fel, pentru dicționare
```
   *Alternativ, nu copiezi nimic: poți da **calea directă către fișierul .zip** în comanda de aliniere (pasul 7.4).*

### 7.3 Pregătirea corpus-ului (structura MFA)

MFA cere: `folder_corpus\vorbitor\*.wav` **+** același nume `.txt` cu textul:

```cmd
copy D:\BANCA-VOCE\02_segmente\*.wav D:\BANCA-VOCE\03_corpus\ioana\
copy D:\BANCA-VOCE\02_segmente\*.txt D:\BANCA-VOCE\03_corpus\ioana\
```
*(structura `03_corpus\ioana\` ai creat-o deja la Etapa 3; „ioana" = numele vorbitorului, poți pune alt nume)*

### 7.4 Comanda de aliniere

```cmd
conda activate aligner
mfa align D:\BANCA-VOCE\03_corpus DICT_NAME ACUSTIC_NAME D:\BANCA-VOCE\04_aliniat
```
înlocuiește `DICT_NAME` / `ACUSTIC_NAME` cu **numele exacte** văzute la pasul 7.2.4 (sau pune **căile complete către .zip** în locul numelor).

**Dacă MFA se plânge de „database"/server** (la prima rulare pe unele instalări):
```cmd
mfa server init
mfa server start
```
și reiei comanda `mfa align`.

**Rezultat așteptat:** `04_aliniat\ioana\*.TextGrid` — un fișier TextGrid pe segment, cu timpii fonemelor. Dacă un segment dă eroare (cuvânt necunoscut dicționarului), îl scoți temporar și-l rezolvi ulterior cu G2P-ul din bundle sau manual — nu oprește restul lotului.

---

## 8. ETAPA 6 — Generarea `transcriptions.csv`

**Ce e:** fișierul-manifest al setului DiffSinger: pe fiecare linie — numele wav-ului, șirul de foneme (`ph_seq`) și durata lor în cadre (`ph_dur`; 1 cadru = 1/86,13 s la 44,1 kHz + hop 512).

**Script — salvează-l ca `D:\BANCA-VOCE\scrise\textgrid2csv.py`** (Notepad → Save As → All Files → UTF-8):

```python
# textgrid2csv.py
# Rulare: python textgrid2csv.py <foldereare_TextGrid> <foldereare_wav> <folder_iesire>
# Ex:     python textgrid2csv.py D:\BANCA-VOCE\04_aliniat D:\BANCA-VOCE\03_corpus D:\BANCA-VOCE\05_dataset
import sys, os, glob, re, csv, shutil

tg_dir, wav_dir, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
SR, HOP = 44100, 512
FPS = SR / HOP  # ~86.13 cadre/s

def parse_phones(path):
    txt = open(path, encoding="utf-8").read()
    tiers = re.split(r"item \[\d+\]:", txt)[1:]
    best, best_n = None, -1
    for t in tiers:
        m = re.search(r'name = "(.*?)"', t)
        nm = m.group(1).lower() if m else ""
        ivs = re.findall(r'xmin = ([\d.eE+-]+)\s*xmax = ([\d.eE+-]+)\s*text = "(.*?)"', t)
        if "phone" in nm:
            return ivs          # tier-ul de foneme
        if len(ivs) > best_n:   # rezerva: tier-ul cu cele mai multe intervale
            best, best_n = ivs, len(ivs)
    return best or []

wavs = {os.path.splitext(os.path.basename(p))[0]: p
        for p in glob.glob(os.path.join(wav_dir, "**", "*.wav"), recursive=True)}

os.makedirs(os.path.join(out_dir, "raw", "wavs"), exist_ok=True)
rows = []
for tg in sorted(glob.glob(os.path.join(tg_dir, "**", "*.TextGrid"), recursive=True)):
    name = os.path.splitext(os.path.basename(tg))[0]
    if name not in wavs:
        print("[lipsa wav]", name); continue
    seq, durs = [], []
    for xmin, xmax, ph in parse_phones(tg):
        ph = ph.strip() or "SP"            # pauza -> fonemul de pauză SP
        d = round((float(xmax) - float(xmin)) * FPS)
        if d <= 0:
            continue
        if seq and seq[-1] == ph == "SP":
            durs[-1] += d                   # fuzioneaza pauzele vecine
        else:
            seq.append(ph); durs.append(d)
    if not seq:
        print("[gol]", name); continue
    # !!! TODO comun: maparea fonemelor MFA -> alfabetul tau RECLIST-RO (o facem impreuna, pas scurt)
    shutil.copy2(wavs[name], os.path.join(out_dir, "raw", "wavs", os.path.basename(wavs[name])))
    rows.append([name, " ".join(seq), " ".join(str(x) for x in durs)])

with open(os.path.join(out_dir, "raw", "transcriptions.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "ph_seq", "ph_dur"])
    w.writerows(rows)

print("GATA:", len(rows), "segmente ->", os.path.join(out_dir, "raw", "transcriptions.csv"))
```

**Cum lucrezi:**
```cmd
cd /d D:\BANCA-VOCE\scrise
python textgrid2csv.py D:\BANCA-VOCE\04_aliniat D:\BANCA-VOCE\03_corpus D:\BANCA-VOCE\05_dataset
```

**Rezultat așteptat:** `05_dataset\raw\transcriptions.csv` + `05_dataset\raw\wavs\*.wav`, arătând așa:

```
name,ph_seq,ph_dur
seg_0001,SP m a SP,5 12 9 4
seg_0002,SP b u n ă SP,5 10 11 8 5
```
*(fonemele deocamdată sunt în alfabetul MFA; pasul următor îl facem împreună: mapare rapidă către RECLIST-RO — fișier de mapare + re-rularea scriptului.)*

---

## 9. ETAPA 7 — Verificarea etichetelor (vLabeler / OpenUTAU)

**Ce e:** ultima plasă de siguranță înainte de GPU: asculți și vezi dacă timpii se potrivesc cu sunetul.

**Cum lucrezi:**
1. Deschizi **vLabeler** (`C:\MY_TOOLS\vLabeler`) și încarci setul/segmentele — treci în ritm de control pe mostre (10–20% din segmente; inspecți integrală doar dacă vezi probleme repetate).
2. Ce corectezi: foneme greșite (cuvinte pe care Whisper le-a scris greșit se văd și se repară la Etapa 4–5), limite de timp evident deplasate.
3. **OpenUTAU** (https://openutau.com/) — îl instalezi mai târziu, pentru proba finală a vocii antrenate.

**Regula de aur aici:** **corectezi puțin și repede, nu perfecționezi la nesfârșit** — modelul toleră mici imprecizii de limită; toleranța lui pentru **foneme greșite** e zero.

---

## 10. ETAPA 8 — Instalarea DiffSinger

**Ce e:** repo-ul openvpi conține tot: binarizarea, antrenamentul, inferența.

**De unde:** https://github.com/openvpi/DiffSinger

**Cum lucrezi (cmd):**
```cmd
cd /d D:\BANCA-VOCE
git clone https://github.com/openvpi/DiffSinger.git
cd DiffSinger
git submodule update --init --recursive
```
*(submodulele sunt obligatorii — fără ele lipsește cod esențial)*

```cmd
python -m venv venv
venv\Scripts\activate
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```
- Aștepți `True NVIDIA GeForce GTX 1660 SUPER` → placa e văzută corect.
- Dacă `requirements.txt` lipsește/alt nume, te uiți în README-ul repo-ului la secțiunea de instalare (se schimbă ușor între versiuni — spune-mi și-ți spun exact).

**Rezultat așteptat:** folderul `DiffSinger` complet, cu venv activat și PyTorch care vede GPU-ul.

---

## 11. ETAPA 9 — Binarizarea (set → fișiere pentru GPU)

**Ce e:** `binarize.py` citește wav-urile + `transcriptions.csv` și extrage automat spectogramele (mel) și F0 (înălțimea vocii) în fișiere binare `.data` — formatul pe care-l mănâncă antrenamentul.

**Cum lucrezi:**
1. Intri în repo și **copiezi un config exemplu care conține „acoustic" în nume** (folderul `configs/` din repo — deschizi, te uiți, copiezi) — nu scrii de la zero; schimbi doar **căile**:
   - calea către set: `D:/BANCA-VOCE/05_dataset` (cu liniuțe, nu cu bine)
   - `binary_data_dir`: `D:/BANCA-VOCE/06_binar`
2. Rulezi (cu venv activat, din folderul repo-ului):
```cmd
python scripts/binarize.py --config configs\calea\configului_tau.yaml
```
3. Verifici că în `06_binar` au apărut fișiere `.data` / `.meta`.

**Atenție (pas comun, de făcut împreună):** în config există lista de **foneme a limbii** (dicționarul de foneme). Acolo intră **alfabetul RECLIST-RO** — adică trecerea pe care am lăsat-o ca TODO la Etapa 6. Când ajungi aici, îmi spui și-ți pregătesc eu fișierul de mapare + modificările exacte din config.

---

## 12. ETAPA 10 — ANTRENAREA PE GPU

**Ce e:** modelul „citește" datele mii de ori și își ajustează parametrii. Tu pornești comanda și urmărești progresul.

### 12.1 Pornești de la un model deja învățat (warm-start) — recomandat

**Ce e:** în locul unui antrenament de la zero (săptămâni), iei un model DiffSinger **pre-antrenat de comunitate** (limbi străine) și îl **adaptezi** pe vocea ta — mult mai rapid și mai puțin date necesare.
**De unde:** în discuțiile repo-ului openvpi există categorie de partajare a modelelor pre-antrenate: https://github.com/openvpi/DiffSinger/discussions (cauți „pretrained"/„warm-start"). Descarci `.ckpt`-ul și-l pui în `D:\BANCA-VOCE\07_modele`.

### 12.2 Comanda de antrenament

```cmd
cd /d D:\BANCA-VOCE\DiffSinger
venv\Scripts\activate
python scripts/train.py --config configs\calea\configului_tau.yaml --exp_name vocea_ro
```
- **FP16:** se activează în config (cheie de tip `precision: 16`) — pe placa ta, **obligatoriu**.
- **Lotul (batch):** în config există un `max_batch_frames` — pe 6 GB îl scazi până nu mai dă eroare de memorie (ex. încerci valori mai mici: dacă pica, înjumătățești). **Nu afectează calitatea finală, doar viteza/stabilitatea pașilor.**
- **Urmărești:** folderul de loguri din repo se deschide cu **TensorBoard** (`tensorboard --logdir logs` în altă fereastră cmd, apoi http://localhost:6006) — vezi curba de „loss" (mai jos = mai bine).

### 12.3 Cât durează & pe cine folosești

| Situație | Ce faci |
|---|---|
| Testare acum, pe PC-ul tău | Rulezi 10–20 min, te uiți că nu dă eroare, oprești (Ctrl+C) — **ziua configurării** |
| Antrenament complet pe a ta (6 GB) | Lasă să meargă **zile** (warm-start FP16); PC-ul poate rămâne ocupat; nu e nicio problemă de calitate |
| Viteză maximă | Închiriezi GPU 24 GB (linkurile la §0), urci `05_dataset` + configul, aceleași comenzi, descarci `.ckpt` |

### 12.4 Inferența (prima probă)

```cmd
python scripts/infer.py acoustic FISIER.ds --exp vocea_ro
```
- Fișierul `.ds` = text + note muzicale pentru care vrei voce — pentru primul test ți-l pregătesc eu (sau iei un exemplu din folderul `examples/` al repo-ului).
- Ieșirea: un `.wav` cu vocea ta cântând. **Verifici:** românesc? corect pronunțat? aceeași identitate vocală? Dacă da → ai trecut.

---

## 13. CHECKLIST FINAL

- [ ] `01_curat`: toate `1 MONO | 16`, 44,1 kHz, fără muzică
- [ ] `02_segmente`: audiate, fără tăieturi în cuvinte
- [ ] `.txt`-uri corectate (Whisper + tine)
- [ ] `mfa align` → TextGrid pentru fiecare segment (erari = segmente scoase, nu întreg lotul)
- [ ] `transcriptions.csv` generat, ~N segmente = ~N wav-uri în `raw/wavs`
- [ ] Mapare foneme → RECLIST-RO făcută (pas împreună)
- [ ] Verificare vLabeler pe mostre
- [ ] `binarize` → `.data` în `06_binar`
- [ ] `train.py` pornește, loss-ul scade în TensorBoard
- [ ] Inferența sună românește

## 14. REGULI DE AUR (repetarea nu strică)

1. **Datele + etichetele fac calitatea; GPU-ul face viteza.**
2. Mono · 44,1 kHz · **16-bit la final** (dither) · aceeași rețetă de prelucrare la toate fișierele.
3. Un singur tăiat de verificare după fiecare automatizare — automatul greșește o dată, tu prinzi o dată.
4. **Niciodată** modele G2P/de altă limbă pe datele românești — de aici apar accentele străine.
5. Când ceva nu corespunde ghidului (nume de comenzi/configuri se mai schimbă între versiuni) — **întreabă înainte să improvizezi**.

---
*Ghid bazat pe: documentația oficială MFA (instalare conda/Miniforge), Romanian MFA Bundle (Vargo 2026), openvpi/MakeDiffSinger, openvpi/dataset-tools + flutydeer/audio-slicer (GUI Windows), openvpi/DiffSinger. Pasii cu „împreună" (mapare foneme, config finală, primul .ds) îi finalizăm la momentul potrivit.*
