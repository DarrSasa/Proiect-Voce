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
        ↓                        ETAPA 11: ambalare ca singer OpenUTAU (ONNX + structură)
   model .ckpt                    ↓                        ETAPA 12: phonemizerul românesc (dsdict-ro + plugin)
        ↓                        apoi: testul de pronunție în OpenUtau Lunai
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

## 5. ETAPA 3 — Tăierea în segmente (5A rapidă / 5B AudioSlicer)

> **Ordinea recomandată e inversă celei clasice:** transcrii **O DATĂ** întregul fișier → tai pe timestamp-uri → textul vine **lipit** de fiecare clip. Rezultă Etapa 3 + Etapa 4 dintr-un singur pas. (Varianta clasică AudioSlicer rămâne la 5B, mai jos.)

### 5A. VARIANTA RAPIDĂ — `taie_si_transcrie.py` (recomandată)

**De ce:** dacă tai întâi în sute de clipuri mici și apoi transcrii/verifici fiecare, pierzi timp potrivind textele. Aici:
1. **WhisperDesktop (sau scriptul) transcrie întregul fișier o dată** — ai text + timestamp-uri;
2. scriptul **taie audio-ul pe timestamp-uri și lipește granitele de liniștile reale** (în centrul pauzei — **nu taie niciodată în cuvânt**; dacă granita cade în vorbire, nu o mută);
3. scrie automat **`nume_0001.wav` + `nume_0001.txt`** (perechi, direct pentru MFA) + **`REVIEW_nume.txt`**.

**Despre timestamp-urile din exemplul tău:** apar pe **fraze** (8–18 s), nu după fiecare liniște — e comportamentul normal al Whisper (grupează după propoziție). Nu e obstacol: scriptul acceptă exact formatul `[00:01:23.456 --> 00:01:31.000] text` de la WhisperDesktop și îl aliniază cu liniștile din audio.

**Ce faci la verificare (în loc să asculți tot):** deschizi `REVIEW_*.txt`, **citești** textele (câteva minute pe fișier) și asculți **doar** liniile dubioase. Ascultarea aprofundată rămâne la Etapa 7 (vLabeler) — acolo e locul ei.

**Instalare (o singură dată):** `pip install faster-whisper` — necesară **doar** pentru fisierele **fără** `.txt` (scriptul transcrie singur). Dacă ai deja transcrieri WhisperDesktop pentru tot, nu instalezi nimic în plus. `ffmpeg` (§2) doar pentru non-wav.

**Comenzi (în cmd):**

```cmd
REM 1) Ai deja .txt de la WhisperDesktop:
python taie_si_transcrie.py --audio "C:\cale\fisier.wav" --txt "C:\cale\fisier.txt" --out "D:\BANCA-VOCE\03_corpus"

REM 2) Fără .txt — pornește singur Whisper (limba română, VAD):
python taie_si_transcrie.py --audio "C:\cale\fisier.wav" --out "D:\BANCA-VOCE\03_corpus"

REM 3) TOATE cele 57 de fișiere dintr-un dat (cu sau fără .txt — le potrivește el):
python taie_si_transcrie.py --folder "D:\BANCA-VOCE\01_curat" --out "D:\BANCA-VOCE\03_corpus"
```

**Parametri utili:** `--prag -45` (prag de liniște dBFS; `-40` dacă fundalul e zgomotos, `-55` dacă e curat) · `--model small` (modelul Whisper pentru fisierele fără txt; `medium` = mai exact, mai lent).

**Scriptul complet** — același conținut ca fișierul `taie_si_transcrie.py` livrat; salvează-l ca fișier pe PC-ul tău:

