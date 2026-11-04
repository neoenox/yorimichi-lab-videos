"""Build the pop-style Anegawa spec for the codex comparison slug."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG = "codex"
THEME = "20261104_anegawa3"
PACK = "cmp3_codex"
MAPBOX = [40, 150, 1260, 800]

BLUE = (67, 132, 245)
RED = (220, 78, 75)
GOLD = (235, 180, 65)
CYAN = (60, 190, 220)
GREEN = (52, 160, 100)
PURPLE = (130, 90, 205)

KEYS = [
    "kanegasaki", "june", "cast", "terrain", "dawn",
    "west", "east", "decide", "kubi", "after",
]

# Crops keep the river corridor large while retaining both banks.
CROPS = {
    "mid": [0.0, 0.08, 1.0, 0.92],
    "main": [0.0, 0.15, 1.0, 0.85],
    "core": [0.0, 0.08, 1.0, 0.92],
}


def point(name, x, y):
    crop = CROPS.get(name)
    if crop:
        x = (x - crop[0]) / (crop[2] - crop[0])
        y = (y - crop[1]) / (crop[3] - crop[1])
    return [round(x, 4), round(y, 4)]


def place(name, xy, label, kind="spot", at=0, side="r", col=GOLD, lsize=30):
    return dict(xy=point(name, *xy), label=label, kind=kind, at=at,
                side=side, col=col, lsize=lsize)


def line(name, coords, label, at=0, col=CYAN, lab=None, dash=False, lsize=32):
    entry = dict(pts=[point(name, *xy) for xy in coords], label=label,
                 at=at, col=col, dash=dash, lsize=lsize)
    if lab:
        entry["lab"] = point(name, *lab)
    return entry


def unit(name, label, coords, legs=None, at=0, sub=None, col=BLUE,
         portrait=None, head=30, lab_off=(38, -5), lsize=28, dashed=False):
    entry = dict(label=label, col=col, pts=[point(name, *xy) for xy in coords],
                 at=at, head=head, lab_off=list(lab_off), lsize=lsize,
                 dashed=dashed)
    if sub:
        entry["sub"] = sub
    if portrait:
        entry["portrait"] = portrait
    if legs:
        entry["legs"] = legs
    return entry


SOURCE_COLORS = {
    "N": "blue",
    "軍": "orange",
    "通説": "red",
    "説": "purple",
    "資": "green",
}

SOURCE_TAGS = {
    "kanegasaki": ["説"] * 7 + ["通説", "説"],
    "june": ["説", "説", "N", "N", "N", "N"],
    "cast": ["資", "N", "N", "N", "資", "資", "資", "N", "N"],
    "terrain": [None, None, None, None, None, None, "N", None],
    "dawn": ["N", "N", "N", "N", "N", "説", "N"],
    "west": ["N", "N", "N", "軍", "軍", "軍", "軍", "軍", "軍", "通説", "N"],
    "east": ["N", "N", "N", "N", "通説", "軍", "軍", "軍", "通説", "説", "N"],
    "decide": ["N"] * 8,
    "kubi": ["N"] * 7,
    "after": ["N", "N", "N", "説", "説", "説", "説", "説", "説"],
}

# Short phrases are copied from the fixed narration and keep each source's
# uncertainty wording visible. Detailed explanation remains in subtitles.
DISPLAY = {
    "kanegasaki": [
        "元亀元年・一五七〇年", "信長、越前の朝倉へ", "浅井長政、朝倉に味方",
        "前から朝倉／後ろから浅井", "挟み撃ちの危ない場面", "信長、急いで退く",
        "金ヶ崎の退き口", "殿は木下藤吉郎ら、と伝わる", "五月・千草越えで岐阜へ",
    ],
    "june": [
        "六月、再び近江へ", "六月十九日、岐阜を出たといわれる",
        "六月二十一日・虎御前山", "二十二日、いったん兵を引く",
        "竜ヶ鼻に陣取る（信長）", "家康も同じ竜ヶ鼻へ",
    ],
    "cast": [
        "朝倉景健の援軍", "朝倉八千／浅井五千", "合計・一万三千",
        "朝倉勢は大依山へ", "浅井方：長政・磯野・遠藤",
        "織田方：柴田・秀吉・稲葉ほか", "徳川方：酒井・榊原・本多ほか",
        "顔ぶれも兵数も、書物で異なる", "織田・徳川の数は公記に記載なし",
    ],
    "terrain": [
        "ここからは地図で", "近江北部・姉川周辺", "北：小谷城", "山上の城",
        "姉川は西へ、琵琶湖へ", "南：横山城", "竜ヶ鼻に織田・徳川",
        "北：野村・三田村",
    ],
    "dawn": [
        "六月二十七日・暁", "陣払いして帰ったと思われた", "二十八日未明・三十町ほど",
        "三十町＝三キロ余り", "野村・三田村へ、二手に備える",
        "奇襲だったと見る説", "公記は「奇襲」と書かない",
    ],
    "west": [
        "公記の布陣", "西は三田村口", "一番合戦に家康",
        "実紀は別の配陣を記す", "信長＝朝倉／家康＝浅井",
        "暁に陣を替えた、と記す", "家康が朝倉へ", "忠勝の突入話",
        "相手：実紀＝浅井／三代記＝朝倉", "榊原康政の側面攻撃説",
        "公記・実紀の姉川条に記載なし",
    ],
    "east": [
        "東は野村", "信長の馬廻が向かう", "さらに東に美濃三人衆",
        "稲葉・氏家・安藤", "相手は浅井の軍、と語られる",
        "磯野員昌が先陣を崩したと伝わる", "十一段崩し",
        "旗本も騒動と浅井三代記", "美濃三人衆の側面攻撃説",
        "後世の創作という見方", "公記には記載なし",
    ],
    "decide": [
        "元亀元年・六月二十八日", "ユリウス暦七月三十日",
        "卯の刻・午前六時ごろ", "公記の記述", "姉川で押し返す",
        "黒煙／しのぎを削る", "浅井・朝倉は退く",
        "公記の戦闘描写は数行",
    ],
    "kubi": [
        "首注文を載せる", "真柄十郎左衛門—青木所左衛門",
        "遠藤喜右衛門—竹中久作", "主だった者・千百余",
        "死者の総数ではない", "大谷まで五十町、追い討ち",
        "高山の大谷から横山へ戻る",
    ],
    "after": [
        "横山城、降参", "木下藤吉郎が定番に", "七月一日、佐和山城へ",
        "浅井・朝倉は、この戦いに敗れる", "けれども滅びてはいない",
        "秋・志賀の陣", "天正元年、浅井・朝倉が倒れる", "三年後",
        "姉川の勝ち、しかし決着ではない",
    ],
}


def background(img, alts):
    return dict(t="anim", name="pop_bgimg", img=img, alts=alts,
                seg=20, dim=0.44, blur=5, at=0)


def battle_map(img, *, places=None, lines=None, units=None, marks=None):
    return dict(t="anim", name="battle_map", img=img, box=MAPBOX, at=0,
                places=places or [], lines=lines or [], units=units or [],
                marks=marks or [])


def story_rows(key, scene_data, mapped=False):
    sentences = [x.strip() + "。" for x in scene_data["narration"].split("。") if x.strip()]
    tags = SOURCE_TAGS[key]
    labels = DISPLAY[key]
    assert len(sentences) == len(tags) == len(labels), (key, len(sentences), len(tags), len(labels))
    x0, x1, y0, size = (1290, 1875, 210, 42) if mapped else (110, 1810, 250, 50)
    out = []
    for i, phrase in enumerate(labels):
        source = tags[i]
        item = dict(t="anim", name="pop_rows", x0=x0, x1=x1, y0=y0,
                    size=size, gap=0,
                    items=[dict(at=i, until=i + 1 if i + 1 < len(labels) else None,
                                tag=f"〔{source}〕" if source else None,
                                text=phrase,
                                col=SOURCE_COLORS.get(source, "orange"))])
        if item["items"][0]["tag"] is None:
            item["items"][0].pop("tag")
        out.append(item)
    return out


def chapter(key, title, bg, alts, scene_data, map_obj=None):
    scene = [background(bg, alts)]
    if map_obj:
        scene.append(map_obj)
    scene.extend(story_rows(key, scene_data, mapped=bool(map_obj)))
    return dict(key=key, title=title, chapter_title=title, scene=scene)


def main():
    scenes = json.loads((ROOT / "data" / f"{SLUG}_scenes.json").read_text(encoding="utf8"))
    assert [s["key"] for s in scenes] == KEYS
    by_key = {s["key"]: s for s in scenes}

    wide_june = battle_map(
        "wide",
        places=[
            place("wide", (.78, .28), "小谷城", "castle", at=2, side="r", col=RED, lsize=32),
            place("wide", (.74, .40), "虎御前山", "spot", at=2, side="l", col=GOLD, lsize=29),
            place("wide", (.60, .69), "横山城", "castle", at=4, side="l", col=BLUE, lsize=30),
            place("wide", (.66, .60), "竜ヶ鼻", "spot", at=4, side="r", col=BLUE, lsize=30),
            place("wide", (.02, .04), "位置は概略", "spot", at=0, side="r", col=GOLD, lsize=25),
        ],
        lines=[line("wide", [(.99, .59), (.78, .57), (.58, .59), (.38, .65), (.16, .79)],
                    "姉川", at=2, col=CYAN, lab=(.48, .62), lsize=30)],
    )

    wide_cast = battle_map(
        "wide",
        places=[
            place("wide", (.77, .28), "小谷城", "castle", at=0, side="r", col=RED, lsize=30),
            place("wide", (.88, .42), "大依山", "camp", at=3, side="l", col=GOLD, lsize=30),
            place("wide", (.02, .04), "位置は概略", "spot", at=0, side="r", col=GOLD, lsize=25),
        ],
        units=[unit("wide", "朝倉勢", [(.88, .42)], at=3,
                    sub="大依山〔N〕", col=RED, lsize=29, lab_off=(-44, 15))],
    )

    area_terrain = battle_map(
        "area",
        places=[
            place("area", (.76, .22), "小谷城", "castle", at=2, side="r", col=RED, lsize=30),
            place("area", (.89, .35), "大依山", "camp", at=0, side="r", col=GOLD, lsize=29),
            place("area", (.62, .72), "横山城", "castle", at=5, side="b", col=BLUE, lsize=30),
            place("area", (.65, .62), "竜ヶ鼻", "spot", at=6, side="l", col=BLUE, lsize=29),
            place("area", (.56, .46), "野村", "spot", at=7, side="r", col=RED, lsize=29),
            place("area", (.37, .46), "三田村", "spot", at=7, side="l", col=RED, lsize=29),
            place("area", (.05, .88), "琵琶湖", "spot", at=4, side="t", col=CYAN, lsize=28),
            place("area", (.02, .04), "位置は概略", "spot", at=0, side="r", col=GOLD, lsize=25),
        ],
        lines=[line("area", [(.97, .57), (.79, .57), (.61, .58), (.43, .61), (.28, .69), (.10, .82)],
                    "姉川", at=4, col=CYAN, lab=(.52, .59), lsize=30)],
    )

    map_dawn = battle_map(
        "main",
        places=[
            place("main", (.60, .43), "野村", "spot", at=4, side="r", col=RED, lsize=30),
            place("main", (.36, .43), "三田村", "spot", at=4, side="l", col=RED, lsize=30),
            place("main", (.02, .04), "位置・経路は概略", "spot", at=0, side="r", col=GOLD, lsize=24),
        ],
        lines=[line("main", [(.98, .55), (.78, .58), (.58, .61), (.36, .60), (.12, .62), (.00, .63)],
                    "姉川", at=0, col=CYAN, lab=(.52, .60), lsize=30)],
        units=[unit("main", "浅井・朝倉", [(.76, .34), (.61, .49)], legs=[[2, 4]],
                    at=0, sub="二手に備える〔N〕", col=RED, lsize=28, dashed=True,
                    lab_off=(-50, -5))],
    )

    west_map = battle_map(
        "core",
        places=[
            place("core", (.35, .46), "三田村口", "spot", at=1, side="l", col=GOLD, lsize=28),
            place("core", (.61, .47), "野村", "spot", at=0, side="r", col=GOLD, lsize=28),
            place("core", (.02, .04), "位置・経路は概略", "spot", at=0, side="r", col=GOLD, lsize=24),
        ],
        lines=[line("core", [(.00, .56), (.27, .59), (.48, .57), (.72, .59), (1.0, .57)],
                    "姉川", at=0, col=CYAN, lab=(.48, .58), lsize=30)],
        units=[
            unit("core", "徳川家康", [(.58, .77), (.36, .49)], legs=[[2, 3]], at=0,
                 sub="西の三田村口へ〔N〕", col=BLUE, portrait="p_ieyasu", head=34,
                 lsize=26, dashed=True, lab_off=(42, -12)),
            unit("core", "朝倉勢", [(.29, .43)], at=6, col=RED,
                 lsize=28, lab_off=(-42, -10)),
        ],
    )

    east_map = battle_map(
        "core",
        places=[
            place("core", (.60, .46), "野村", "spot", at=0, side="r", col=GOLD, lsize=28),
            place("core", (.79, .47), "さらに東", "spot", at=2, side="r", col=GOLD, lsize=26),
            place("core", (.02, .04), "位置・経路は概略", "spot", at=0, side="r", col=GOLD, lsize=24),
        ],
        lines=[line("core", [(.00, .56), (.27, .59), (.48, .57), (.72, .59), (1.0, .57)],
                    "姉川", at=0, col=CYAN, lab=(.32, .58), lsize=29)],
        units=[
            unit("core", "信長の馬廻", [(.42, .79), (.58, .47)], legs=[[0, 1]], at=0,
                 sub="野村へ〔N〕", col=BLUE, portrait="p_nobunaga", head=34,
                 lsize=26, dashed=True, lab_off=(42, -12)),
            unit("core", "美濃三人衆", [(.76, .80), (.80, .48)], legs=[[2, 3]], at=0,
                 sub="さらに東へ〔N〕", col=BLUE, lsize=26, dashed=True,
                 lab_off=(-44, -8)),
            unit("core", "浅井方", [(.66, .40)], at=4,
                 sub="相手と語られる〔通説〕", col=RED, lsize=25, lab_off=(-42, 15)),
        ],
        marks=[
            dict(xy=point("core", .51, .59), at=5, label="十一段崩し〔軍〕", col=GOLD),
        ],
    )

    battle_map_decide = battle_map(
        "core",
        places=[place("core", (.02, .04), "位置・経路は概略", "spot", at=0,
                      side="r", col=GOLD, lsize=24)],
        lines=[line("core", [(.00, .56), (.27, .59), (.48, .57), (.72, .59), (1.0, .57)],
                    "姉川", at=0, col=CYAN, lab=(.47, .58), lsize=30)],
        units=[
            unit("core", "織田・徳川", [(.43, .78), (.49, .59)], legs=[[2, 4]],
                 at=0, col=BLUE, lsize=28, dashed=True, lab_off=(-42, 18)),
            unit("core", "浅井・朝倉", [(.65, .32), (.54, .57)], legs=[[2, 4]],
                 at=0, col=RED, lsize=28, dashed=True, lab_off=(42, -12)),
        ],
        marks=[dict(xy=point("core", .52, .58), at=6,
                    label="追い崩し〔N〕", col=GOLD)],
    )

    map_kubi = battle_map(
        "mid",
        places=[
            place("mid", (.59, .70), "横山城", "castle", at=6, side="b", col=BLUE, lsize=30),
            place("mid", (.80, .30), "大谷", "spot", at=5, side="r", col=RED, lsize=29),
            place("mid", (.02, .04), "位置・経路は概略", "spot", at=0, side="r", col=GOLD, lsize=24),
        ],
        lines=[line("mid", [(.98, .57), (.77, .58), (.58, .59), (.35, .62), (.12, .73)],
                    "姉川", at=0, col=CYAN, lab=(.54, .59), lsize=29)],
        units=[unit("mid", "信長勢", [(.61, .57), (.80, .30), (.59, .70)],
                    legs=[[5, 6], [6, 7]], at=0, sub="大谷へ、横山へ戻る〔N〕",
                    col=BLUE, portrait="p_nobunaga", head=32, lsize=26,
                    dashed=True, lab_off=(-44, -8))],
    )

    chapters = [
        chapter("kanegasaki", "金ヶ崎の退き口", "art_dawn",
                ["art_docs", "art_castle", "art_river"], by_key["kanegasaki"]),
        chapter("june", "虎御前山と竜ヶ鼻", "art_castle",
                ["art_dawn", "art_river", "art_docs"], by_key["june"], wide_june),
        chapter("cast", "両軍の顔ぶれ", "art_docs",
                ["art_castle", "art_dawn", "art_river"], by_key["cast"], wide_cast),
        chapter("terrain", "戦場の地形", "art_river",
                ["art_dawn", "art_docs", "art_castle"], by_key["terrain"], area_terrain),
        chapter("dawn", "陣払い、未明", "art_dawn",
                ["art_river", "art_castle", "art_docs"], by_key["dawn"], map_dawn),
        chapter("west", "西の戦場：徳川と朝倉", "art_river",
                ["art_dawn", "art_docs", "art_castle"], by_key["west"], west_map),
        chapter("east", "東の戦場：織田と浅井", "art_dawn",
                ["art_castle", "art_river", "art_docs"], by_key["east"], east_map),
        chapter("decide", "卯の刻、姉川", "art_river",
                ["art_dawn", "art_docs", "art_castle"], by_key["decide"], battle_map_decide),
        chapter("kubi", "首注文と追い討ち", "art_docs",
                ["art_river", "art_castle", "art_dawn"], by_key["kubi"], map_kubi),
        chapter("after", "戦いの後", "art_castle",
                ["art_docs", "art_dawn", "art_river"], by_key["after"]),
    ]

    images = {
        "wide": {"file": "assets/anegawa/map_wide.png"},
        "main": {"file": "assets/anegawa/map_main.png", "crop": CROPS["main"]},
        "mid": {"file": "assets/anegawa/map_mid.png", "crop": CROPS["mid"]},
        "area": {"file": "assets/anegawa/map_area.png"},
        "core": {"file": "assets/anegawa/map_core.png", "crop": CROPS["core"]},
        "art_castle": {"file": "assets/anegawa/art_castle.png"},
        "art_dawn": {"file": "assets/anegawa/art_dawn.png"},
        "art_docs": {"file": "assets/anegawa/art_docs.png"},
        "art_river": {"file": "assets/anegawa/art_river.png"},
        "p_ieyasu": {"file": "assets/portraits/ieyasu.jpg"},
        "p_nobunaga": {"file": "assets/portraits/nobunaga.jpg"},
    }

    spec = dict(
        slug=SLUG,
        theme_dir=THEME,
        pack=PACK,
        style="pop",
        header_sub="姉川の戦いを、同時代の記録・軍記・通説・説に分けて見る",
        images=images,
        bgm=[
            ["kanegasaki", "cast", "piano35"],
            ["terrain", "dawn", "ethnic31"],
            ["west", "decide", "orchestra25"],
            ["kubi", "after", "acoustic48"],
        ],
        chapters=chapters,
    )

    out = ROOT / "data" / f"{SLUG}_spec.json"
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
