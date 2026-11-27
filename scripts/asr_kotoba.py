"""手元の音声認識(kotoba-tech/kotoba-whisper-v2.0)で、ナレーションの読みを確かめる。
  python scripts/asr_kotoba.py cache/short_solo_<slug> <出力txt>
cache/short_solo_<slug>/n_00.wav 〜 n_NN.wav(BGMなしの元ナレーション)を、1つずつ文字起こしして出力に書く。
使い方の注意:
  ・稀な語・同音語(冬至→当時、新嘗祭→ニーナメサイ、四苦八苦→宿泊区、亥の日→井の日、勅令→直礼)はずれる。数字・日付が台本と一致するかが主な確認。
    読み自体は out/short_solo_<slug>_kana.txt(VOICEVOXに渡す読み仮名)が正で、ASRのずれは「聞き取りのぶれ」として扱う。
  ・初回はモデルをダウンロードする(1本2〜4分)。pip: transformers torch soundfile numpy(torchaudioは無くてよい。リサンプルは np.interp)。
  ・Chromeのタブや並行ビルドを減らす(メモリ)。
"""
import sys, glob, os
import numpy as np
import soundfile as sf
import torch
from transformers import pipeline

src, out = sys.argv[1], sys.argv[2]
files = sorted(glob.glob(os.path.join(src, 'n_*.wav')))
asr = pipeline('automatic-speech-recognition', model='kotoba-tech/kotoba-whisper-v2.0', torch_dtype=torch.float32, device='cpu',
               model_kwargs={}, chunk_length_s=15)
lines = []
for f in files:
    wav, sr = sf.read(f)
    if wav.ndim > 1:
        wav = wav.mean(axis=1)
    if sr != 16000:
        n = int(len(wav) * 16000 / sr)
        wav = np.interp(np.linspace(0, len(wav) - 1, n), np.arange(len(wav)), wav)
    r = asr({'raw': wav.astype(np.float32), 'sampling_rate': 16000}, generate_kwargs={'language': 'ja', 'task': 'transcribe'})
    lines.append(f"{os.path.basename(f)}: {r['text'].strip()}")
    print(lines[-1], flush=True)
open(out, 'w', encoding='utf8').write('\n'.join(lines))
print('done')
