# CERCETARE-INSTRUMENTE — bănci vocale fără microfon + unelte (2026-10-19)

Cercetare la cerere: site-uri comunitate DiffSinger + opțiuni TTS/alternative la înregistrare proprie.

---

## 1. Ce am găsit pe site-uri

### tigermeat.xyz/cast — „DiffSinger | TTS" la TIGER
- TIGER = singurul etichetat **„DiffSinger | TTS"**; restul: DiffSinger sau UTAU|DiffSinger.
- **TTS = mod de folosire, nu metodă de construcție:** DiffSinger e proiectat pentru cântat (SVS) **și** vorbit (TTS/DiffSpeech) — repo oficial MoonInTheRiver/DiffSinger: „SVS & TTS".
- TIGER e **construit clasic**: microfoane studio (Neumann TLM 103, AT4040, Rode NT1), antrenat de **UFR** (UTAU France), 6 vocal modes, Multi-Dict 11 limbi, Auto-Pitch.
- Modele înrudite (TRITON, DANROU, Miss Thera, Miyo, Canary…) — toate cu înregistrări reale.

### LabelMakr — etichetare AUTOMATĂ (cea mai importantă descoperire)
- GUI: **Whisper** (transcriere) + **SOFA** (aliniere forțată) → etichete HTK pentru DiffSinger.
- https://github.com/spicytigermeat/LabelMakr — **versiune portabilă Windows** în Releases.
- Suport total: EN, JA, ZH, FR, KO — **RO nu e oficial**, dar Whisper știe română, iar **SOFA acceptă G2P custom**.
- Rezerve: mVocalToolkit (WhisperX+SOFA+HubertFA), MFA, WhisperX, vLabeler manual.

### potluck-vocoder (github.com/mrtigermeat/potluck-vocoder)
- Vocoder PC-NSF-HiFiGAN pentru DiffSinger, **licență comercial-friendly** (donat de comunitate, 100+ ore date).
- NU se antrenează de la zero (24 GB VRAM, săptămâni) — **fine-tune pe datele tale** (`finetune_guide.md`).
- Pentru GPU 6 GB: fine-tune doar după ce modelul acustic e gata.

### utaufrance.com/voicebank
- Director comunitar mare: filtre Engine (UTAU/DiffSinger), Format (CV/CVVC), Gen, Limbă (13 — **fără română**). UFR antrenează TIGER și distribuie pachetele.

### coda-svs.org/characters (Team Coda, Coreea)
- KITANE, YEONU, CHIO, RANG, SAW, SaBi — DiffSinger, 9 limbi, 7 vocal modes, tutoriale postype.

### teambrapa.com.br (Brazilia)
- Bănci DiffSinger braziliene (MPB/Bossa/Samba); **eliberează public datasetul pe etape** („Dataset Release: Iteration 04").
- Rețea parteneri: Lunai, Coda, Tiger, nJokis, PRINTmov, NeoDiva, Misc Labs, Millefeuille.

### njokis-labs.carrd.co — modelul cel mai apropiat de cazul nostru
- Bănci spaniole din **înregistrări ale unor colaboratori VOLUNTARI** (nu angajați, nu microfonul propriu).
- **Corpus public** spaniol (acces pe formular) + unelte deschise: github.com/nJokisLabs.
- Non-comercial; credit obligatoriu la folosire.

### printmov.com (Tailanda)
- Vocal-synth UTAU/DeepVocal/DiffSinger Thai („Printto Magicbeat"); eliberează pluginuri, recliste, soluții.

---

## 2. Căi de a face un banc vocal FĂRĂ înregistrare proprie

| # | Calea | Calitate | Licență/etică |
|---|---|---|---|
| 1 | **TTS → corpus DiffSinger** (calea curentă) | ⭐⭐ (moștenește vocea TTS) | ✅ Piper CC-BY-NC; ❌ TTS corporativ (ToS) |
| 2 | **Corpusuri publice vorbire** (Common Voice RO CC0, corpus nJokis) | ⭐⭐⭐ vorbire; cântat „speechy" | ✅ cel mai curat etic |
| 3 | **Voluntar care cântă** (modelul nJokis) | ⭐⭐⭐⭐⭐ (bara Lunai) | ✅ consimțământ scris, fără bani |
| 4 | **Cântat AI online** (Flow/Suno) | ❌ | ❌ ToS + verdict deja dat |

- Băncuri din TTS se distribuie **doar cu permisiunea proprietarului TTS** (ex. Defoko = Aquestalk cu permisiune) — Piper/licențe deschise = ok, corporații = nu.

---

## 3. Tabel instrumente

| Instrument | Rol | Pentru noi |
|---|---|---|
| LabelMakr | etichetare auto (Whisper+SOFA), Windows portabil | ✅ prima încercare |
| SOFA | aliniere + G2P custom | ✅ bază pentru RO |
| MFA | aliniere pe dicționar (folosit de DiffSinger oficial) | ✅ rezervă |
| WhisperX / mVocalToolkit | word-timestamps + aliniere | ✅ rezervă |
| vLabeler | etichetare manuală | ✅ backup garantat RO |
| openvpi dataset tools | G2P labeling, slicing, MIDI | ✅ faza de date |
| Potluck Vocoder | vocoder final (fine-tune) | ✅ la final |
| Voicebank2DiffSinger | banc UTAU vechi → dataset DS | doar dacă apare un banc |

---

## 4. Planul recomandat (6 GB, zero microfon)

1. TTS + cele 25 fraze (`FRAZE-COMPLETE.md`, acoperire 141/141) — licență curată.
2. Etichetare: **LabelMakr** pe WAV-urile de fraze (textul îl știm deja!) → dacă SOFA nu acceptă RO → **MFA** → dacă nu → **vLabeler** (25 fraze = ore, nu zile).
3. Antrenare: openvpi DiffSinger, batch 1–2, FP16 (vezi `PLAN.md`).
4. Final: fine-tune **Potluck Vocoder**.
5. Atenție la așteptări: rezultat TTS = mai sintetic decât băncile cu studio real (TIGER/KITANE). Voluntar (modelul nJokis) = saltul spre bara Lunai, cu aceeași infrastructură.

## Surse (pagini vizitate)
tigermeat.xyz/projects/labelmakr/ · github.com/mrtigermeat/potluck-vocoder · tigermeat.xyz/cast/ · tigermeat.xyz/cast/tiger/ · utaufrance.com/voicebank/ · utaufrance.com/voicebank/tiger/ · coda-svs.org/characters · teambrapa.com.br · njokis-labs.carrd.co · printmov.com · github.com/spicytigermeat/LabelMakr · github.com/qiuqiao/SOFA · MoonInTheRiver/DiffSinger (SVS&TTS) · reddit r/utau (TTS voicebanks)
