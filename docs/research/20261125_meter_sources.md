# メートルShort の根拠確認（2026-11-25）

対象: `solo_meter_light` / `solo_meter_before`。

## 一次資料（BIPM）

`https://www.bipm.org/en/history-si/metre` を bsk で開き、本文を直接読んだ（web_fetch ではナビゲーションの後に本文が truncation され、bsk で取得した）。

原文の要点（2026-11-25 確認）:
- The 1889 definition of the metre, namely, the length of the international prototype of platinum-iridium, was replaced by the 11th CGPM (1960) using a definition based on the wavelength of the radiation corresponding to a particular transition in krypton 86.
- This change was adopted in order to improve the accuracy with which the definition of the metre could be realized, this being achieved using an interferometer with a travelling microscope to measure the optical path difference as the fringes were counted.
- In turn, this was replaced in 1983 by the 17th CGPM (Resolution 1) with a definition referenced to the distance that light travels in vacuum in a specified interval of time.
- The original international prototype of the metre, which was sanctioned by the 1st CGPM in 1889, is still kept at the BIPM under conditions specified in 1889.
- In order to make clear its dependence on the fixed numerical value of the speed of light, the wording of the definition was changed in Resolution 1 of the 26th CGPM (2018).

関連決議へのリンクも同ページに載っている: CGPM Resolution 1 (2018) / Resolution 1 (1983) / Resolution 6 (1960) / Declaration (1889)。決議本文の内部文言は未確認（到達とページ上の記載のみ確認）。

## 台本との照合

| 台本の主張 | 判定 |
| --- | --- |
| 1889年に白金とイリジウムの国際原器ができた | BIPM 本文で確認 |
| 1960年に光の波（クリプトン86）による定義に替わった | BIPM 本文で確認 |
| 1983年から光の速さで決めている | BIPM 本文で確認 |
| 基準は三度替わった | 上記3点から言える |

## 二次資料のみ／未確認

- 1799年のダンケルク〜バルセロナの測量と、現在のメートルが当初の定義より約0.197ミリ短いという数値は、Wikipedia「History of the metre」で確認しただけで、BIPM 本文には無い。一次史料での照合は未実施。答え（基準が三度替わった）を変えるものではないので `needs_research` に「答えは変わらない」理由つきで残す。
- `scripts/gen_solo_meter.py` の docstring には「BIPMの原文照合は未実施」とあるが、notes には「一次確認済み」とある。今回 bsk で本文を確認したので docstring も実態に合わせる。
