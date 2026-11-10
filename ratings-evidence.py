"""Print historical ratings with their source links for analyst review."""
import csv
from pathlib import Path

def main():
    path = Path(__file__).parent / "public-data/historical-ratings.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            print(f"{row['Company']} | {row['Platform']} | {row['Overall rating']} / 5 | {row['Reviews']} reviews | {row['Source page']}")

if __name__ == "__main__":
    main()
