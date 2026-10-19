<#
画像生成を、ブラウザ（ChatGPT web UI）で回す。scripts/codex_art.py の代替で、
`codex` CLI が使えない環境のためのもの。生成物は assets/<dir>/art_<name>.png。

usage:
  pwsh scripts/art_chatgpt.ps1 -Dir okehazama -Session <bskのセッションID> -Scenes scenes.json
  pwsh scripts/art_chatgpt.ps1 -Dir okehazama -Session <ID> -Scenes scenes.json -Only downpour -Force

scenes json: [{"name":"downpour","scene":"..."}, ...]
すでに assets/<dir>/art_<name>.png がある場合は飛ばす（-Force で上書き）。
セッションは `bsk session start --json` で作り、`bsk navigate <会話URL>` で対象の
会話を開いておく。

注意: ChatGPT は長い会話の古い画像を DOM から外す（間引く）ため、「画像の枚数が
増えたか」では生成完了を判定できない。そこで「直前まで無かった src の画像が
あらわれたか」で見る。また bsk のセッションは途中で切れることがあるので、
その場合はセッションを作り直して会話URLを開き直す。
#>
param(
  [Parameter(Mandatory=$true)][string]$Dir,
  [Parameter(Mandatory=$true)][string]$Session,
  [Parameter(Mandatory=$true)][string]$Scenes,
  [string]$Only,
  [switch]$Force,
  [int]$TimeoutSec = 300
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$root    = Split-Path -Parent $PSScriptRoot
$outDir  = Join-Path $root "assets/$Dir"
$downloads = Join-Path $env:USERPROFILE 'Downloads'

# 画風は codex_art.py の STYLE と同じ。1本の動画の中でそろえる。
$STYLE = '落ち着いた紺・金・生成り色を基調にした、やや様式化したデジタルイラスト（絵本や図鑑の挿絵のような柔らかい質感）。写真のようにリアルにはしない。'

function MakePrompt([string]$scene) {
  '横長16:9の背景イラストを1枚生成してください。' +
  '条件：画像の中に、文字・数字・ロゴ・透かし・看板の文字を一切入れない（本や巻物の文字は、読めない模様にする）。' +
  '実在の人物の顔や、実在の作品・商標に似せない。人物を描く場合は、必ず遠景の小さな後ろ姿かシルエットにし、顔を描かない。' +
  '旗・幕・武具に、家紋や紋章を描かない（無地にする）。' +
  "画風：$STYLE" +
  '構図：画面の中央から右に主題を大きく置き、左上は、文字を重ねられるよう、比較的すっきりと暗めにする（細かい模様を避ける）。' +
  "場面：$scene"
}

function RunBsk([string[]]$cmdArgs) {
  $r = & bsk @cmdArgs --session $Session 2>&1
  if ($LASTEXITCODE -ne 0) { throw ("bsk " + ($cmdArgs -join ' ') + " failed: " + ($r -join ' ')) }
  return ($r -join "`n")
}

function ComposerRef {
  $snap = RunBsk @('snapshot')
  $m = [regex]::Matches($snap, '@e(\d+)\s+textbox')
  if ($m.Count -eq 0) { throw 'composer textbox not found' }
  return '@e' + $m[$m.Count-1].Groups[1].Value
}

function ArtSrcs {
  # ChatGPT は長い会話の古い画像を DOM から外すので、「枚数」ではなく「src の顔ぶれ」で進捗を見る
  $js = '(()=>{const a=[...document.querySelectorAll("img")].filter(i=>i.naturalWidth>1500).map(i=>i.src);return JSON.stringify(a)})()'
  return (RunBsk @('evaluate', $js)).Trim() | ConvertFrom-Json
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$list = [IO.File]::ReadAllText((Join-Path $root $Scenes), [Text.Encoding]::UTF8) | ConvertFrom-Json
# -File で起動すると配列パラメータが分割されないので、カンマ区切りの文字列で受ける
$onlyList = if ($Only) { $Only -split ',' | ForEach-Object { $_.Trim() } } else { $null }

foreach ($item in $list) {
  $name  = $item.name
  if ($onlyList -and ($name -notin $onlyList)) { continue }
  $target = Join-Path $outDir ("art_$name.png")
  if ((Test-Path $target) -and -not $Force) { Write-Host "[skip] $name"; continue }

  Write-Host "[gen ] $name"
  $ref = ComposerRef
  Set-Clipboard -Value (MakePrompt $item.scene)
  RunBsk @('press', 'Escape') | Out-Null          # 何かのダイアログ/プレビューを閉じる
  RunBsk @('press', 'Ctrl+V', '--ref', $ref) | Out-Null
  Start-Sleep -Milliseconds 400
  $before = ArtSrcs
  RunBsk @('press', 'Enter', '--ref', $ref) | Out-Null

  # 生成完了 = 直前まで無かった src の画像があらわれる
  $deadline = (Get-Date).AddSeconds($TimeoutSec)
  $new = @()
  do {
    Start-Sleep -Seconds 4
    $new = @(ArtSrcs | Where-Object { $_ -notin $before })
  } while ($new.Count -eq 0 -and (Get-Date) -lt $deadline)
  if ($new.Count -eq 0) { throw "[fail] $name : no new image after ${TimeoutSec}s" }
  $src = $new[$new.Count-1]
  Start-Sleep -Seconds 4                        # ぼかしプレビューが本番画像に変わるのを待つ

  # いちばん新しい画像を、そのままダウンロード（フル解像度）
  $dl = Join-Path $downloads ("art_$name.png")
  if (Test-Path $dl) { Remove-Item $dl -Force }
  $js = @"
(()=>{document.getElementById('bsk-dl')?.remove();
const a=document.createElement('a');a.href='$src';a.download='art_$name.png';a.id='bsk-dl';a.textContent='DL';
a.setAttribute('style','position:fixed !important;left:10px !important;top:10px !important;width:120px !important;height:40px !important;z-index:2147483647 !important;background:#c00 !important;color:#fff !important;display:block !important');
document.body.appendChild(a);a.click();return 'clicked'})()
"@
  RunBsk @('evaluate', $js) | Out-Null

  $dlDeadline = (Get-Date).AddSeconds(90)
  while (-not (Test-Path $dl) -and (Get-Date) -lt $dlDeadline) { Start-Sleep -Milliseconds 700 }
  if (-not (Test-Path $dl)) { throw "[fail] $name : download did not arrive" }
  Start-Sleep -Milliseconds 500                  # 書き込み完了待ち
  Move-Item $dl $target -Force
  $sz = (Get-Item $target).Length
  Write-Host ("[done] {0} {1:N0} bytes" -f $name, $sz)
  if ($sz -lt 200000) { throw "[fail] $name : file too small, probably not an image" }
}

Write-Host 'all done'
