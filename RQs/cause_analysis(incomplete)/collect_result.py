import csv
import pathlib
from numbers_parser import Document


def collect_intocsv(output):
    p = pathlib.Path(
        "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/cause_analysis/numbers_output/")
    numberFiles = p.glob("*.csv")
    records = []
    for file in numberFiles:
        with open(file) as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row[7]) > 0 and row[7] != 'X' and row[7] != "Cause":
                    records.append(row)
    with open(output, "w") as f:
        writer = csv.writer(f)
        writer.writerows(records)


def count_ratio(path):
    C_count = 0
    G_count = 0
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[7] == 'C':
                C_count += 1
            elif row[7] == 'G':
                G_count += 1
    print("C_count", C_count)
    print("G_count", G_count)


if __name__ == "__main__":
    output = "numbers_output/record_selected.csv"
    # collect_intocsv(output)
    count_ratio(output)
