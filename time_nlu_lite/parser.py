"""中文时间解析：把下周三下午三点 / 明天早上 解析成结构化 datetime。"""
from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ParsedTime:
    text: str
    datetime: str
    date: str
    time: str | None
    period: str | None
    is_time_exact: bool


_WEEKDAY_MAP = {"一":0,"二":1,"三":2,"四":3,"五":4,"六":5,"日":6,"天":6}
_PERIOD_HOUR = {"早上":8,"上午":9,"中午":12,"下午":14,"傍晚":17,"晚上":19}
_CN_NUM = {"零":0,"一":1,"二":2,"两":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10}


def _cn_to_int(s):
    if s is None: return None
    if s.isdigit(): return int(s)
    if s in _CN_NUM: return _CN_NUM[s]
    if s.startswith("十"): return 10 + (_CN_NUM.get(s[1:],0) if len(s)>1 else 0)
    if "十" in s:
        a,_,b = s.partition("十")
        return _CN_NUM.get(a,0)*10 + (_CN_NUM.get(b,0) if b else 0)
    return None


def _resolve_date(utterance, base):
    for word, delta in [("大后天",3),("后天",2),("明天",1),("今日",0),("今天",0)]:
        if word in utterance:
            return base + timedelta(days=delta), word
    m = re.search(r"(下|这)?周([一二三四五六日天])", utterance)
    if m:
        prefix, wd = m.group(1), m.group(2)
        target_wd = _WEEKDAY_MAP[wd]
        delta_days = (target_wd - base.weekday()) % 7
        if prefix == "下": delta_days += 7
        elif prefix is None and delta_days == 0: delta_days = 0
        return base + timedelta(days=delta_days), m.group(0)
    return base, ""


def _resolve_time(utterance):
    period = None
    for p in ("早上","上午","中午","下午","傍晚","晚上"):
        if p in utterance: period = p; break
    m = re.search(r"(\d{1,2}):(\d{2})", utterance)
    if m:
        return period, int(m.group(1)), int(m.group(2)), True
    m = re.search(r"(\d{1,2}|[零一二两三四五六七八九十]+)(?:点|:)(\d{1,2}|[零一二两三四五六七八九十]+)?分?(半)?", utterance)
    if m:
        hh = _cn_to_int(m.group(1))
        mm = _cn_to_int(m.group(2)) if m.group(2) else 0
        if m.group(3) == "半": mm = 30
        if hh is None: return period, 0, 0, False
        if period in ("下午","傍晚","晚上") and hh < 12: hh += 12
        if period == "中午" and hh < 6: hh += 12
        if period in ("早上","上午") and hh == 12: hh = 0
        return period, hh, mm, True
    if period: return period, _PERIOD_HOUR[period], 0, False
    return None, 0, 0, False


def parse_time(utterance, base=None):
    base = base or datetime.now()
    day, _ = _resolve_date(utterance, base)
    period, hh, mm, exact = _resolve_time(utterance)
    dt = day.replace(hour=hh, minute=mm, second=0, microsecond=0)
    time_str = f"{hh:02d}:{mm:02d}" if (exact or period) else None
    return ParsedTime(text=utterance, datetime=dt.strftime("%Y-%m-%d %H:%M"), date=dt.strftime("%Y-%m-%d"), time=time_str, period=period, is_time_exact=exact)
