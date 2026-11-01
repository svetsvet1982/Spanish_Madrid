"""원고_md/N부/*.md → PDF/빛과속기사_N부.pdf (부 단위 합본, 화마다 새 페이지)
사용: python3 도구/md2pdf.py [부 번호 ...]  (인자 없으면 있는 부 전체)"""
import re, sys, glob, os, html, asyncio
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TURN = re.compile(r'^([^(#\-\[*\s][^:]{0,40}?)( \(V\.O\.\))?: (.*)$')
TITLES = {1:"커미션 · La Comisión",2:"배관공들 · Las Fontaneras",3:"벽돌 · Ladrillo",4:"해협 · El Estrecho",5:"진흙 · Barro",6:"오프사이드 · Fuera de Juego",7:"빛과 속기사 · Luz y Taquígrafos"}
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400&display=swap');
@page { size: A4; margin: 18mm 17mm 18mm 17mm;}
body { font-family: 'Noto Serif','Noto Sans KR','WenQuanYi Zen Hei',serif; font-size: 10.5pt; line-height: 1.5; color:#111; }
.ko, h1, h2, .meta, .gl, .end { font-family: 'Noto Sans KR','WenQuanYi Zen Hei',sans-serif; }
.cover { height: 250mm; display:flex; flex-direction:column; justify-content:center; text-align:center; page-break-after: always; }
.cover .t { font-size: 30pt; font-weight:700; } .cover .s { font-size: 16pt; margin-top:6mm; } .cover .p { font-size: 20pt; margin-top: 18mm; }
.toc { page-break-after: always; } .toc li { margin: 1.5mm 0; }
.ep { page-break-before: always; }
h1 { font-size: 15pt; border-bottom: 1.5px solid #333; padding-bottom: 2mm; }
h2 { font-size: 11.5pt; margin-top: 6mm; color:#1f3a5f; }
.meta { font-size: 9.5pt; margin: 1.5mm 0; } .meta b { color:#1f3a5f; }
.dir { font-style: italic; color:#444; margin: 2mm 0 2mm 0; }
.ln { margin: 0.8mm 0 0.8mm 0; padding-left: 0; } .ln .n { font-weight:700; } .ln .vo { font-style: italic; color:#555; } .ln i { color:#555; }
.gl { font-size: 9.5pt; margin: 1.2mm 0; } .gl b { font-family:'Noto Serif',serif; }
.end { font-style: italic; color:#555; margin-top: 5mm; font-size: 9.5pt; }
"""
def inline(t):
    t = html.escape(t)
    return re.sub(r'(\([^)]*\))', r'<i>\1</i>', t)
def ep_html(md):
    out = ['<section class="ep">']
    for line in open(md, encoding='utf-8').read().splitlines():
        s = line.strip()
        if not s: continue
        if s.startswith('# '): out.append(f'<h1>{html.escape(s[2:])}</h1>')
        elif s.startswith('## '): out.append(f'<h2>{html.escape(s[3:])}</h2>')
        elif s.startswith('**') and ':**' in s:
            k, v = s[2:].split(':**', 1); out.append(f'<p class="meta"><b>{html.escape(k)}:</b> {html.escape(v.strip())}</p>')
        elif s.startswith('- «'):
            q, _, rest = s[2:].partition('» — '); out.append(f'<p class="gl"><b>{html.escape(q)}»</b> — {html.escape(rest)}</p>')
        elif s.startswith('['): out.append(f'<p class="end">{html.escape(s)}</p>')
        elif s.startswith('('): out.append(f'<p class="dir">{html.escape(s)}</p>')
        elif (m := TURN.match(s)):
            n, vo, t = m.groups()
            out.append(f'<p class="ln"><span class="n">{html.escape(n)}</span>{" <span class=vo>(V.O.)</span>" if vo else ""}: {inline(t)}</p>')
        else: out.append(f'<p class="ln">{inline(s)}</p>')
    out.append('</section>'); return '\n'.join(out)
def epno(f): return int(re.search(r'_(\d+)화', f).group(1))
def main(parts):
    import subprocess, tempfile
    os.makedirs(os.path.join(ROOT, 'PDF'), exist_ok=True)
    jobs = []
    tmp = tempfile.mkdtemp()
    for n in parts:
        files = sorted(glob.glob(os.path.join(ROOT, '원고_md', f'{n}부', '*화_*.md')), key=epno)
        if not files: continue
        toc = ''.join(f'<li>{html.escape(open(f,encoding="utf-8").readline()[2:].strip())}</li>' for f in files)
        doc = f'<!doctype html><html lang="es"><meta charset="utf-8"><style>{CSS}</style><body>'
        doc += f'<div class="cover ko"><div class="t">빛과 속기사</div><div class="s">Luz y Taquígrafos</div><div class="p">{n}부 「{TITLES[n]}」</div><div class="s" style="font-size:11pt;margin-top:20mm">마드리드 탐사보도 7부작 · 15화 × 150턴</div></div>'
        doc += f'<div class="toc ko"><h1>차례 — {n}부</h1><ol>{toc}</ol></div>'
        doc += ''.join(ep_html(f) for f in files) + '</body></html>'
        h = os.path.join(tmp, f'{n}.html'); open(h, 'w', encoding='utf-8').write(doc)
        jobs.append((h, os.path.join(ROOT, 'PDF', f'빛과속기사_{n}부.pdf')))
    js = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html2pdf.js')
    subprocess.run(['node', js] + [x for j in jobs for x in j], check=True)
main([int(a) for a in sys.argv[1:]] or range(1, 8))
