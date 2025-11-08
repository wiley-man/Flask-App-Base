import csv
from flaskapp import db, Quote

with open("quotes.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    samples = []
    for row in reader:
        quote = Quote(id=row['id'], text=row['text'], author=row['author'])
        samples.append(quote)
        print(f"Prepared Quote({quote})")