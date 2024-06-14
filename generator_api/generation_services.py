import itertools
import pandas as pd
from io import BytesIO
from datetime import datetime
import time

class FileError(Exception):
    pass

def read_file(content: bytes, filename: str) -> pd.DataFrame:
    if filename.endswith('.csv'):
        try:
            df = pd.read_csv(BytesIO(content))
        except Exception:
            raise FileError('Service cannot read your file')
    elif filename.endswith('.xls') or filename.endswith('.xlsx'):
        try:
            df = pd.read_excel(BytesIO(content))
        except Exception:
            raise FileError('Service cannot read your file')
    else:
        raise FileError('Service doesn\'t support this type of files')
    return df

def generate_combinations(word_lists) -> list[str]:
    all_combinations = []
    for r in range(1, len(word_lists) + 1):
        for combination in itertools.product(*word_lists[:r]):
            all_combinations.append(' '.join(combination))
    return all_combinations

def create_word_array(table: pd.DataFrame) -> list[list[str]]:
    word_list = []
    for column in table.columns.to_list():
        c = table[column].dropna().to_list()
        word_list.append(c)
    return word_list

def write_to_file(combinations: list[str]) -> str:
    filename = f'kernels/kernel_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(filename, 'w') as file:
        for combo in combinations:
            file.write(f'{combo}\n')
    time.sleep(1)
    return filename