"""Short の投稿パックを upload/short_<slug>/ に作る（動画・字幕・概要欄・タイトル・タグ）。
usage: python scripts/pack_short.py <slug> <long_pack>    例: pack_short.py sunrise 20_sunrise_solstice
       python scripts/pack_short.py <slug> --tags=江戸,地図,歴史  # 対応する長尺が無い単独Shorts
タイトルは「<title> 約N秒で確かめる #Shorts」。タグは長尺のタグ（または --tags の値）に Shorts を足す。"""
import json, re, shutil, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
_argv = [a for a in sys.argv[1:] if not a.startswith('--')]
_tags_opt = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--tags=')), None)
slug = _argv[0]
long_pack = _argv[1] if len(_argv) > 1 else None
if not long_pack and not _tags_opt:
    raise SystemExit('使い方: pack_short.py <slug> <long_pack> または pack_short.py <slug> --tags=a,b,c')
spec = json.loads((R / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
desc = (R / 'out' / f'short_{slug}_description.md').read_text(encoding='utf8')
sec = int(re.search(r'約(\d+)秒', desc).group(1))
d = R / 'upload' / f'short_{slug}'
d.mkdir(parents=True, exist_ok=True)
shutil.copyfile(R / 'out' / f'short_{slug}.mp4', d / 'video.mp4')
shutil.copyfile(R / 'out' / f'short_{slug}_subtitles.srt', d / 'subtitles_ja.srt')
(d / 'description.txt').write_text(desc, encoding='utf8')
title = f"{spec['title']} 約{sec}秒で確かめる #Shorts"
assert len(title) <= 100
(d / 'title.txt').write_text(title + '\n', encoding='utf8')
tags = _tags_opt or (R / 'upload' / long_pack / 'tags.txt').read_text(encoding='utf8').strip()
(d / 'tags.txt').write_text((tags + ', Shorts') if 'Shorts' not in tags else tags, encoding='utf8')
print('packed', d, title)
