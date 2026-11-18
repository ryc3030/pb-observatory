"""기계 번역 제목 다듬기(정문 v2.8의 원칙을 제목에 맞게 줄인 후처리기).

기계 번역은 뉴스 제목을 "~이 시작되었습니다."처럼 존댓말 문장으로 옮기고, '참여 예산'을 띄어 쓰며,
같은 지명을 여러 표기로 쓴다. 여기서는 의미를 바꾸지 않는 범위에서만 고친다.
  1) 용어 통일: 참여예산·주민참여예산·시민예산 붙여 쓰기, 지명 표기 통일
  2) 뉴스 제목 끝: 존댓말 문장 → 신문 제목체(명사형·해라체), 마침표·느낌표 제거
  3) 번역투: 정문 N06 사전에서 제목에 흔한 꼴만 골라 고침
숫자·고유명·인용부호 안은 건드리지 않는다. 같은 입력에는 늘 같은 출력이 나오므로 여러 번 돌려도 안전하다.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------- 1) 용어·지명
TERMS = [
    (r"(주민|시민|국민|청소년|학교|어린이|청년)\s+참여\s*예산", r"\1참여예산"),
    (r"참여\s+예산", "참여예산"),
    (r"참여형\s*예산(?:\s*편성)?", "참여예산"),
    (r"참여적\s*예산(?:\s*편성)?", "참여예산"),
    (r"참여예산\s+제(?=[\s,.:!?]|$)", "참여예산제"),
    (r"시민\s+예산", "시민예산"),
    (r"주민\s+예산", "주민예산"),
    (r"공동체\s+예산", "공동체예산"),
    (r"포르투\s*알레그[레리]", "포르투알레그리"),
    (r"상파울로", "상파울루"),
    (r"벨[루로]\s*오리[존종]\s*[치테]", "벨루오리존치"),
    (r"헬싱키의\s*오마\s*스타디|오마\s+스타디", "오마스타디"),
]

# ---------------------------------------------------------------- 3) 번역투(N06 중 제목에 나오는 꼴)
N06_TITLE = [
    (r"도전\s*과제", "과제"),
    (r"을\s*통해서", "을 통해"),
    (r"를\s*통해서", "를 통해"),
    (r"에\s*있어서", "에서"),
]

# ---------------------------------------------------------------- 2) 제목 끝
_ADJ = set("높낮많적좋넓깊같길짧싫옳작")  # '~습니다' 앞이 형용사 어간이면 '~다'


def _jamo_n_final(syl: str) -> str:
    """받침 없는/ㅂ받침 음절에 ㄴ받침을 붙인다(합→한, 됩→된, 갑→간)."""
    code = ord(syl) - 0xAC00
    if not (0 <= code < 11172):
        return syl
    base = code - code % 28
    return chr(0xAC00 + base + 4)  # 4 = ㄴ


def plain_ending(t: str) -> str:
    """존댓말 종결(~습니다/~ㅂ니다)을 해라체로."""
    t = re.sub(r"입니다$", "이다", t)
    t = re.sub(r"(있|없)습니다$", r"\1다", t)
    t = re.sub(r"(었|았|였|했|됐|웠|겠|갔|왔|졌|켰|쳤|섰|냈|봤|줬)습니다$", r"\1다", t)
    m = re.search(r"([가-힣])습니다$", t)
    if m:
        stem = m.group(1)
        t = t[: m.start()] + stem + ("다" if stem in _ADJ else "는다")
    m = re.search(r"([가-힣])니다$", t)  # 합니다·됩니다·갑니다(ㅂ받침)
    if m and (ord(m.group(1)) - 0xAC00) % 28 == 17:  # 17 = ㅂ받침
        t = t[: m.start()] + _jamo_n_final(m.group(1)) + "다"
    return t


_NOMINAL_ENDING = re.compile(r"(^|[\s(])([가-힣]{2,4})(했다|됐다|되었다|하였다|한다|된다|하다|되다)$")
_NOT_NOUN = {"생각", "말씀", "위", "인", "의", "대"}


def _has_final(ch: str) -> bool:
    code = ord(ch) - 0xAC00
    return 0 <= code < 11172 and code % 28 != 0


def _particle_ok(word: str, p: str) -> bool:
    """조사가 앞말 받침과 맞을 때만 조사로 본다(어린이·놀이 같은 낱말 끝 '이'를 조사로 오인하지 않게)."""
    if not word or not re.match(r"[가-힣]", word[-1]):
        return p in ("가", "는")  # 영문·숫자 뒤
    fin = _has_final(word[-1])
    return (p in ("이", "은") and fin) or (p in ("가", "는") and not fin)


def _drop_subject(t: str) -> str:
    """명사형으로 끝난 제목의 주어 조사를 제목체로: '회차가 시작' → '회차 시작', '칼리는 … 추진' → '칼리, … 추진'."""
    m = re.search(r"(\S+?)(이|가) (\S+(?: 중| 전망)?)$", t)
    if (m and _particle_ok(m.group(1), m.group(2)) and not re.match(r"(할|될) ", m.group(3))
            and " " not in m.group(3).replace(" 중", "").replace(" 전망", "")):
        return t[: m.start()] + m.group(1) + " " + m.group(3)
    for m in re.finditer(r"(?:(?<=^)|(?<=\s))(\S+?)(은|는|가|이) ", t):
        w, p = m.group(1), m.group(2)
        if re.search(r"(에서|에게|으로|로|에|와|과|의)$", w) or not _particle_ok(w, p):
            continue
        if len(t) - m.end() < 6:  # 남은 말이 짧으면(이미 위에서 처리) 두지 않음
            break
        return t[: m.start()] + w + ", " + t[m.end():]
    return t


def headline(t: str) -> str:
    """해라체 문장을 신문 제목체로: '~을 시작했다' → '~을 시작', '~하고 있다' → '~ 중', '~할 것이다' → '~할 전망'."""
    before = t
    t = re.sub(r"([가-힣]{2,4})(하|되)고\s*있다$", r"\1 중", t)
    t = re.sub(r"(할|될)\s*것이다$", r"\1 전망", t)
    m = _NOMINAL_ENDING.search(t)
    if m and m.group(2) not in _NOT_NOUN:
        t = t[: m.start(2)] + m.group(2)
    t = re.sub(r"(중|전망|예정|계획|결과|목록|대상|시작|마감)이다$", r"\1", t)
    if t != before and not re.search(r"(다)$", t):
        t = _drop_subject(t)
    return t


def polish(text: str | None, kind: str = "news") -> str | None:
    if not text:
        return text
    t = re.sub(r"\s+", " ", text).strip()
    for a, b in TERMS + N06_TITLE:
        t = re.sub(a, b, t)
    if kind == "news":
        # 여러 문장으로 된 제목은 문장마다 끝을 다듬는다
        parts = re.split(r"(?<=[.!])\s+(?=\S)", t)
        out = []
        for s in parts:
            s = s.strip()
            tail = ""
            m = re.search(r"([.!]+|…)$", s)
            if m and m.group(1) != "…":
                s = s[: m.start()].rstrip()
            if re.search(r"(니다|습니다)$", s):
                s = headline(plain_ending(s))
            elif re.search(r"(했다|됐다|한다|된다|이다|하다|되다)$", s):
                s = headline(s)
            out.append(s + tail)
        t = ""
        for x in out:
            if not x:
                continue
            t = x if not t else t + (" " if re.match(r"[•\-–—|·:]", x) else ". ") + x
        t = re.sub(r"\s*[.!]+$", "", t)
    return t


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        print(polish(line.strip()))
