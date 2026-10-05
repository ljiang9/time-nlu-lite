"""命令行：python -m time_nlu_lite "下周三下午三点"。"""
from __future__ import annotations
import argparse, json, sys
from datetime import datetime
from .parser import parse_time


def main(argv=None):
    ap = argparse.ArgumentParser(prog="time-nlu", description="中文时间解析")
    ap.add_argument("utterance")
    ap.add_argument("--base", help="基准时间 YYYY-MM-DD HH:MM")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    base = datetime.strptime(args.base, "%Y-%m-%d %H:%M") if args.base else None
    p = parse_time(args.utterance, base=base)
    if args.json:
        print(json.dumps({"text": p.text, "datetime": p.datetime, "date": p.date, "time": p.time, "period": p.period, "is_time_exact": p.is_time_exact}, ensure_ascii=False, indent=2))
    else:
        print(f"原文: {p.text}")
        print(f"日期: {p.date}")
        print(f"时间: {p.time or '（未指定具体时分）'}")
        if p.period: print(f"时段: {p.period}")
        print(f"解析结果: {p.datetime}")
    return 0


if __name__ == "__main__": raise SystemExit(main())
