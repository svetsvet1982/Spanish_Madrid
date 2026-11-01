"""대사 턴 수 계산 (생활 표현 섹션 이전의 '이름: ' / '이름 (V.O.): ' 줄만 센다)
사용: python3 도구/턴수.py 파일.md [...]   또는   python3 도구/턴수.py '원고_md/4부/*.md'"""
import re, sys, glob
pat = re.compile(r'^[^(#\-\[*\s][^:]{0,40}: ')
files = [g for a in sys.argv[1:] for g in (sorted(glob.glob(a)) or [a])]
for f in files:
    if '연속성_메모' in f: continue
    body = open(f, encoding='utf-8').read().split('## 생활 표현')[0]
    n = sum(1 for l in body.splitlines() if pat.match(l))
    print(n, 'OK' if n == 150 else 'XX', f)
