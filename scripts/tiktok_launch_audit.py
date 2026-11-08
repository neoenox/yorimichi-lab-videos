"""TikTok 初回投稿（Phase 1）の直前監査。動画・キャプション・固定コメント・日付の整合を1枚にまとめる。

見るもの:
  - mp4: 1080x1920 / 20〜45秒 / 音声あり / 尺
  - キャプション: 禁止語（チャンネル登録・概要欄・youtu.be・高評価・拡散希望・http）、ハッシュタグ3〜5、
    VOICEVOX と 参考（出典）が入っているか、1行目（検索語になる題）
  - 固定コメント: 出典とクレジット（VOICEVOX）が入っているか
  - 予定日: docs/TIKTOK_POSTING_PACK.md のカレンダーと slug が一致するか
usage: python scripts/tiktok_launch_audit.py
出力: out/TIKTOK_LAUNCH_SHEET.md（人はこれを見て投稿する）
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
_BIN = R / 'tools' / 'ffmpeg' / 'bin'
if not shutil.which('ffprobe') and _BIN.exists():
    os.environ['PATH'] = str(_BIN) + os.pathsep + os.environ.get('PATH', '')
BAD = ['チャンネル登録', '概要欄', 'youtu.be', '高評価', '拡散希望', 'http://', 'https://', '登録はこちら']
PACK = R / 'docs' / 'TIKTOK_POSTING_PACK.md'
CAL_RE = re.compile(r'^\|\s*(\d+)\s*\|\s*(\d+)/(\d+)\s*\|\s*(.)\s*\|\s*([\d:]+)\s*\|\s*`(\w+)`\s*\|\s*([^|]+)\|\s*([\d.]+)s\s*\|')


def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height', '-of', 'json', str(p)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    j = json.loads(r.stdout or '{}')
    v = next((s for s in j.get('streams', []) if s.get('codec_type') == 'video'), {})
    a = next((s for s in j.get('streams', []) if s.get('codec_type') == 'audio'), None)
    return float(j.get('format', {}).get('duration') or 0), v.get('width'), v.get('height'), a is not None


def main():
    cal = []
    for line in PACK.read_text(encoding='utf8').splitlines():
        m = CAL_RE.match(line.strip())
        if m:
            cal.append({'n': int(m.group(1)), 'date': f'{m.group(2)}/{m.group(3)}', 'wd': m.group(4), 'time': m.group(5),
                        'slug': m.group(6), 'title': m.group(7).strip(), 'dur': float(m.group(8))})
    pinned = (R / 'out' / 'tiktok_pinned_comments.md').read_text(encoding='utf8')
    blocks = {}
    for sec in re.split(r'^## ', pinned, flags=re.M)[1:]:
        head, _, body = sec.partition('\n')
        parts = re.split(r'[　\s]+', head.strip())
        # "1. 11/04 水　shibuya　渋谷の谷に…" -> 3番目が slug
        slug = parts[3] if len(parts) > 3 else None
        if slug:
            blocks[slug] = body
    rows, issues = [], []
    for c in cal:
        s = c['slug']
        mp4 = R / 'out' / f'short_tiktok_{s}.mp4'
        cap = R / 'out' / f'short_tiktok_{s}_description.md'
        if not mp4.exists():
            issues.append(f'{s}: mp4 が無い'); continue
        dur, w, h, has_audio = probe(mp4)
        text = cap.read_text(encoding='utf8') if cap.exists() else ''
        first = text.splitlines()[0].strip() if text else ''
        tags = len(re.findall(r'#[^\s#]+', text))
        bad = [b for b in BAD if b in text]
        pin = blocks.get(s, '')
        pin_ok = ('VOICEVOX' in pin) and ('出典' in pin or '参考' in pin)
        row_issues = []
        if (w, h) != (1080, 1920): row_issues.append(f'解像度 {w}x{h}')
        if not 20 <= dur <= 45: row_issues.append(f'尺 {dur:.1f}s')
        if not has_audio: row_issues.append('音声なし')
        if abs(dur - c['dur']) > 0.5: row_issues.append(f'カレンダーの尺と違う（{c["dur"]}s）')
        if bad: row_issues.append('禁止語: ' + ', '.join(bad))
        if not 3 <= tags <= 5: row_issues.append(f'ハッシュタグ {tags}個')
        if 'VOICEVOX' not in text: row_issues.append('キャプションにVOICEVOXが無い')
        if '参考' not in text and '出典' not in text: row_issues.append('キャプションに出典が無い')
        if not pin: row_issues.append('固定コメントが無い')
        elif not pin_ok: row_issues.append('固定コメントに出典/クレジットが無い')
        rows.append({**c, 'dur_real': dur, 'first': first, 'tags': tags, 'pin': bool(pin), 'issues': row_issues})
        if row_issues:
            issues.append(f'{s}: ' + ' / '.join(row_issues))
    L = ['# TikTok 投稿シート（Phase 1・直前監査）', '',
         f'- 対象: {len(rows)}本 / 指摘: {len(issues)}件',
         '- 検査: `python scripts/tiktok_launch_audit.py`（動画・キャプション・固定コメント・日付の整合）', '']
    if issues:
        L += ['## 要確認', ''] + [f'- {i}' for i in issues] + ['']
    L += ['## 投稿カレンダー（月水金 19:30）', '',
          '| # | 日付 | 曜 | slug | 尺 | フック（1行目） | タグ | 固定コメント |', '|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append(f'| {r["n"]} | {r["date"]} | {r["wd"]} | `{r["slug"]}` | {r["dur_real"]:.1f}s | {r["first"]} | {r["tags"]} | {"あり" if r["pin"] else "無し"} |')
    L += ['', '## 投稿の手順（1本あたり・初回3本は特に）', '',
          '1. `out/short_tiktok_<slug>.mp4` をアプリで選ぶ（Webは表示が変わりやすい）',
          '2. 「次へ」→「その他のオプション」→「AI生成コンテンツ」を **ON**',
          '3. キャプションを `out/short_tiktok_<slug>_description.md` から全文貼る（リンクは貼らない）',
          '4. 19:30 に公開（Webの予約投稿でもよい。上限は実機で確認）',
          '5. `out/tiktok_pinned_comments.md` の該当節を**固定コメント**にしてピン留め',
          '6. 投稿URLと時刻を記録。48時間後に3秒維持・完走率・共有・保存・フォローを `TIKTOK_POSTING_PACK.md` の計測表へ', '',
          '## 実機で見る5点（人の作業）', '',
          '- [ ] 音が聞こえる（イヤホンで一度）',
          '- [ ] 字幕が下のUIに隠れていない',
          '- [ ] 出典（上部の小さい行）が読める',
          '- [ ] 最初の1秒で内容が分かる',
          '- [ ] AIラベルがONになっている', '',
          '## 尺の扱い（方針）', '',
          '- 目標は21〜34秒。**34秒を超えるのは銀座（35.9）・深川（35.5）・関ヶ原（38.5）の3本**。',
          '- TikTokの上限（60分）には遠く、検査も20〜45秒で通しているため、**切らずに出す**。切る場合は台本の1場面を削って作り直す（音声速度は上げない）。', '']
    (R / 'out' / 'TIKTOK_LAUNCH_SHEET.md').write_text('\n'.join(L) + '\n', encoding='utf8')
    print(f'{len(rows)}本 / 指摘 {len(issues)}件')
    for i in issues:
        print(' -', i)
    return 0


if __name__ == '__main__':
    sys.exit(main())
