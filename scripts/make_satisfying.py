"""「気持ちいい系」Short(ナレーションなし)を組み立てる。assets/<slug>/fv/clip1..N.mp4(AI生成・7秒) を、クロスフェードでつなぎ、BGMを載せ、題名と注記を重ねる。
  python scripts/make_satisfying.py <slug> "<題名>" [BGM mp3のパス]
出力: out/short_<slug>.mp4 (1080x1920, 30fps) / upload/short_<slug>/ (video.mp4, title.txt, description.txt, tags.txt)
注意: BGMは assets/bgm_maou/ (魔王魂。概要欄に「音楽：魔王魂」と表記)。私は音を聴けないので、曲の相性は人が判断する。AI生成の映像は「イメージです」と明記。"""
import json, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
slug, title = sys.argv[1], sys.argv[2]
bgm = sys.argv[3] if len(sys.argv) > 3 else str(R / 'assets' / 'bgm_maou' / 'maou_bgm_acoustic45.mp3')
clips = sorted((R / 'assets' / slug / 'fv').glob('clip*.mp4'))
assert clips, 'クリップがありません'
XF, CLIP = 0.8, 7.0
n = len(clips)
total = CLIP * n - XF * (n - 1)
inp, filt = [], []
for i, c in enumerate(clips):
    inp += ['-i', str(c)]
    filt.append(f'[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p,trim=duration={CLIP},setpts=PTS-STARTPTS[v{i}]')
cur = 'v0'
for i in range(1, n):
    off = CLIP * i - XF * i
    filt.append(f'[{cur}][v{i}]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}]'); cur = f'x{i}'
font = 'C\\:/Windows/Fonts/meiryob.ttc'
txt = title.replace(':', '\\:').replace("'", '')
filt.append(f"[{cur}]drawtext=fontfile='{font}':text='{txt}':fontsize=58:fontcolor=white:borderw=3:bordercolor=black@0.55:x=(w-text_w)/2:y=h*0.10:enable='lt(t,4)':alpha='if(lt(t,0.6),t/0.6,if(gt(t,3.4),(4-t)/0.6,1))'[vt]")
filt.append(f"[vt]drawtext=fontfile='{font}':text='AI生成の映像（イメージ）':fontsize=30:fontcolor=white@0.8:borderw=2:bordercolor=black@0.5:x=(w-text_w)/2:y=h*0.93[vout]")
out = R / 'out' / f'short_{slug}.mp4'
cmd = ['ffmpeg', '-y', '-loglevel', 'error', *inp, '-stream_loop', '-1', '-i', bgm,
       '-filter_complex', ';'.join(filt) + f';[{n}:a]atrim=duration={total:.2f},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-1.5:LRA=7,afade=t=in:d=1,afade=t=out:st={total - 1.5:.2f}:d=1.5[aout]',
       '-map', '[vout]', '-map', '[aout]', '-t', f'{total:.2f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', str(out)]
subprocess.run(cmd, check=True)
pk = R / 'upload' / f'short_{slug}'; pk.mkdir(parents=True, exist_ok=True)
(pk / 'video.mp4').write_bytes(out.read_bytes())
(pk / 'title.txt').write_text(f'{title} #Shorts', encoding='utf8')
(pk / 'description.txt').write_text(f'{title}\n\n映像はFreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の映像ではありません。\n音楽：魔王魂(https://maou.audio/)\n\n#Shorts #ASMR #癒し #気持ちいい', encoding='utf8')
(pk / 'tags.txt').write_text('Shorts,気持ちいい,癒し,ASMR,AI生成,砂,蜂蜜,氷,墨', encoding='utf8')
print('作成:', out, f'{total:.1f}秒')
