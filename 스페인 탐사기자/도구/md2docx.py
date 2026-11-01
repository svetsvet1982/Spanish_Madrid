"""원고_md/N부/*.md → N부/*.docx (기존 스페인판 대본 서식과 동일)
사용: python3 md2docx.py [md파일 ...]  (인자 없으면 전체 변환)"""
import re, sys, glob, os
import docx
from docx.shared import Pt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TURN = re.compile(r'^([^(#\-\[*][^:]{0,40}?)( \(V\.O\.\))?: (.*)$')
def runs(p, text, size, bold=False):
    for part in re.split(r'(\([^)]*\))', text):
        if not part: continue
        r = p.add_run(part); r.font.size = Pt(size); r.bold = bold
        if part.startswith('(') and part.endswith(')'): r.italic = True
def conv(md):
    d = docx.Document()
    for line in open(md, encoding='utf-8').read().splitlines():
        s = line.strip()
        if not s: continue
        p = d.add_paragraph()
        if s.startswith('# '):
            r = p.add_run(s[2:]); r.bold = True; r.font.size = Pt(16)
        elif s.startswith('## '):
            r = p.add_run(s[3:]); r.bold = True; r.font.size = Pt(13)
        elif s.startswith('**') and ':**' in s:
            k, v = s[2:].split(':**', 1)
            r = p.add_run(k + ': '); r.bold = True; r.font.size = Pt(11)
            r = p.add_run(v.strip()); r.font.size = Pt(11)
        elif s.startswith('- «'):
            q, _, rest = s[2:].partition('» — ')
            r = p.add_run(q + '»'); r.bold = True; r.font.size = Pt(11)
            r = p.add_run(' — ' + rest); r.font.size = Pt(11)
        elif s.startswith('(') or s.startswith('['):
            r = p.add_run(s); r.italic = True; r.font.size = Pt(11)
        elif (m := TURN.match(s)):
            name, vo, text = m.groups()
            if vo:
                r = p.add_run(name + ' '); r.font.size = Pt(11)
                r = p.add_run('(V.O.)'); r.italic = True; r.font.size = Pt(11)
                r = p.add_run(': '); r.font.size = Pt(11)
            else:
                r = p.add_run(name + ': '); r.bold = True; r.font.size = Pt(11)
            runs(p, text, 11)
        else:
            runs(p, s, 11)
    rel = os.path.relpath(md, os.path.join(ROOT, '원고_md'))
    out = os.path.join(ROOT, os.path.splitext(rel)[0] + '.docx')
    os.makedirs(os.path.dirname(out), exist_ok=True); d.save(out); return out
files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, '원고_md', '*', '*.md')))
for f in files: print(conv(os.path.abspath(f)))
