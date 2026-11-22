"""ffmpeg-skill の check.py を、このリポジトリの成果物に合わせて呼ぶ薄いラッパー。

動画を編集・再生成はしない。既存ファイルを読み取って検査し、結果を要約するだけなので、
元成果物は上書きしない（動画制作前確認の「元成果物を守り、版を分ける」に従う）。

使い方:
    python scripts/ffmpeg_skill_check.py out/90_foo_video.mp4 --platform youtube
    python scripts/ffmpeg_skill_check.py upload/short_foo/video.mp4 --platform shorts --write
    python scripts/ffmpeg_skill_check.py clip.mp4 --platform youtube --levels

スキルの場所:
    既定は ~/.agents/skills/ffmpeg-skill/scripts/check.py
    環境変数 FFMPEG_SKILL_DIR でスキルのルートを差し替えられる。

終了コード:
    0 ... FAIL なし（WARN は許容）
    1 ... 1件以上の FAIL
    2 ... スキル未導入、入力不存在、出力の解釈失敗などの実行エラー

注意:
    技術検査（尺・codec・音量・黒/フリーズ/ドロップアウト）の合格は、
    連続視聴・全編の実聴・字幕同期・史実確認の合格を意味しない。
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_SKILL_DIR = Path.home() / ".agents" / "skills" / "ffmpeg-skill"


def check_script():
    root = Path(os.environ.get("FFMPEG_SKILL_DIR") or DEFAULT_SKILL_DIR)
    p = root / "scripts" / "check.py"
    if not p.is_file():
        raise FileNotFoundError(
            f"ffmpeg-skill が見つかりません: {p}\n"
            "  npx -y ffmpeg-skill@4.1.2 --codex\n"
            "  または FFMPEG_SKILL_DIR にスキルのルートを指定してください"
        )
    return p


def main(argv=None):
    ap = argparse.ArgumentParser(description="ffmpeg-skill で成果物を検査する（編集はしない）")
    ap.add_argument("video", type=Path, help="検査する動画ファイル")
    ap.add_argument("--platform", default="youtube",
                    choices=("youtube", "shorts", "reels", "tiktok", "x", "broadcast", "podcast", "custom"))
    ap.add_argument("--no-content", action="store_true", help="黒/フリーズ/沈黙などの内容検査を省略する")
    ap.add_argument("--levels", action="store_true", help="法的な輝度/色差レベルも検査する（追加デコードあり）")
    ap.add_argument("--write", action="store_true",
                    help="out/<stem>_ffmpeg_skill_check.json に生の JSON を保存する")
    ap.add_argument("--python", default=sys.executable, help="check.py を実行する Python")
    a = ap.parse_args(argv)

    if not a.video.is_file():
        print(f"動画がありません: {a.video}", file=sys.stderr)
        return 2
    try:
        script = check_script()
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 2

    cmd = [a.python, str(script), str(a.video), "--platform", a.platform, "--json"]
    if not a.no_content:
        cmd.append("--content")
    if a.levels:
        cmd.append("--levels")
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if p.returncode not in (0, 1):
        sys.stderr.write(p.stderr or "")
        print(f"check.py が失敗しました（exit {p.returncode}）", file=sys.stderr)
        return 2
    try:
        data = json.loads(p.stdout)
    except (ValueError, TypeError) as e:
        print(f"check.py の出力を解釈できません: {e}", file=sys.stderr)
        sys.stderr.write(p.stdout[:2000])
        return 2

    rows = data.get("checks") or []
    for r in rows:
        status = r.get("status")
        if status in ("WARN", "FAIL"):
            print(f"{status:4s} {r.get('check')}: {r.get('value')}")
            if r.get("fix"):
                print(f"      fix: {r['fix']}")
    failed = data.get("failed")
    warnings = data.get("warnings")
    print(f"\n{a.video}: platform={data.get('platform')} "
          f"FAIL={failed} WARN={warnings} ({len(rows)} checks)")

    if a.write:
        out = Path("out") / f"{a.video.stem}_ffmpeg_skill_check.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf8")
        print(f"JSON: {out}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
