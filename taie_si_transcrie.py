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