```python
# -*- coding: utf-8 -*-
r"""
taie_si_transcrie.py — ETAPA 3+4 intr-un singur pas (varianta rapida)
=====================================================================
In loc sa tai in sute de clipuri si apoi sa transcrii/verifici fiecare clip,
transcrii INTREGUL fisier o singura data, apoi il tai pe timestamp-uri:
fiecare segment primeste automat .wav + .txt cu acelasi nume (gata pentru MFA).

Intrari acceptate:
  - .txt in formatul WhisperDesktop ("text with timestamps"):
        [00:01:23.456 --> 00:01:31.000]  textul...
  - sau fara .txt: ruleaza el Whisper (limba romana) — trebuie
    pip install faster-whisper (daca ai instalat deja ghidul, e gata).

Iesiri (in folderul --out):
  - sursa_0001.wav + sursa_0001.txt   (perechi, direct pentru MFA)
  - sursa_0002.wav + sursa_0002.txt
  - ...
  - REVIEW_sursa.txt -> "0001 | 00:01:23-00:01:31 | textul"
    (citesti TEXTUL aici in 2 minute; asculti doar liniile dubioase.)

Utilizare (in cmd!):
  # 1) Ai deja transcriptia de la WhisperDesktop (cea cu --> ):
  python taie_si_transcrie.py --audio "C:\BANCA\01_curat\fisier.wav" --txt "C:\...\fisier.txt" --out "C:\BANCA\03_corpus"

  # 2) Fara transcriptie (porneste singur Whisper, limba ro):
  python taie_si_transcrie.py --audio "C:\BANCA\01_curat\fisier.wav" --out "C:\BANCA\03_corpus"

  # 3) TOATE fisierele dintr-un folder (cu sau fara .txt — le gaseste el):
  python taie_si_transcrie.py --folder "C:\BANCA\01_curat" --out "C:\BANCA\03_corpus"

Note:
  - Fisierele trebuie sa fie MONO, 16-bit (Etapa 1-2). Daca vreunul e stereo,
    scriptul il sareste cu mesaj (alegi tu canalul — vezi ghidul).
  - ffmpeg e necesar DOAR daca .audio-ul nu e .wav.
  - --prag -45 (dBFS) = cat de linistit e ca sa taie acolo. Creste la -40
    daca fundalul e zgomotos, coboara la -55 daca e foarte curat.
  - NU pierde continut: segmentele mici se lipesc de vecine, textele se pastreaza.
"""
import argparse, os, re, sys, glob, shutil, subprocess, tempfile, wave
import numpy as np

TS = re.compile(
    r"\[(\d+):(\d{2}):(\d{2}[.,]\d{1,3})\s*-->\s*(\d+):(\d{2}):(\d{2}[.,]\d{1,3})\]\s*(.*)"
)

class SkipFile(Exception):
    pass

# ---------- utilitare ----------
def t2f(hms):
    h, m, s = hms.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

def fmt_t(t):
    m, s = divmod(t, 60.0)
    return "%02d:%05.2f" % (m, s)

def sanitize(name):
    return "".join(c if (c.isalnum() or c in "-_") else "_" for c in name).strip("_")

def load_wav(path):
    if path.lower().endswith(".wav"):
        src, tmp = path, None
    else:
        if not shutil.which("ffmpeg"):
            raise SkipFile("nu e .wav si nu gasesc ffmpeg in PATH — instaleaza ffmpeg (gyan.dev, §2) sau converteste intai")
        tmp = tempfile.mktemp(suffix=".wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, tmp], check=True)
        src = tmp
    try:
        w = wave.open(src, "rb")
        sr, nch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        data = w.readframes(n)
        w.close()
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    if sw != 2:
        raise SkipFile("nu e 16-bit (%d octeti/esantion) — converteste la 16-bit (Etapa 2)" % sw)
    if nch != 1:
        raise SkipFile("%d canale — trebuie MONO; alege intai canalul (Etapa 1)" % nch)
    return sr, np.frombuffer(data, dtype="<i2").copy()

def silences(x, sr, prag_db=-45.0, min_dur=0.12):
    hop = max(1, int(sr * 0.01))
    n = len(x) // hop
    if n == 0:
        return []
    frames = x[: n * hop].astype(np.float32).reshape(n, hop)
    rms = np.sqrt((frames ** 2).mean(axis=1) + 1e-12)
    db = 20.0 * np.log10(rms / 32768.0 + 1e-12)
    quiet = db < prag_db
    out, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) * 0.01 >= min_dur:
                out.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return out

def snap(t, sils):
    """Daca granita cade intr-o liniste → o mutam la centrul linistii (taie curat,
    niciodata in cuvant). Daca granita e in vorbire → NU o misca (fara pierderi)."""
    cands = [0.5 * (a + b) for a, b in sils if a <= t <= b]
    if not cands:
        return t
    return min(cands, key=lambda c: abs(c - t))

# ---------- mode A: parsare WhisperDesktop ----------
def segments_from_txt(path):
    segs = []
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            m = TS.search(line)
            if m:
                s = t2f("%s:%s:%s" % m.group(1, 2, 3))
                e = t2f("%s:%s:%s" % m.group(4, 5, 6))
                txt = m.group(7).strip()
                if e - s > 0.05:
                    segs.append([s, e, txt])
    if not segs:
        raise SkipFile("nu am gasit linii de tip [00:00:00.000 --> 00:00:00.000] in txt")
    return segs

# ---------- mode B: Whisper ----------
def segments_from_whisper(audio, model_name):
    from faster_whisper import WhisperModel
    print("   Whisper '%s' (prima rulare poate descarca modelul)..." % model_name)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    stream = model.transcribe(
        audio,
        language="ro",
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        word_timestamps=True,
        condition_on_previous_text=False,
    )
    segs = []
    for s in stream:
        txt = (s.text or "").strip()
        if not txt:
            continue
        segs.append([float(s.start), float(s.end), txt, list(s.words or [])])
    if not segs:
        raise SkipFile("Whisper nu a gasit vorbire")
    return segs

def split_at_pauses(segs, sils, min_pause=0.45):
    """Imparte segmentele lungi la liniștile interioare, cu textul impartit pe cuvinte."""
    out = []
    for s, e, txt, words in segs:
        if not words:
            out.append([s, e, txt])
            continue
        inner = [0.5 * (a + b) for a, b in sils
                 if s + 0.25 < 0.5 * (a + b) < e - 0.25 and (b - a) >= min_pause]
        cuts = [s] + sorted(inner) + [e]
        for k in range(len(cuts) - 1):
            a, b = cuts[k], cuts[k + 1]
            if b - a < 0.10:
                continue
            ws = [w for w in words if a <= (w.start + w.end) / 2.0 < b]
            part = "".join(w.word for w in ws).strip() if ws else ""
            if not part:
                continue  # bucata de liniste fara cuvinte — nu scrie nimic (fara pierdere de text)
            out.append([a, b, part])
    if not out:
        out = [[s, e, txt] for s, e, txt, _ in segs]
    return out

# ---------- construirea clipurilor (fara pierderi) ----------
def make_clips(segs, b, dur):
    clips = []
    for i, (s, e, txt) in enumerate(segs):
        t0 = b[i]
        t1 = b[i + 1] if i + 1 < len(b) else dur
        clips.append([t0, max(t1, t0), txt])
    # 1) un text gol se lipeste de vecin (continutul audio ramane!)
    merged = []
    for c in clips:
        if not c[2] and merged:
            merged[-1][1] = max(merged[-1][1], c[1])
        elif not c[2]:
            merged.append(c)  # eventualul prim cu text gol — rezolvat mai jos
        else:
            merged.append(c)
    if merged and not merged[0][2] and len(merged) > 1:
        merged[1][0] = merged[0][0]
        merged[1][2] = merged[0][2]
        merged.pop(0)
    # 2) clipurile mai mici de 0.35 s se lipesc de precedentul (audio + text)
    out = []
    for c in merged:
        if out and (c[1] - c[0]) < 0.35:
            out[-1][1] = max(out[-1][1], c[1])
            out[-1][2] = (out[-1][2] + " " + c[2]).strip()
        else:
            out.append(c)
    if len(out) >= 2 and (out[0][1] - out[0][0]) < 0.35:
        out[1][0] = out[0][0]
        out[1][2] = (out[0][2] + " " + out[1][2]).strip()
        out.pop(0)
    # 3) curatenie finala
    out = [c for c in out if c[1] > c[0] + 0.05 and c[2].strip()]
    out[0][0] = max(0.0, out[0][0])
    out[-1][1] = min(dur, out[-1][1])
    return out

def main():
    ap = argparse.ArgumentParser(description="Etapa 3+4: transcrie o data, taie pe timestamp-uri, scrie wav+txt perechi.")
    ap.add_argument("--audio")
    ap.add_argument("--txt")
    ap.add_argument("--folder")
    ap.add_argument("--txt-dir", help="folder cu .txt-urile de la WhisperDesktop (daca difera de folderul audio)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--prag", type=float, default=-45.0, help="prag liniste dBFS (implicit -45)")
    ap.add_argument("--model", default="small", help="model Whisper pt fisierele fara .txt (implicit small)")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    jobs = []
    if a.folder:
        audios = []
        for ext in ("*.wav", "*.mp3", "*.flac", "*.m4a", "*.ogg"):
            audios += glob.glob(os.path.join(a.folder, ext))
        audios.sort()
        if not audios:
            sys.exit("Nu am gasit audio in %s" % a.folder)
        for au in audios:
            tdir = a.txt_dir or a.folder
            cand = os.path.join(tdir, os.path.splitext(os.path.basename(au))[0] + ".txt")
            jobs.append((au, cand if os.path.isfile(cand) else None))
    elif a.audio:
        jobs.append((a.audio, a.txt))
    else:
        ap.error("trebuie --audio sau --folder")

    total = 0
    for au, tx in jobs:
        base = sanitize(os.path.splitext(os.path.basename(au))[0])
        print("== %s ==" % os.path.basename(au))
        try:
            sr, x = load_wav(au)
            dur = len(x) / float(sr)

            if tx:
                segs = segments_from_txt(tx)
            else:
                segs = segments_from_whisper(au, a.model)
                segs = split_at_pauses(segs, silences(x, sr, a.prag))

            segs = [s for s in segs if s[1] > s[0] + 0.05]
            segs.sort(key=lambda s: s[0])
            segs[0][0] = max(0.0, segs[0][0])
            segs[-1][1] = min(dur, segs[-1][1])

            sils = silences(x, sr, a.prag)
            # granite: intre segmente = mijlocul spatiului dintre ele, "lipit" de liniste
            b = [snap(segs[0][0], sils)]
            for i in range(len(segs) - 1):
                b.append(snap(0.5 * (segs[i][1] + segs[i + 1][0]), sils))
            b.append(snap(segs[-1][1], sils))
            for i in range(len(b) - 1):
                if b[i + 1] <= b[i] + 0.05:
                    b[i + 1] = b[i] + 0.05
            b[0] = max(0.0, b[0])
            b[-1] = min(dur, b[-1])

            clips = make_clips(segs, b, dur)
        except SkipFile as e:
            print("   SARIT: %s" % e)
            continue
        except Exception as e:
            print("   EROARE: %s" % e)
            continue

        review = []
        for idx, (t0, t1, txt) in enumerate(clips, 1):
            name = "%s_%04d" % (base, idx)
            i0 = max(0, min(int(round(t0 * sr)), len(x)))
            i1 = max(i0 + 1, min(int(round(t1 * sr)), len(x)))
            w = wave.open(os.path.join(a.out, name + ".wav"), "wb")
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes(x[i0:i1].tobytes())
            w.close()
            with open(os.path.join(a.out, name + ".txt"), "w", encoding="utf-8") as f:
                f.write(txt.strip())
            review.append("%s | %s-%s | %s" % (name[-4:], fmt_t(t0), fmt_t(t1), txt.strip()))
            total += 1

        rv = os.path.join(a.out, "REVIEW_%s.txt" % base)
        with open(rv, "w", encoding="utf-8") as f:
            f.write("REVIEW pentru %s — citesti textul; asculti doar liniile dubioase:\n\n"
                    % os.path.basename(au))
            f.write("\n".join(review) + "\n")
        print("   %d segmente (wav+txt) + %s" % (len(review), os.path.basename(rv)))

    print("\nTOTAL: %d segmente (wav+txt) in %s" % (total, a.out))
    if total == 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Testul din fabrică (făcut de mine):** granita mutată intenționat în liniște → s-a centrat în pauză (8.50 / 16.80 / 31.00), acoperire audio = 39.15 s din 39.15 s utili (**zero conținut pierdut**), 4 perechi wav+txt + REVIEW scrise corect, format ieșire: mono · 16-bit · 44,1 kHz.

### 5B. VARIANTA CLASICĂ — AudioSlicer pas cu pas (tăiere fără text)


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

> **Dacă ai folosit varianta 5A:** NU mai urmezi pașii de aici — `.txt`-urile sunt deja scrise lângă fiecare wav (perechi gata pentru MFA). Capitolul rămâne pentru varianta clasică (5B) și pentru refaceri punctuale.


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

## 13. ETAPA 11 — AMBALAREA VOCII CA SINGER OPENUTAU (structura Llane Crow)

Modelul `.ckpt` e pentru Python. OpenUtau Lunai vrea **ONNX + fișiere de configurare**. Șablonul nostru = **structura exactă a vocii Llane Crow v170** (verificată fișier cu fișier pe PC-ul tău — vocea ta va arăta la fel și va apărea în lista Singers din Lunai).

### 13.1 Export ONNX (cu mediul venv al DiffSinger activat)

```cmd
cd /d D:\BANCA-VOCE\07_modele\DiffSinger
venv\Scripts\activate
python scripts/export.py acoustic --exp vocea_ro
```

- Exportul produce **`acoustic.onnx`** (modelul pentru OpenUTAU) + un **`dsconfig.yaml`** generat automat. Consola îți spune exact unde le scrie (caută un folder `export` sub `logs\vocea_ro`).
- Variante de argumente (`onnx_version`, `opset_version`) ai le lasă pe default la prima încercare.

### 13.2 Structura folderului singer (oglim Llane 1:1)

Creezi `C:\Users\adudc\Documents\OpenUtau\Singers\VoceaRo\` și copiezi ce urmează:

```
VoceaRo\
├── configs\
│   ├── character.yaml          ← identitatea vocii (mai jos, 13.3)
│   ├── dsconfig.yaml           ← cel exportat + câmpurile din șablon (13.4)
│   ├── icon.png                ← poză (opusțional)
│   └── dsdur\
│       └── dsdict-ro.yaml      ← dicționarul fonemizerului (Etapa 12)
├── files\
│   ├── acoustic.onnx           ← de la 13.1
│   ├── phonemes.json           ← alfabetul vocii (13.5)
│   ├── languages.json          ← {"ro": 1} (13.5)
│   └── dictionary-ro.txt       ← dicționar cuvinte→foneme (Etapa 12)
└── tgm_hifigan\                ← vocoderul: COPIEZI folderul din Llane_Crow_v170
                                   (tgm_hifigan_v110.onnx + documents\) — e standard,
                                   nu-l generezi tu
