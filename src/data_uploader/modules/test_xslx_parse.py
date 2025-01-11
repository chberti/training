from xlsx_importer import xlsx_parse
from pathlib import Path

current_dir = Path(__file__).parent
file = current_dir.parent / 'uploads' / 'data_2.xlsx'
print(xlsx_parse(file))

