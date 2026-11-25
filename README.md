# The World in One Image — 25 November 2026

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Tiannuryadins/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Tiannuryadins/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for [news-image-20261125](https://make.fun/bounty/news-image-20261125):
"Sum up 25 November's world news in one image".

`main.py` (Python 3, standard library only) copies the sibling
`poster.png` — a 1024×1024 newspaper front page rendered at build time
by `render_poster.py` from verified 25 November 2026 news — to
`/output/entry.png` (two runs produce identical bytes; no network at
runtime).

Structure (per the news-image playbook: every story illustrated):
31 stories in 3 layers — 3 large leads (Nvidia slides 7% as lawmakers
question Trump's role in Huang's return; mines hit two tankers in the
Strait of Hormuz; Asia's AI sell-off deepens), 10 illustrated cards
(Microsoft's "Code Red" outage, Shenzhou-24 with Pakistan's first
astronaut, Cartagena hostage siege, Senegal regain the AFCON crown,
Solomon Islands–Australia security treaty, Democrats take the House
with 259 seats, Spain heads to snap polls, Trump readies new tariffs
on 16 partners, Bangladesh garment workers win +36%, Russian jets
enter Korea's ADIZ), a world map with 15 story dots, and an 18-line
index. 14 illustrations (13 scenes + map), 7-stat number strip, red
italic dek naming the top 3 stories, 7 region tabs, serif masthead.
All figures checked against live sources on 25 Nov 2026 (BBC,
The Guardian, Reuters, AP, The Hindu, OneTurn, Newsof.today, SRI).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```
