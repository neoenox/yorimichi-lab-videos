"""spec を書くための共通の部品（make_spec_*.py から import する）。姉川の比較検証で作った書き方を、誰でも使えるようにしたもの。
  ・テロップ／右の列の文（pop）：tel / rtel / rows / seq_rows / note
  ・戦況地図：place / unit / river / bmap（座標は、いちばん広い地図の正規化座標で書く。詳細な地図には自動で換算）
  ・詳細な地図が、広い地図のどこにあたるかは、画像の位置合わせ（SIFT）で自動で求める：auto_extents()
書き方の例は、scripts/make_spec_anesonnet3.py。
文の入れ替え（rows の落とし穴）：同じ pop_rows の中の文は、まだ出ていない文の場所も、最初から下に確保される。
  順に入れ替えたいときは、seq_rows を使う（1つずつ別の pop_rows にして、前の文を until で消す）。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = [30, 100, 1230, 836]    # 地図の枠（字幕の帯 y836 の手前まで）
RX0, RX1 = 1290, 1890         # 地図の右の列
SUB_TOP = 836


def bgi(img, alts=(), dim=0.55, blur=4, seg=22):
    return dict(t='anim', name='pop_bgimg', img=img, at=0, dim=dim, blur=blur, alts=list(alts), seg=seg)


def tel(text, at, until=None, x=960, y=330, size=100, plate=None, rot=-1.5, maxw=1560):
    d = dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, at=at, plate=plate, rot=rot, maxw=maxw)
    if until is not None:
        d['until'] = until
    return d


def rtel(text, at, until=None, plate='yellow', y=250, size=58):
    """右の列のテロップ"""
    return tel(text, at, until, x=(RX0 + RX1) // 2, y=y, size=size, plate=plate, maxw=580)


def rows(items, y0=370, size=40, x0=RX0, x1=RX1, gap=14, ymax=None):
    """右の列の文は、注記（y770）の手前（y755）で自動的に縮んで止まる。"""
    d = dict(t='anim', name='pop_rows', items=items, x0=x0, x1=x1, y0=y0, size=size, gap=gap)
    if ymax is None and x0 == RX0 and y0 < 700:
        ymax = 755
    if ymax:
        d['ymax'] = ymax
    return d


def seq_rows(entries, y0=360, size=38, **kw):
    """順に入れ替える文。entries=[(at, tag, text, col), ...]。各文は次の文の at で消える（最後の文は残る）。"""
    out = []
    for k, e in enumerate(entries):
        at, tag, text, col = e[:4]
        it = dict(at=at, tag=tag, text=text, col=col)
        if k + 1 < len(entries):
            it['until'] = entries[k + 1][0]
        out.append(rows([it], y0=y0, size=size, **kw))
    return out


def note(text='現代の地形。位置は目安です', y0=770):
    return rows([dict(at=0, text=text, col='cyan')], y0=y0, size=28, gap=0)


def place(xy, label, kind, col, side='r', at=0, lsize=34):
    return dict(xy=list(xy), label=label, kind=kind, col=list(col), side=side, at=at, lsize=lsize)


def unit(label, col, pts, at=0, legs=None, portrait=None, sub=None, until=None, dashed=False, head=34, lab_off=None, lsize=34, trail=True):
    u = dict(label=label, col=list(col), pts=[list(p) for p in pts], at=at, head=head, lsize=lsize, trail=trail)
    for k, v in (('legs', legs), ('portrait', portrait), ('sub', sub), ('until', until), ('lab_off', list(lab_off) if lab_off else None)):
        if v is not None:
            u[k] = v
    if dashed:
        u['dashed'] = True
    return u


def river(pts, label='川', col=(90, 160, 245), at=0, lab=None, lsize=34):
    d = dict(pts=[list(p) for p in pts], label=label, col=list(col), at=at, lsize=lsize)
    if lab:
        d['lab'] = list(lab)
    return d


class Maps:
    """基準の地図（広い地図）と、詳細な地図の対応。座標は基準の地図の正規化座標で書く。
    Maps('area', {'area': (0,0,1,1), 'core': (0.318,0.318,0.818,0.909)})  または  Maps.auto('area', {'area': path, 'core': path, ...})"""

    def __init__(self, base, ext):
        self.base, self.ext = base, dict(ext)

    @classmethod
    def auto(cls, base, files):
        """files={キー: 画像ファイル}（基準の地図を含む）。詳細な地図の範囲は、SIFT の位置合わせで求め、data/map_extents.json に保存する。"""
        ext = {base: (0, 0, 1, 1)}
        for k, f in files.items():
            if k != base:
                ext[k] = auto_extent(files[base], f)
        return cls(base, ext)

    def conv(self, img, q):
        x0, y0, x1, y1 = self.ext[img]
        return [round((q[0] - x0) / (x1 - x0), 4), round((q[1] - y0) / (y1 - y0), 4)]

    def bmap(self, img=None, places=(), lines=(), units=(), marks=(), at=0, until=None, box=None):
        img = img or self.base
        P = [dict(o, xy=self.conv(img, o['xy'])) for o in places]
        L = []
        for o in lines:
            o = dict(o, pts=[self.conv(img, q) for q in o['pts']])
            if 'lab' in o:
                o['lab'] = self.conv(img, o['lab'])
            L.append(o)
        U = [dict(o, pts=[self.conv(img, q) for q in o['pts']]) for o in units]
        M = [dict(o, xy=self.conv(img, o['xy'])) for o in marks]
        d = dict(t='anim', name='battle_map', img=img, box=list(box or BOX), at=at, places=P, lines=L, units=U, marks=M)
        if until is not None:
            d['until'] = until
        return d


def auto_extent(base_file, detail_file):
    """detail が base のどの範囲か（左,上,右,下。base の正規化座標）。結果は data/map_extents.json に保存する。"""
    cache = ROOT / 'data' / 'map_extents.json'
    db = json.loads(cache.read_text(encoding='utf8')) if cache.exists() else {}
    bf, df = ROOT / base_file, ROOT / detail_file
    key = f'{base_file}|{detail_file}|{bf.stat().st_size}|{df.stat().st_size}'
    if key in db:
        return tuple(db[key])
    import cv2
    import numpy as np
    A = cv2.imread(str(bf), 0)
    B = cv2.imread(str(df), 0)
    h = int(min(A.shape[0], B.shape[0]) * 0.9)   # 下端の出典の帯を除く
    sift = cv2.SIFT_create(4000)
    ka, da = sift.detectAndCompute(A[:h], None)
    kb, db_ = sift.detectAndCompute(B[:h], None)
    m = cv2.BFMatcher().knnMatch(db_, da, k=2)
    good = [a for a, b in m if a.distance < 0.75 * b.distance]
    if len(good) < 12:
        raise RuntimeError(f'位置合わせできない（対応点 {len(good)}）。{detail_file} は {base_file} の一部ではない可能性')
    src = np.float32([kb[g.queryIdx].pt for g in good])
    dst = np.float32([ka[g.trainIdx].pt for g in good])
    M, inl = cv2.estimateAffinePartial2D(src, dst, ransacReprojThreshold=4)
    if M is None or inl.sum() < 12:
        raise RuntimeError('位置合わせに失敗')
    H, W = B.shape
    c = cv2.transform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]).reshape(-1, 1, 2), M).reshape(-1, 2)
    ext = (float(c[:, 0].min() / A.shape[1]), float(c[:, 1].min() / A.shape[0]), float(c[:, 0].max() / A.shape[1]), float(c[:, 1].max() / A.shape[0]))
    db[key] = [round(v, 4) for v in ext]
    cache.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf8')
    return tuple(db[key])
