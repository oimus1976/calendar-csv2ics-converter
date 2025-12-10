# calendar-csv2ics-converter

CSV 形式のスケジュールデータを iCalendar（.ics）形式へ変換する軽量ツールです。  
Google カレンダー、Outlook、Apple カレンダーなど主要カレンダーへインポート可能です。

本ツールは特定サービス名（desknet's NEO 等）を含まない汎用仕様で構成されています。

---

## 📌 Features

- 任意の CSV を ICS（iCalendar）形式へ変換
- 開始日・終了日・時刻を解析して VEVENT を生成
- 時刻がない場合は「終日予定」として扱う
- **SUMMARY（表題）は「予定 + 予定詳細」を自動連結して生成（例：`WEB会議 - 説明会（第2回）`）**
- DESCRIPTION は CSV の「予定詳細」をそのまま利用
- 場所（LOCATION）にも対応
- Python のみで動作（外部 API 不要）

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

以下の列を持つ CSV を推奨します：

| CSV 列名 | 役割 |
|---------|------|
| 開始日 | DTSTART |
| 開始時刻 | DTSTART（時間） |
| 終了日 | DTEND |
| 終了時刻 | DTEND（時間） |
| **予定** | SUMMARY（表題）に使用 |
| **予定詳細** | SUMMARY（表題）および DESCRIPTION に使用 |
| 場所 | LOCATION |

---

## 🛡️ Notes

- SUMMARY の生成ルールは以下のとおりです：

```

予定 + " - " + 予定詳細
（どちらかが空の場合は、存在する方のみを使用）

```

- 本ツールは特定商標（desknet's、NEO 等）の使用を避けて設計されています。
- CSV のカラム名はローカル運用に合わせて自由に拡張・変更できます。

---

