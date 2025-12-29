
import numpy as np
import pandas as pd
import re
from chem_corrector import clean_chem_formula
import shutil

from pathlib import Path

from reportlab.lib.pagesizes import letter

#from Examples_gpt.transform_by_gpt import new_matrix
from nice_df_print import print_df_cols

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
def clean_token(s: str) -> str|None:
    if not isinstance(s, str):
        return None
    s = s.replace('\xa0', ' ')
    s = re.sub(r'\s', ' ', s)
    s = s.strip()
    if s == '':
        return None
    return s

def not_nan_cols(row_series, max_reserve):
    modif_row = row_series.to_frame().T
    modif_row = modif_row.dropna(axis=1)
    if modif_row.empty:
        return pd.Series(dtype=object)

    values = modif_row.columns.tolist()
    keys = modif_row.iloc[0].tolist()

    print( keys)
    print(values)
    melted_row = dict(zip(keys,values))
    last_key = max(keys)
    while last_key < max_reserve:
        last_key +=1
        value = np.nan
        melted_row[last_key]=value

    return pd.Series(melted_row).sort_index()

def validate_keys_row(row):
    """
    Повертає список помилок у ключах:
    - дублікат
    - пропуск (дірка в послідовності)
    - некоректний тип
    Порожні рядки дозволені і не дають помилок.
    """
    errors = []

    keys = row.dropna().index.tolist()
    if len(keys) == 0:
        return []  # повністю допустимий порожній рядок

    # дублікати
    if len(keys) != len(set(keys)):
        errors.append("дублікати ключів")

    # пропуски в послідовності
    if keys and (sorted(keys) != list(range(min(keys), max(keys) + 1))):
        errors.append("пропуски в послідовності ключів")

    # типи ключів
    if any(not isinstance(k, (int, np.integer)) for k in keys):
        errors.append("некоректний тип ключа")

    return errors

def print_bad_rows(workers_df):
    """
    Виводить проблемні рядки з описом помилок для користувача.
    Рядки з усіма NaN ключами не вважаються помилковими,
    але інші помилки враховуються.
    """
    bad_rows = workers_df[workers_df["errors"].str.len() > 0]

    if bad_rows.empty:
        print("✔️ Помилок не знайдено – можна продовжувати обробку.")
        return

    print("❌ Знайдено проблемні рядки:\n")
    for idx, row in bad_rows.iterrows():
        excel_row = idx + 2  # +1 для 0-index Python, +1 для header Excel
        row_values = row.drop("errors").to_dict()
        error_types = "; ".join(row["errors"])  # декілька помилок через ;

        print(f"Рядок Excel {excel_row}:")
        print(f"  Значення рядка: {row_values}")
        print(f"  Типи помилок: {error_types}\n")

def transform_by_method_priority(raw_df):
    workers_df = raw_df[raw_df.columns[3:]]
    # print(workers_df)
    # print_bad_rows(workers_df)
    max_reserve = np.max(workers_df)
    print('max_reserve=', max_reserve)
    add_colnames = [f'Виконавець_{i}' for i in range(0, max_reserve + 1)]
    # print('add_colnames=', add_colnames)
    new_matrix = raw_df[['dep_shortname', 'harmful_factors', 'm_group_longname']].copy()
    new_matrix[add_colnames] = np.nan
    print('\n',new_matrix)
    workers_df = workers_df.copy()
    # print(not_nan_cols(workers_df.loc[0],max_reserve))

    new_matrix[new_matrix.columns[3:]] = workers_df.apply(
        not_nan_cols, axis=1, max_reserve=max_reserve)

    print_df_cols(new_matrix)

    return  new_matrix

def try_to_read_xlsx(full_path_to_dep_file_xlsx ):
    try:
        path_to_1_dep_file = str(full_path_to_dep_file_xlsx)
        raw_df = pd.read_excel(path_to_1_dep_file,
                                   engine='openpyxl',
                                   sheet_name=0,
                                   header=0,
                                   dtype_backend="pyarrow")

        col_names_lst = ['dep_shortname', 'harmful_factors', 'm_group_longname']
        raw_df = raw_df.rename(columns=dict(zip(raw_df.columns[:3], col_names_lst)))

        print('before pyarrow transform new_matrix.info()=>')
        raw_df.info()
        raw_df['harmful_factors'] = raw_df['harmful_factors']\
            .apply(lambda x: x.split(','))  # harmful_factors -> string[pyarrow]
        raw_df['harmful_factors'] = raw_df['harmful_factors']\
            .apply(lambda lst:[clean_token(x) for x in lst if clean_token(x) is not None])

        raw_df['harmful_factors'] = raw_df['harmful_factors']\
            .apply(lambda lst:[clean_chem_formula(x) for x in lst])

        raw_df['m_group_longname'] = raw_df['m_group_longname']\
            .apply(lambda x: clean_token(x))

        print('***raw_df=>\n')
        print('after pyarrow transform raw_df.info()=>')
        raw_df.info()

        #print(raw_df.columns)

    except Exception as e:
        print("Помилка читання Excel:", e)
    else:
        return raw_df

#new_matrix = transform_by_method_priority(raw_df)




