#!/bin/bash
# 背景(FreeVideo)のクリップを生成する。使い方: bash scripts/fv_clips.sh <slug> [clipN ...]
#   slug だけ → assets/<slug>/fv/prompts.json の全クリップ(solo_ship.py clips)。
#   clipN も指定 → その番号だけ作り直す(freevideo_batch.py)。1本あたり約9分。
# ComfyUI(127.0.0.1:8188)を起動 → 待つ → 生成 → 止める。VOICEVOXやChromeを重く動かさない(メモリ不足で失敗する)。
SLUG="$1"; shift
cd /e/FreeVideo/runtime/ComfyUI
( "E:/FreeVideo/runtime/FreeVideo-engine/envs/comfyui-e0766581f8a2729a/Scripts/python.exe" -u -B main.py --listen 127.0.0.1 --port 8188 --disable-auto-launch --disable-all-custom-nodes --whitelist-custom-nodes FreeVideo > "${TEMP:-/tmp}/comfy_${SLUG}.log" 2>&1 & SRV=$!
for i in $(seq 1 120); do curl -s http://127.0.0.1:8188/ >/dev/null && break; sleep 3; done
cd /e/rekishikaisetu-honnoji
if [ $# -eq 0 ]; then python scripts/solo_ship.py clips "$SLUG"; else python scripts/freevideo_batch.py "assets/$SLUG/fv/prompts.json" "assets/$SLUG/fv" "$@"; fi
echo DONE
kill $SRV; wait )
