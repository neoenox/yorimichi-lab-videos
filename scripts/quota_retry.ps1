# Wait for network recovery, then run the quota batch once (with a lock file).
# usage: powershell -NoProfile -File scripts\quota_retry.ps1
# log: out\codex\quota_retry.log
$ErrorActionPreference = 'Continue'
Set-Location 'E:\rekishikaisetu-honnoji'
$log = 'E:\rekishikaisetu-honnoji\out\codex\quota_retry.log'
$lock = 'E:\rekishikaisetu-honnoji\out\codex\quota_retry.lock'
$deadline = (Get-Date).Date.AddHours(23)

function Log($m) { "[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $m | Out-File -Append -Encoding utf8 $log }

if (Test-Path $lock) {
    $other = Get-Content $lock -ErrorAction SilentlyContinue
    if ($other -and (Get-Process -Id $other -ErrorAction SilentlyContinue)) { Log "already running (pid $other). exit"; exit 0 }
}
Set-Content -Path $lock -Value $PID -Encoding ascii

function Net-OK {
    $c = New-Object System.Net.Sockets.TcpClient
    try { return $c.ConnectAsync('www.googleapis.com', 443).Wait(6000) } catch { return $false } finally { $c.Close() }
}

Log "waiting start (pid $PID)"
while ((Get-Date) -lt $deadline) {
    if (-not (Net-OK)) { Log 'network down. retry in 120s'; Start-Sleep -Seconds 120; continue }
    Log 'network up. start quota batch'
    $py = 'C:\Users\neoen\AppData\Local\Programs\Python\Python311\python.exe'
    & $py -X utf8 scripts/daily_quota_run.py --budget 9400 --wait 30 *>> $log
    $code = $LASTEXITCODE
    Log "quota batch finished code=$code"
    & $py -X utf8 scripts/check_publish.py --check *>> $log
    break
}
Remove-Item $lock -ErrorAction SilentlyContinue
Log 'exit'
