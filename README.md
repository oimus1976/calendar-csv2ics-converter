# calendar-csv2ics-converter

CSV 形式のスケジュールデータを iCalendar（.ics）形式へ変換する軽量ツールです。  
Google カレンダー、Outlook、Apple カレンダーなど主要カレンダーへインポート可能です。

本ツールは特定サービス（desknet's NEO 等）の名称を含まず、  
一般的な CSV → ICS 変換器として利用できます。

---

## 📌 Features
- 任意の CSV を ICS（iCalendar）形式へ変換
- 開始日・終了日・時刻を解析して VEVENT を生成
- 時刻がない場合は「終日予定」として扱う
- 予定詳細・場所にも対応
- Python だけで動作（外部 API 不要）

---

## 📁 Project Structure

```

src/
└─ csv2ics.py     … メイン変換ロジック
examples/
└─ sample_schedule.csv
output/
└─ （変換結果 .ics が出力される）

```

---

## 🚀 How to Use

### 1. Install dependencies
```

pip install -r requirements.txt

```

### 2. Run converter
```

python src/csv2ics.py examples/sample_schedule.csv

```

`output/converted.ics` が生成されます。

---

## 📝 CSV Format Requirements

最低限必要な列は以下のとおりです：

| CSV 列名 | 役割 |
|---------|------|
| 開始日 | DTSTART |
| 開始時刻 | DTSTART（時間） |
| 終了日 | DTEND |
| 終了時刻 | DTEND（時間） |
| 予定 | SUMMARY |
| 予定詳細 | DESCRIPTION |
| 場所 | LOCATION |

日付形式は `YYYY/MM/DD` としてください。

---

## 🛡️ Notes

- 本ツールは特定商標（desknet's NEO 等）の使用を避けて設計されています。
- CSV のカラム名はローカル用途に応じて調整可能です。
- 公開 OSS としても安全に利用できます。

---
