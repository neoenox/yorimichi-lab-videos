"""単独Short: 1円玉は、作るのに1円以上かかる？(solo_1yen_fv、FreeVideo背景版)。
根拠は造幣局「貨幣Q&A」(https://www.mint.go.jp/faq-list/faq_coin) と
「現在製造している貨幣」(https://www.mint.go.jp/operations/production/operations_coin_presently-minted.html)。
2026-11-19に本文確認。nolong, nolink。背景はFreeVideo(MiniMax H3)、図は自作。"""
import sys, os, json
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solo_spec import build, T, fv_prompts

Q = '造幣局「貨幣Q&A」'
M = '造幣局「現在製造している貨幣」'
pron = {
    '1円玉': 'イチエンダマ', '造幣局': 'ゾーヘイキョク', '製造原価': 'セイゾウゲンカ',
    '原価': 'ゲンカ', '勘案': 'カンアン', '偽造': 'ギゾウ', '助長': 'ジョチョウ',
    'アルミニウム': 'アルミニウム', '第4条': 'ダイヨンジョウ', '信用': 'シンヨウ',
    '信任': 'シンニン', '貨種': 'カシュ',
}
scenes = [
    dict(text='1円玉は、作るのに1円以上かかる？ 造幣局は、貨幣の製造原価を公表していません。',
         big='原価は公表されていない', sub='造幣局の公式Q&A', src=Q,
         viz=T(2.8, [('噂', '3円は未確認'), ('公式', '原価は非公表'), ('時点', '2026年11月19日')])),
    dict(text='理由は、国民の貨幣に対する信任を維持するためと、偽造を助長するおそれがあるためです。',
         big='公表しない理由', sub='信任維持と偽造防止', src=Q,
         viz=T(2.8, [('理由1', '信任の維持'), ('理由2', '偽造の助長防止'), ('出典', '造幣局Q&A')])),
    dict(text='財務省が造幣局に払う製造代金の算定には、原価などが勘案されると、法律に書かれています。',
         big='算定に原価を勘案', sub='通貨法第4条', src=Q,
         viz=T(2.8, [('製造', '造幣局'), ('発行', '政府'), ('算定', '原価を勘案')])),
    dict(text='1円玉はアルミニウム製で、重さは1グラム。3円かかるという話は、公式には確認できません。',
         big='重さ1グラム', sub='アルミニウム製・「3円」は公式未確認', src=M,
         viz=T(2.8, [('材質', 'アルミニウム'), ('量目', '1g'), ('原価', '非公表')])),
]

notes = (
    '■ 2026年11月19日に、造幣局「貨幣Q&A」(https://www.mint.go.jp/faq-list/faq_coin) と'
    '「現在製造している貨幣」(https://www.mint.go.jp/operations/production/operations_coin_presently-minted.html) '
    'の本文を読んで作った整理です。2026年11月19日時点の情報です。\n'
    '・使った事実(同)：造幣局は、貨幣の製造原価について「国民の貨幣に対する信任を維持するためや、'
    '貨幣の偽造を助長するおそれがあると考えられることから、公表していません」と明記。'
    '「現在製造している貨幣」の表では、1円貨はアルミニウム製・重さ1g・直径20mm。'
    '通貨の単位及び貨幣の発行等に関する法律第4条4項では、財務大臣が造幣局に支払う製造代金は'
    '貨幣の製造原価等を勘案して算定すると規定されている。\n'
    '・言い過ぎを避けた点：「1円玉は3円で作れる」という話は造幣局が原価を公表していないため公式には確認できず、'
    '断定しない。材料の重さだけから原価を求めることもしない。\n'
    '・使っていないこと：原価の推計を載せた報道・雑学記事（一次資料ではない）、'
    '流通枚数や2026年の増産に関する話題。\n'
    '・未確認：造幣局の方針が変わった後の情報（動画は2026年11月19日時点）。\n'
)
def make_bg():
    """自作の硬貨イラスト背景。assets/ はgit管理外なので、毎回ここで作る。"""
    from PIL import Image, ImageDraw, ImageFont
    import math
    p = Path(__file__).resolve().parents[1] / 'assets/1yen'
    p.mkdir(parents=True, exist_ok=True)
    W, H = 1080, 1920
    im = Image.new('RGB', (W, H), (9, 20, 34)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(9 + 22 * t), int(20 + 30 * t), int(34 + 35 * t)))
    cx, cy, r = 540, 760, 360
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(205, 168, 72), outline=(255, 225, 140), width=14)
    d.ellipse((cx - r + 34, cy - r + 34, cx + r - 34, cy + r - 34), outline=(150, 116, 40), width=8)
    f = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 260)
    d.text((cx, cy - 40), '1', font=f, fill=(88, 64, 20), anchor='mm')
    d.text((cx, cy + 120), 'YEN', font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 90),
           fill=(88, 64, 20), anchor='mm')
    for i in range(24):
        a = i * math.pi / 12
        d.line((cx + int(math.cos(a) * (r + 30)), cy + int(math.sin(a) * (r + 30)),
                cx + int(math.cos(a) * (r + 80)), cy + int(math.sin(a) * (r + 80))),
               fill=(90, 72, 40), width=3)
    im.save(p / 'bg.png')


if __name__ == '__main__':
    build('1yen_fv', '1円玉は、作るのに1円以上かかる？ 原価は公表されていない',
          '1円玉の製造原価', '公式な原価は、公表されていない', pron, scenes,
          ['硬貨の接写', '静かな事務机と白いカード', '帳面と小さな秤', '硬貨の縁の接写'], notes,
          bg_note='・動画内の図は自作です。背景映像はFreeVideo(MiniMax H3)によるAI生成で、イメージです。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです\n・図・表：自作',
          end_q='1円玉、まだ財布に入っていますか？',
          tags=['1円玉', '造幣局', '貨幣', 'お金', '雑学', 'Shorts'])
    fv_prompts('1yen_fv', [
        'A close-up of a plain silver Japanese aluminium one-yen coin with a simple young tree sapling emblem, no human portrait, resting on a dark wooden table, soft warm window light, slow camera glide, cinematic realistic look, no people, no hands, no text, no letters, no numbers, no writing, no labels, no logos',
        'A quiet dark wooden counter with a few blank white information cards and an empty brass tray, soft light, slow camera push in, cinematic realistic look, no people, no hands, no text, no letters, no writing, no labels',
        'A stack of plain blank notebooks and a small old weighing scale on a dark shelf, soft light, slow camera glide, cinematic realistic look, no people, no hands, no text, no letters, no writing, no labels',
        'The edge of a plain silver Japanese aluminium one-yen coin on a dark matte surface, simple tree sapling motif barely visible, no human portrait, soft spotlight, the camera slowly gliding around the rim, shallow depth of field, cinematic realistic look, no people, no hands, no text, no letters, no numbers, no writing',
    ], allow_modern=True)
