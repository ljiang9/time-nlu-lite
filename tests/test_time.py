import sys, unittest
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from time_nlu_lite.parser import parse_time, _cn_to_int

BASE = datetime(2026, 10, 6, 10, 0)

class TestTimeNLU(unittest.TestCase):
    def test_cn_to_int(self):
        self.assertEqual(_cn_to_int("三"), 3)
        self.assertEqual(_cn_to_int("十二"), 12)
        self.assertEqual(_cn_to_int("二十"), 20)
    def test_tomorrow(self): self.assertEqual(parse_time("明天", base=BASE).date, "2026-10-07")
    def test_day_after(self): self.assertEqual(parse_time("后天", base=BASE).date, "2026-10-08")
    def test_next_wednesday(self): self.assertEqual(parse_time("下周三", base=BASE).date, "2026-10-14")
    def test_this_friday(self): self.assertEqual(parse_time("周五", base=BASE).date, "2026-10-09")
    def test_today_morning(self):
        p = parse_time("明天早上", base=BASE)
        self.assertEqual(p.date, "2026-10-07"); self.assertEqual(p.period, "早上")
    def test_afternoon_three(self):
        p = parse_time("下周三下午三点", base=BASE)
        self.assertEqual(p.date, "2026-10-14"); self.assertEqual(p.time, "15:00")
    def test_nine_thirty_half(self): self.assertEqual(parse_time("明天早上九点半", base=BASE).time, "09:30")
    def test_24h_format(self): self.assertEqual(parse_time("明天 14:30", base=BASE).time, "14:30")
    def test_today_evening(self):
        p = parse_time("晚上", base=BASE)
        self.assertEqual(p.date, "2026-10-06"); self.assertIn("19:00", p.datetime)
    def test_is_exact_flag(self):
        self.assertTrue(parse_time("明天下午三点", base=BASE).is_time_exact)
        self.assertFalse(parse_time("明天早上", base=BASE).is_time_exact)
    def test_evening_eight_plus_12(self): self.assertEqual(parse_time("明天晚上八点", base=BASE).time, "20:00")


if __name__ == "__main__": unittest.main()
