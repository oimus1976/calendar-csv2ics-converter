import unittest
from src.csv2ics import to_dt

class TestToDt(unittest.TestCase):
    def test_to_dt_normal_date_and_time(self):
        # normal date and time such as 2025/10/03 + 08:30 → 20251003T083000
        self.assertEqual(to_dt("2025/10/03", "08:30"), "20251003T083000")

    def test_to_dt_date_with_no_time(self):
        # date with no time → YYYYMMDD all-day form
        self.assertEqual(to_dt("2025/10/03", None), "20251003")
        self.assertEqual(to_dt("2025/10/03", ""), "20251003")

    def test_to_dt_missing_or_empty_date(self):
        # missing/empty date → None
        self.assertIsNone(to_dt(None, "08:30"))
        self.assertIsNone(to_dt("", "08:30"))
        self.assertIsNone(to_dt(None, None))
        self.assertIsNone(to_dt("", ""))

if __name__ == '__main__':
    unittest.main()
