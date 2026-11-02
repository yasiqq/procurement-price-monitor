import csv
from pathlib import Path


def read_quotes_from_csv():
    data_dir = Path(__file__).resolve().parent.parent / "data"
    csv_files = data_dir.glob("data*.csv")
    rows = []
    for path in csv_files:
        with open(path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                rows.append(row)


    print(f"Quotes read: {len(rows)}")
    print(rows[0]["<TICKER>"])
    print(rows[-1]["<TICKER>"])


    return rows