```

**De ce copiem structura Llane:** ea funcționează în OpenUtau Lunai 0.2.1.0 — dovedit. Nu improviza alte căi.

### 13.3 `configs\character.yaml` (conținut minimal)

```yaml
name: Vocea Ro
image: icon.png
default_phonemizer: <clasa phonemizerului românesc — o punem în Etapa 14>
singer_type: diffsinger
text_file_encoding: utf-8
```

(Lipsește `subbanks:` — alea sunt pentru voci cu stiluri/embeddri; a noastră are un singur stil.)

### 13.4 `configs\dsconfig.yaml` (câmpuri esențiale — restul le copiezi din șablonul Llane)

```yaml
acoustic: ../files/acoustic.onnx
phonemes: ../files/phonemes.json
languages: ../files/languages.json
vocoder: dsvocoder

sample_rate: 44100
hop_size: 512
use_lang_id: true
num_lang: 1

dictionaries:
  ro: ../../files/dictionary-ro.txt
```

Plus rândurile de stil din Llane (`hidden_size`, `win_size`, `fft_size`, `mel_*`…) — **le copiezi exact** din `dsconfig.yaml` al lui Llane, că sunt legate de arhitectura modelului.

### 13.5 `files\languages.json` și `files\phonemes.json`

```json
{ "ro": 1 }
```

`phonemes.json` = **inventarul vocii cu ID-uri**, în ordinea etichetelor de antrenament:

```json
{
  "AP": 1,
  "SP": 2,
  "ro/a": 3,
  "ro/ă": 4,
  "ro/â": 5,
  "...": "toate fonemele RECLIST-RO, fiecare cu ID-ul lui"
}
```

- De obicei **îl generează exportul/ambalarea**; dacă nu, îl facem din RECLIST-RO (pas împreună).
- **Regulă tare:** orice fonem folosit în `dsdict-ro.yaml` care NU e declarat aici → **e ignorat silențios** (fără eroare, cuvântul pur și simplu nu sună).

---

## 14. ETAPA 12 — PHONEMIZERUL ROMÂNESC (diacritice, „i" moale, copiii…)

### 14.1 Cum funcționează — fapte verificate (wiki OpenUTAU + codul sursă + exemple reale)

1. **Phonemizerele sunt în PROGRAM**, nu în folderele cu voci:
 - cele integrate (ex. `OpenUtau.Core.DiffSinger.DiffSingerPhonemizer` = „DiffSinger Default Phonemizer") sunt în fișierele programului;
 - cele „Contributed by…" = fișiere **`.dll` puse în folderul `Plugins\` de lângă `OpenUtau.exe`**, apoi repornești programul. (Exemplu real: phonemizerul taiwanez se instalează exact așa.)
2. **Vocea ține datele**: `configs\dsdur\dsdict-<cod limbă>.yaml` — pentru noi **`dsdict-ro.yaml`** — cu două secțiuni **obligatorii**:
 - `symbols:` — TIPUL fiecărui fonem (`vowel`, `semivowel`, `stop`, `fricative`, `affricate`, `nasal`, `liquid`) — OpenUTAU are nevoie de el ca să împartă silabele;
 - `entries:` — dicționarul **cuvânt → secvență de foneme**.
3. **Două capcane silențioase (verificate în practica comunității):**
 - dsdict **fără `symbols:` complet → TOTUL eșuează**;
 - o intrare care folosește un fonem **nedeclarat în `phonemes.json` → este omisă fără niciun mesaj de eroare**.
4. Dacă lipsește `dsdict-ro.yaml`, OpenUTAU caută `dsdict.yaml` generic. Denumirile fonemizerelor din lista ta urmăresc codul limbii (`dsdict-en`, `dsdict-ru`…) — al nostru = **`dsdict-ro`**.
5. În lista Lunai (17 limbi) **româna lipsește** → o adăugăm, exact cum au făcut ceilalți cu „Contributed by…".

### 14.2 Planul nostru în două părți

**A. Datele în voce — generate de script (ți-l scriu eu: `genereaza_dsdict_ro.py`):**

Intrări: RECLIST-RO + regulile G2P (14.3) + lexiconul (cuvintele din textele tale + excepții). Ieșiri: `dsdict-ro.yaml` + `dictionary-ro.txt`.

Schelet `configs\dsdur\dsdict-ro.yaml` (exemple reale, cu formatarea corectă):

```yaml
symbols:
- {symbol: SP,  type: vowel}
- {symbol: AP,  type: vowel}
- {symbol: ro/a, type: vowel}
- {symbol: ro/ă, type: vowel}
- {symbol: ro/â, type: vowel}
- {symbol: ro/e, type: vowel}
- {symbol: ro/i, type: vowel}
- {symbol: ro/o, type: vowel}
- {symbol: ro/u, type: vowel}
- {symbol: ro/j, type: semivowel}   # „i"-ul moale (flori, copiii)
- {symbol: ro/p, type: stop}
- {symbol: ro/f, type: fricative}
- {symbol: ro/ș, type: fricative}
- {symbol: ro/ț, type: affricate}   # /ts/
- {symbol: ro/c, type: stop}
- {symbol: ro/l, type: liquid}
- {symbol: ro/m, type: nasal}
- {symbol: ro/r, type: liquid}
- {symbol: ro/n, type: nasal}
- {symbol: ro/o, type: vowel}
# ... TOATE celelalte din RECLIST-RO — complet, altfel pică în silențiu

