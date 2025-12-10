import csv
import sys
from datetime import datetime
from pathlib import Path


def to_dt(date_str, time_str):
    """'2025/10/03', '08:30' → '20251003T083000'"""
    if not date_str or date_str != date_str:
        return None

    # 時刻なし → 終日予定
    if not time_str or time_str != time_str:
        d = datetime.strptime(date_str, "%Y/%m/%d")
        return d.strftime("%Y%m%d")

    dt = datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M")
    return dt.strftime("%Y%m%dT%H%M%S")


def convert_csv_to_ics(input_csv, output_ics="output/converted.ics"):
    events = []

    with open(input_csv, encoding="cp932") as f:
        reader = csv.DictReader(f)

        for row in reader:
            start = to_dt(row.get("開始日"), row.get("開始時刻"))
            end = to_dt(row.get("終了日"), row.get("終了時刻"))
            summary_raw = row.get("予定", "") or ""
            detail_raw = row.get("予定詳細", "") or ""
            location = row.get("場所", "") or ""
            uid = row.get("ＩＤ（システムＩＤ：自動発番）", "") or ""

            if not start:
                continue

            # ----------------------------
            # SUMMARY ロジック（A案）
            # 予定 + " - " + 予定詳細
            # ----------------------------
            if summary_raw and detail_raw:
                summary = f"{summary_raw} - {detail_raw}"
            else:
                summary = summary_raw or detail_raw

            # DESCRIPTION は詳細をそのまま
            description = detail_raw

            allday = "T" not in start

            evt = ["BEGIN:VEVENT"]
            evt.append(f"UID:{uid}@csv2ics")

            if allday:
                evt.append(f"DTSTART;VALUE=DATE:{start}")
                if end:
                    evt.append(f"DTEND;VALUE=DATE:{end}")
            else:
                evt.append(f"DTSTART:{start}")
                if end:
                    evt.append(f"DTEND:{end}")

            evt.append(f"SUMMARY:{summary}")
            evt.append(f"DESCRIPTION:{description}")
            evt.append(f"LOCATION:{location}")
            evt.append("END:VEVENT")

            events.append("\n".join(evt))

    final = "BEGIN:VCALENDAR\nVERSION:2.0\n" + "\n".join(events) + "\nEND:VCALENDAR\n"

    Path(output_ics).parent.mkdir(parents=True, exist_ok=True)
    Path(output_ics).write_text(final, encoding="utf-8")

    print(f"ICS generated → {output_ics}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv2ics.py <input_csv>")
        sys.exit(1)

    convert_csv_to_ics(sys.argv[1])
