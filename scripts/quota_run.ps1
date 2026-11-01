# YouTube API クォータ回復後（毎日 16:05 JST 以降）に、溜まっている作業を1日分だけ実行する。
# 登録: schtasks /create /tn "rekishi-quota-run" /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File E:\rekishikaisetu-honnoji\scripts\quota_run.ps1" /sc daily /st 16:05 /f
# 解除: schtasks /delete /tn "rekishi-quota-run" /f
# ログ: out\codex\quota_run.log
# 何度実行しても安全（data/quota_run_state.json で済んだ作業を覚えている）。

$ErrorActionPreference = 'Continue'
$env:PATH = 'E:\rekishikaisetu-honnoji\tools\ffmpeg\bin;' + $env:PATH
$env:PYTHONIOENCODING = 'utf8'
Set-Location 'E:\rekishikaisetu-honnoji'

# 16:00ちょうどにクォータが戻らないことがあるので、最大3時間は待つ
$py = 'C:\Users\neoen\AppData\Local\Programs\Python\Python311\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }
& $py -X utf8 scripts/daily_quota_run.py --budget 9400 --wait 180
$code = $LASTEXITCODE

# 実行後の突き合わせ（予約・ID・Shortのリンク・二重公開）。NG があればログに残す
& $py -X utf8 scripts/check_publish.py --check *>&1 | Tee-Object -Append -FilePath out\codex\quota_check.log

# F2: 前日までに公開された Short に、対応する長尺への案内コメントを入れる（未投稿の分だけ。固定はStudioで手作業）
& $py -X utf8 scripts/short_comment.py *>&1 | Tee-Object -Append -FilePath out\codex\quota_comment.log
exit $code
