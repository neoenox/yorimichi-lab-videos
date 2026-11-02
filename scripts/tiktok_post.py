"""TikTokの投稿1本分を、貼るだけの形で出す。

usage:
    python scripts/tiktok_post.py shibuya      # 動画・キャプション・固定コメントを表示
    python scripts/tiktok_post.py --list       # 15本の順番と日付
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ORDER = [
    ('shibuya', '11/04 水 19:30'), ('hibiya', '11/06 金 19:30'), ('ginza', '11/09 月 19:30'),
    ('fukagawa', '11/11 水 19:30'), ('sekigahara', '11/13 金 19:30'), ('koku', '11/16 月 19:30'),
    ('islands', '11/18 水 19:30'), ('oke', '11/20 金 19:30'), ('mikatagahara', '11/23 月 19:30'),
    ('tottori', '11/25 水 19:30'), ('shizugatake', '11/27 金 19:30'), ('yachin', '11/30 月 19:30'),
    ('sushi', '12/02 水 19:30'), ('hikeshi', '12/04 金 19:30'), ('hikyaku', '12/07 月 19:30'),
]


def ffprobe_bin():
    p = shutil.which('ffprobe')
    if p:
        return p
    local = ROOT / 'tools' / 'ffmpeg' / 'bin' / 'ffprobe.exe'
    return str(local) if local.exists() else None


def duration(mp4):
    exe = ffprobe_bin()
    if not exe:
        return None
    out = subprocess.run([exe, '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', str(mp4)], capture_output=True, text=True).stdout.strip()
    return float(out) if out else None


def pinned(spec):
    lines = ['■ 出典']
    lines += [f'・{r}' for r in spec.get('refs', [])]
    lines += ['■ クレジット', '・音声：VOICEVOX:四国めたん']
    credit = spec.get('credit') or '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです）'
    lines += [ln.rstrip() for ln in credit.split('\n') if ln.strip()]
    return '\n'.join(lines)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    if args[0] == '--list':
        for i, (slug, when) in enumerate(ORDER, 1):
            spec = json.loads((ROOT / 'data' / f'short_tiktok_{slug}.json').read_text(encoding='utf8'))
            print(f'{i:2}. {when}  {slug:14} {spec["title"]}')
        return 0

    slug = args[0]
    spec_path = ROOT / 'data' / f'short_tiktok_{slug}.json'
    mp4 = ROOT / 'out' / f'short_tiktok_{slug}.mp4'
    cap_path = ROOT / 'out' / f'short_tiktok_{slug}_description.md'
    if not spec_path.exists() or not mp4.exists() or not cap_path.exists():
        print(f'ない: {spec_path} / {mp4} / {cap_path}')
        return 1

    spec = json.loads(spec_path.read_text(encoding='utf8'))
    when = dict(ORDER).get(slug, '(予定外)')
    dur = duration(mp4)
    print('=' * 60)
    print(f'{when}  {spec["title"]}')
    print('=' * 60)
    print(f'動画      : {mp4.relative_to(ROOT)}' + (f'  ({dur:.1f}s)' if dur else ''))
    print(f'キャプション: {cap_path.relative_to(ROOT)}')
    print()
    print('--- キャプション（コピペ） ---')
    print(cap_path.read_text(encoding='utf8').strip())
    print()
    print('--- 固定コメント（コピペ→ピン留め） ---')
    print(pinned(spec))
    print()
    print('--- 投稿前チェック ---')
    print('[ ] AIラベルON（その他のオプション → AI生成コンテンツ）')
    print('[ ] 音が聞こえる')
    print('[ ] 字幕が下のUIに隠れていない')
    print('[ ] 投稿後、固定コメントをピン留め')
    return 0


if __name__ == '__main__':
    sys.exit(main())
