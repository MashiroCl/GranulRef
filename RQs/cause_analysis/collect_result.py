import csv
import pathlib


def collect_intocsv(output):
    p = pathlib.Path(
        "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/cause_analysis/csv/")
    numberFiles = p.glob("*.csv")
    records = []
    for file in numberFiles:
        with open(file) as f:
            reader = csv.reader(f)
            temp = []
            for row in reader:
                temp.append(row)
            for row in temp[2:]:
                if len(row[7]) > 0:
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
            if row[7][0] == 'C':
                C_count += 1
            elif row[7][0] == 'G':
                G_count += 1
    print("# of Combination type", C_count)
    print("# of Generation type", G_count)


def count_explicit_ratio(path):
    explicit = [0, 0, 0, 0]
    not_explicit = 0
    with open(path,"r") as f:
        reader = csv.reader(f)
        for row in reader:
            if "not" in row[8]:
                not_explicit += 1
            else:
                if "1" in row[8]:
                    explicit[0] += 1
                elif "2" in row[8]:
                    print(row[8])
                    explicit[1] += 1
                elif "3" in row[8]:
                    explicit[2] += 1
                elif "4" in row[8]:
                    explicit[3] += 1
                else:
                    print(row)
    print("Does not explicitly suggest existence of CGR", not_explicit)
    print("Explicitly suggest total", sum(explicit))
    for i in range(4):
        print(f"Type {i+1}", explicit[i])


if __name__ == "__main__":
    output = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/cause_analysis/res/record.csv"
    # collect_intocsv(output)

    # count_ratio(output)
    count_explicit_ratio(output)
