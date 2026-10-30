"""Short の投稿パックを upload/short_<slug>/ に作る（動画・字幕・概要欄・タイトル・タグ）。
usage: python scripts/pack_short.py <slug> <long_pack>    例: pack_short.py sunrise 20_sunrise_solstice
タイトルは「<title> 約N秒で確かめる #Shorts」。タグは長尺のタグに Shorts を足す。"""
import json, re, shutil, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
slug, long_pack = sys.argv[1], sys.argv[2]
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
tags = (R / 'upload' / long_pack / 'tags.txt').read_text(encoding='utf8').strip()
(d / 'tags.txt').write_text((tags + ', Shorts') if 'Shorts' not in tags else tags, encoding='utf8')
print('packed', d, title)
