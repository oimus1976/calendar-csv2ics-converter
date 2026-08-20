import unittest
import csv
import os
import tempfile
from pathlib import Path
from src.csv2ics import escape_ical_text, convert_csv_to_ics

class TestCSV2ICS(unittest.TestCase):

    def test_escape_ical_text(self):
        # Ordinary text
        self.assertEqual(escape_ical_text("Hello World"), "Hello World")
        self.assertEqual(escape_ical_text(""), "")
        self.assertEqual(escape_ical_text(None), None)

        # Special characters individually
        self.assertEqual(escape_ical_text("Path\\To\\File"), "Path\\\\To\\\\File")
        self.assertEqual(escape_ical_text("Hello, World"), "Hello\\, World")
        self.assertEqual(escape_ical_text("Item 1; Item 2"), "Item 1\\; Item 2")
        self.assertEqual(escape_ical_text("Line 1\nLine 2"), "Line 1\\nLine 2")
        self.assertEqual(escape_ical_text("Line 1\r\nLine 2"), "Line 1\\nLine 2")
        self.assertEqual(escape_ical_text("Line 1\rLine 2"), "Line 1\\nLine 2")

        # Multiple special characters
        self.assertEqual(
            escape_ical_text("A\\B, C; D\nE"),
            "A\\\\B\\, C\\; D\\nE"
        )
        self.assertEqual(
            escape_ical_text("Meeting: Discuss budget, timelines;\nLocation: C:\\docs"),
            "Meeting: Discuss budget\\, timelines\\;\\nLocation: C:\\\\docs"
        )

    def test_convert_csv_to_ics_escaping(self):
        # Create a temporary CSV file with synthetic test input
        with tempfile.NamedTemporaryFile(mode='w', encoding='cp932', delete=False, newline='') as csvfile:
            csv_path = csvfile.name
            writer = csv.DictWriter(csvfile, fieldnames=["開始日", "開始時刻", "終了日", "終了時刻", "予定", "予定詳細", "場所", "ＩＤ（システムＩＤ：自動発番）"])
            writer.writeheader()
            writer.writerow({
                "開始日": "2025/10/01",
                "開始時刻": "10:00",
                "終了日": "2025/10/01",
                "終了時刻": "11:00",
                "予定": "Meeting: Alice, Bob; Charlie",
                "予定詳細": "Review PRs\nMerge \\ fix",
                "場所": "Room A, Floor 1; HQ",
                "ＩＤ（システムＩＤ：自動発番）": "test_id_1"
            })
            writer.writerow({
                "開始日": "2025/10/02",
                "開始時刻": "14:00",
                "終了日": "2025/10/02",
                "終了時刻": "15:00",
                "予定": "Ordinary Event",
                "予定詳細": "Just a normal description",
                "場所": "Office",
                "ＩＤ（システムＩＤ：自動発番）": "test_id_2"
            })

        # Output ICS path
        ics_path = csv_path + ".ics"

        try:
            # Run the conversion
            convert_csv_to_ics(csv_path, output_ics=ics_path)

            # Read the generated ICS file
            with open(ics_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Assert correct escaping in the output for the first event
            self.assertIn(r"SUMMARY:Meeting: Alice\, Bob\; Charlie - Review PRs\nMerge \\ fix", content)
            self.assertIn(r"DESCRIPTION:Review PRs\nMerge \\ fix", content)
            self.assertIn(r"LOCATION:Room A\, Floor 1\; HQ", content)

            # Assert ordinary values remain correct for the second event
            self.assertIn(r"SUMMARY:Ordinary Event - Just a normal description", content)
            self.assertIn(r"DESCRIPTION:Just a normal description", content)
            self.assertIn(r"LOCATION:Office", content)

        finally:
            # Cleanup
            if os.path.exists(csv_path):
                os.remove(csv_path)
            if os.path.exists(ics_path):
                os.remove(ics_path)

if __name__ == '__main__':
    unittest.main()
