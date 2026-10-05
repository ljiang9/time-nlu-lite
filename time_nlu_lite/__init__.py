"""time_nlu_lite: 中文自然语言时间解析。"""
from .parser import parse_time, ParsedTime

__all__ = ["parse_time", "ParsedTime"]
__version__ = "0.1.0"
