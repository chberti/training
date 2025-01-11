from csv_importer import csv_parse
from pathlib import Path

current_dir = Path(__file__).parent
file = current_dir.parent / 'uploads' / 'data_1.csv'
print(csv_parse(file))

