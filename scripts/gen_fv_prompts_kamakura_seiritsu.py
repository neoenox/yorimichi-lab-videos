"""kamakura_seiritsu の背景クリップ(FreeVideo)の指示文を assets/kamakura_seiritsu/fv/prompts.json に書く。
人物・文字・建物・現代物は入れない(fv_prompts が末尾に no people, no text... を足す)。歴史上の場面の再現ではなく、話題を連想させる雰囲気映像(イメージ)。
  python scripts/gen_fv_prompts_kamakura_seiritsu.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from solo_spec import fv_prompts

fv_prompts('kamakura_seiritsu', [
    # 1 疑問(成立は1192年?)：霧の中の古い街道。問いかける雰囲気
    'A quiet stone path winding through thick morning mist toward a distant dark mountain ridge, pale light breaking through the fog, the camera slowly pushing forward.',
    # 2 年は一つに決まらない：複数の道・流れが分かれる
    'A mountain stream splitting into several thin channels over dark mossy rocks, clear water flowing in different directions, soft cold light, the camera slowly gliding along the water.',
    # 3 1185 守護・地頭(土地を治める):稲穂の広がる田
    'A wide field of golden rice stalks swaying in a gentle wind at dusk, distant low hills, warm low light, the camera slowly gliding sideways.',
    # 4 1192 征夷大将軍(任命・権威):古い巻物と筆(無地)
    'Close-up of an empty plain blank aged washi paper scroll slowly unrolling on a dark wooden desk, soft warm candlelight flickering, the camera slowly pushing in. No pens, no books, no objects on the desk.',
    # 5 教科書の年表(1192→1185):和紙の上に墨が一筋のびる(文字にならない線)
    'A single thick line of black ink slowly spreading across a blank sheet of washi paper, soft lamplight, the camera slowly pushing in. No brush, no hands, no characters.',
    # 6 欄外の諸説:薄れる灯り・複数の光
    'Several small paper lanterns without any markings glowing softly in the dark and drifting slowly on a calm river at night, gentle reflections, the camera slowly gliding forward.',
    # 7 段階を踏んで整う:夜明け、石段をのぼる光
    'Warm sunrise light slowly spreading over a calm sea of clouds and distant mountains, the sky changing from deep blue to gold, the camera slowly gliding upward.',
])
print('ok')