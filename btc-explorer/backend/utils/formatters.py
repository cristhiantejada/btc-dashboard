import csv
from io import StringIO

def volume_to_csv(data):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["date", "volume"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    return output.getvalue()