entries:
- {grapheme: SP, phonemes: [SP]}
- {grapheme: AP, phonemes: [AP]}
- {grapheme: flori,   phonemes: [ro/f, ro/l, ro/o, ro/r, ro/j]}
- {grapheme: copiii,  phonemes: [ro/c, ro/o, ro/p, ro/i, ro/j, ro/j]}
- {grapheme: mamă,    phonemes: [ro/m, ro/a, ro/m, ro/ă]}
- {grapheme: cântec,  phonemes: [ro/c, ro/â, ro/n, ro/t, ro/e, ro/c]}
- {grapheme: gheață,  phonemes: [ro/g, ro/h, ro/e, ro/ț, ro/ă]}
- {grapheme: taxi,    phonemes: [ro/t, ro/a, ro/k, ro/s, ro/i]}  # excepție: i vocală
```

**B. Motorul — două planuri, în ordinea asta:**

1. **Proba 1 (fără cod):** selecționezi vocea + „DiffSinger Default Phonemizer" și scrii un cuvânt — dacă preia `dsdict-ro.yaml`, gata.
2. **Proba 2 (calea cu precedente dovedite):** dacă nu preia → **plugin `.dll` „DiffSinger Romanian Phonemizer"** în folderul `Plugins\` al Lunai (se construiește pe clasa de bază DiffSinger a programului; eu ți-l scriu și ți-l compilez — trebuie țintit pe .NET 8, cât e Lunai). Îl copiezi în `Plugins\`, repornești, alegi phonemizerul din listă.

În `character.yaml`, `default_phonemizer:` primește clasa pluginului → vocea deschide direct phonemizerul românesc.

### 14.3 Regulile G2P românești (nucleul scriptului)

| Caz | Regulă | Exemplu |
|---|---|---|
| Diacritice „duble" Unicode | `ș`/`ț` cu virgulă (U+0219/021B) ȘI virgulă cedilată veche (U+015F/0163) → ambele normalizează la `ș`/`ț`, **niciodată** la `s`/`t` | „cafea cu șerbet" ≠ „serbet" |
| `ă` | fonem distinct `ro/ă` | mamă → `m a m ă` |
| `â`, `î` | același fonem `ro/â` | cânt → `c â n t` |
| `c`,`g` + `e`,`i` | moi: `ce`,`ci`,`ge`,`gi` | cer, geam |
| `che`,`chi`,`ghe`,`ghi` | `h` anulează moliciunea → k/g tari + vocală | gheață, chem |
| `i` moale final după consoană | nu e vocală → `ro/j` | **flori → f l o r j** |
| `-ii` / `-iii` | un `i` vocală + glide `j` | **copii → c o p i j ; copiii → c o p i j j** |
| `i` vocală (nucleu de silabă) | `ro/i` | mașină, copil |
| Diftonguri (`ăi ei oi ui ia ie io iu ău`…) | rămân grupuri, NU palatalizare | tăi → `t ăi` |
| Cuvinte străine | dicționar de excepții (i rămâne vocală) | taxi |
| Punctuație / cratimă | se ignoră / cratima = graniță de cuvânt | „Ți-a" → `ț i` + `a` |

Decizia de design (reprezentarea finală a „i"-ului moale și a grupurilor CV) o legăm de forma RECLIST-RO la pasul de mapare — **același alfabet în: etichetele de antrenament = `phonemes.json` = `dsdict-ro.yaml`**. Dacă difere unul → accente străine sau silențiu.

### 14.4 Testul de pronunție (după ce am ambele părți)

1. Repornești OpenUtau Lunai → vocea **Vocea Ro** apare în Singers.
2. Scrii pe note cuvintele-probă și asculți: **flori, copiii, mamă, cântec, gheață, chemare, taxi, zâmbet**.
3. Verifici: se aude ă-ul din „mamă"? „â"-ul din „cântec"? i-ul moale din „flori"? „copiii" cu trei de i? Dacă da → phonemizerul e gata.

---

## 15. CHECKLIST FINAL

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
- [ ] `scripts/export.py acoustic` → `acoustic.onnx` + `dsconfig.yaml`
- [ ] Folder `VoceaRo` în `Singers` cu structura Llane (character/dsconfig/languages/phonemes/tgm_hifigan)
- [ ] `dsdict-ro.yaml` generat: `symbols` complet + `entries` (flori, copiii…)
- [ ] Phonemizerul românesc: proba cu Default → dacă nu, pluginul în `Plugins\`
- [ ] Testul de pronunție din 14.4 trece (ă, â, i-moale, -iii)

## 16. REGULI DE AUR (repetarea nu strică)

1. **Datele + etichetele fac calitatea; GPU-ul face viteza.**
2. Mono · 44,1 kHz · **16-bit la final** (dither) · aceeași rețetă de prelucrare la toate fișierele.
3. Un singur tăiat de verificare după fiecare automatizare — automatul greșește o dată, tu prinzi o dată.
4. **Niciodată** modele G2P/de altă limbă pe datele românești — de aici apar accentele străine.
5. Când ceva nu corespunde ghidului (nume de comenzi/configuri se mai schimbă între versiuni) — **întreabă înainte să improvizezi**.

---
*Ghid bazat pe: documentația oficială MFA (instalare conda/Miniforge), Romanian MFA Bundle (Vargo 2026), openvpi/MakeDiffSinger, openvpi/dataset-tools + flutydeer/audio-slicer (GUI Windows), openvpi/DiffSinger (scripts/export.py → ONNX), wiki-ul OpenUTAU (Phonemizers, Voicebank Development: dsdict symbols/entries, dicționar per limbă `dsdict-<cod>`), structura verificată a vocii Llane Crow v170 (LUNAI Project) + experiența comunității (asaxi-g2p: capcanele `symbols`/foneme nedeclarate). Pasii cu „împreună" (mapare foneme, `phonemes.json`, generatorul `dsdict-ro`, pluginul `.dll`, primul `.ds`) îi finalizăm la momentul potrivit.*
