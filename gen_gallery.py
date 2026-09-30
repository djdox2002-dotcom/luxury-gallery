#!/usr/bin/env python3
"""photos 폴더 사진들을 읽어서 index.html 생성 (액자형 다크 테마 갤러리).

- 대문(hero.jpg)은 사진 비율(2907x3215)에 맞춘 aspect-ratio 영역에
  object-fit: contain 으로 잘리지 않게 표시
- 앨범 사진은 가로 방향으로 추억1 -> 2 -> ... -> N 순서로 배치
- 각 앨범 사진은 동일 크기 액자(aspect-ratio: 4/3) 안에
  object-fit: cover 로 빈틈없이 꽉 차게 표시
- 사진은 photos 폴더에 추가된 시간순으로 추억 번호를 붙인다.
"""

from pathlib import Path
import datetime

BASE = Path(__file__).parent
PHOTOS = BASE / "photos"
IDX = BASE / "index.html"

ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}

# 폴더에 추가된 시간순(가장 최근 넣은 사진이 뒤쪽)으로 정렬
def _mtime(p: Path) -> float:
    return p.stat().st_mtime

images = sorted(
    [p for p in PHOTOS.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED],
    key=_mtime,
)
images = [p.name for p in images]

hero_ok = (BASE / "hero.jpg").is_file()

cards = []
for i, fname in enumerate(images, start=1):
    title = f"추억{i}"
    cards.append(
        '            <div class="card">\n'
        '                <div class="frame">\n'
        f'                    <img src="photos/{fname}" alt="{title}">\n'
        "                </div>\n"
        f'                <div class="caption">{title}</div>\n'
        "            </div>"
    )

cards_html = "\n".join(cards) if cards else (
    '            <p class="no-photos">아직 사진이 없습니다. photos 폴더에 사진을 넣어주세요.</p>'
)

year = datetime.date.today().year

hero_img_tag = "<img src='hero.jpg' alt='대문 사진'>" if hero_ok else ""

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>나의 사진 갤러리</title>
<style>
:root {{
  --bg: #111;
  --gold: #d4af37;
  --text: #f2f2f2;
  --muted: #9a9a9a;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ height: 100%; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: 'Noto Serif KR', Georgia, 'Times New Roman', serif;
  min-height: 100vh;
}}

/* ---------- Hero ---------- */
.hero {{
  position: relative;
  width: 100%;
  aspect-ratio: 2907 / 3215;   /* 대문사진 비율(가로:세로)에 딱 맞춤 */
  overflow: hidden;
  background: #000;
}}
.hero img {{
  width: 100%;
  height: 100%;
  object-fit: contain;        /* 대문사진은 잘리지 않고 온전히 표시 */
  object-position: center;   /* 정중앙 기준 */
  display: block;
  filter: brightness(0.82) saturate(1.02);
}}
.hero-title {{
  position: absolute;
  left: 0; right: 0; bottom: 0;
  padding: 2.2rem 1.8rem 1.6rem;
  background: linear-gradient(to top, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0) 100%);
  pointer-events: none;
}}
.hero-title h1 {{
  font-size: clamp(1.6rem, 4vw, 3rem);
  font-weight: 500;
  letter-spacing: 0.14em;
  color: #d4af37;              /* 노랑색 앨범 장식과 동일한 색 */
  text-shadow: 0 2px 10px rgba(0,0,0,0.6);
}}
.hero-title p {{
  margin-top: 0.25rem;
  font-size: clamp(0.85rem, 1.4vw, 1.05rem);
  color: rgba(255,255,255,0.75);
  letter-spacing: 0.08em;
}}

/* ---------- Gallery ---------- */
.wrap {{
  max-width: 1280px;
  margin: 0 auto;
  padding: 2.6rem 1.4rem 1rem;
}}

/* === 가로 방향으로 순서대로 배치 === */
.grid {{
  display: flex;
  flex-wrap: wrap;
  gap: 1.4rem;
}}
.card {{
  flex: 0 0 calc((100% - 4.2rem) / 4);   /* 기본 4열 */
  min-width: 160px;
  margin-bottom: 0;
  break-inside: avoid;
}}
.frame {{
  position: relative;
  aspect-ratio: 4 / 3;        /* 모든 액자 동일 크기 */
  background: #1b1b1b;         /* 매트(액자 뒷판) */
  padding: 6px 6px 7px;        /* 액자 외곽 테두리 */
  border: 2px solid #0c0c0c;  /* 액자 외각테 */
  outline: 1px solid rgba(212,175,55,0.32);  /* 금빛 아우트라인 */
  box-shadow:
      0 4px 14px rgba(0,0,0,0.7),
      inset 0 0 0 1px rgba(212,175,55,0.12);
  transition:
      transform .28s ease,
      box-shadow .28s ease,
      outline-color .28s ease,
      border-color .28s ease;
}}
.frame:hover {{
  transform: translateY(-3px);
  border-color: #161616;
  outline-color: rgba(212,175,55,0.75);
  box-shadow:
      0 12px 30px rgba(0,0,0,0.8),
      inset 0 0 0 1px rgba(212,175,55,0.22);
}}

.frame img {{
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;        /* 액자 안을 빈틈없이 꽉 채움 */
  object-position: center;   /* 정중앙 기준 */
  background: #0a0a0a;
}}

.caption {{
  margin: 0.7rem 0.4rem 0;
  padding: 0 0.2rem;
  font-size: 0.82rem;
  color: var(--gold);
  letter-spacing: 0.06em;
  opacity: 0;
  transition: opacity .25s ease;
}}
.frame:hover + .caption,
.card:hover .caption {{ opacity: 1; }}

.no-photos {{
  text-align: center;
  color: var(--muted);
  padding: 3rem 0;
  font-size: 0.95rem;
}}
footer {{
  text-align: center;
  padding: 2rem 1rem 2.4rem;
  color: #555;
  font-size: 0.82rem;
  letter-spacing: 0.05em;
  border-top: 1px solid rgba(255,255,255,0.05);
  margin-top: 1rem;
}}

/* 반응형: 화면 좁으면 열 수 줄임 */
@media (max-width: 900px) {{
  .card {{ flex: 0 0 calc((100% - 2.8rem) / 3); }}
}}
@media (max-width: 640px) {{
  .card {{ flex: 0 0 calc((100% - 1.4rem) / 2); }}
}}
@media (max-width: 420px) {{
  .card {{ flex: 0 0 100%; }}
}}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>

<section class="hero">
  {hero_img_tag}
  <div class="hero-title">
    <h1>나의 사진 갤러리</h1>
    <p>소중한 순간들</p>
  </div>
</section>

<div class="wrap">
  <div class="grid">
{cards_html}
  </div>
</div>

<footer>
  &copy; {year} 나의 사진 갤러리
</footer>

</body>
</html>
"""

IDX.write_text(html, encoding="utf-8")
print(f"[OK] index.html 생성됨 — 사진 {len(images)}장 반영 (hero: {'있음' if hero_ok else '없음'})")
