import numpy as np
import pandas as pd
import shutil

import re
from pathlib import Path
from transliteration_ua import transliterate_ua
from nice_df_print import print_df_cols
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import re

def en_folder_surname_with_2_init(name: str) -> str:
    # 1. Прибираємо апострофи
    name = re.sub(r"[’'`]", "", name)

    # 2. Замінюємо крапки на підкреслення (індексація типу Є.Д.)
    name = re.sub(r"\.", "_", name)

    # 3. Пробіли → _
    name = re.sub(r"\s+", "_", name)

    # 4. Прибираємо будь-які заборонені символи для шляхів
    name = re.sub(r"[^0-9A-Za-zА-Яа-яІіЇїЄєҐґ_\\-]", "", name)

    # 5. Уникнення подвійних підкреслень
    name = re.sub(r"_+", "_", name)

    # 6. Прибираємо підкреслення з початку та кінця
    name = name.strip("_")
    name  = transliterate_ua(name)
    return name.upper()

def surname_with_2_init(worker_fullname):
    surname, name, fathername   = worker_fullname.split(' ')
    return f'{surname} {name[0:1]}.{fathername[0:1]}.'

df_workers = pd.read_excel(
    "/home/dream/PycharmProjects/Dict_parsers/READ_FILES/TRANSFORM/workers_src.xlsx",
    dtype=str  # optional, if you want everything as strings
)

df_workers = df_workers.applymap(lambda x: x.strip() if isinstance(x,str) else x)
# чистимо колонку sublevel_no від \n у кінці
df_workers['pk_id_worker_full_name'] = (
    df_workers['pk_id_worker_full_name']
    .astype(str)       # на випадок NaN або чисел
    .str.strip()       # прибираємо зайві пробіли
    .str.rstrip('\n')   # видаляємо всі крапки з кінця рядка
)

df_workers.insert(1,'Surname_N_F', np.nan)
df_workers.insert(1,'en_folder_SURNAME_N_F', np.nan)
df_workers.insert(1,'N_Surname', np.nan)

#print(df_workers['pk_id_worker_full_name'])
df_workers['Surname_N_F'] = df_workers['pk_id_worker_full_name'].apply(surname_with_2_init)
df_workers['en_folder_SURNAME_N_F'] = df_workers['Surname_N_F'].apply(en_folder_surname_with_2_init)
df_workers['N_Surname'] = df_workers['Surname_N_F'].apply(lambda s: f'{s[-4:-2]} {s.split(" ")[0]}')
print_df_cols(df_workers)
#print(df_workers.head())

START_of_nested_dirs = Path("/home/dream/PycharmProjects/Dict_parsers/WRITE_FILES/")
START_of_nested_dirs.mkdir(exist_ok=True)
for folder_name in df_workers['en_folder_SURNAME_N_F']:
    folder_path = START_of_nested_dirs /'WORKERS_FOLDERS'/folder_name
    if folder_path.exists():
        shutil.rmtree(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)

    subfolders = ['MED_OGLADY','ZAYAVY', 'PASSPORT', 'DIPLOMAS', 'IPN', 'OSOB_KARTKA','JOBS_BOOK','OTHER']
    for subfolder_name in subfolders:
        subfolder_path = folder_path / subfolder_name
        if subfolder_path.exists():
            shutil.rmtree(subfolder_path)
        subfolder_path.mkdir(parents=True,exist_ok=True)
        if subfolder_name == 'MED_OGLADY':
            year_folder_path = subfolder_path / '2026'
            if year_folder_path.exists():
                shutil.rmtree(year_folder_path)
            year_folder_path.mkdir(parents=True, exist_ok=True)

WORKERS_DATA_XLSX_dir_path = START_of_nested_dirs/'WORKERS_DATA'/'XLSX'
if WORKERS_DATA_XLSX_dir_path.exists():
    shutil.rmtree(WORKERS_DATA_XLSX_dir_path)
WORKERS_DATA_XLSX_dir_path.mkdir(parents=True,exist_ok=True)
path_workers_xlsx = str(WORKERS_DATA_XLSX_dir_path) + '/workers.xlsx'
print('path_workers_xlsx=>', path_workers_xlsx)
with pd.ExcelWriter(path_workers_xlsx, mode='w') as writer:
    df_workers.to_excel(
        excel_writer=writer,  # файл, в который будем записывать
        sheet_name='workers',  # название листа, на который писать
        index=True,  # записывать ли индекс таблицы
        startrow=0,  # строка, с которой начать запись в целевом файле
        startcol=0  # столбец, с которого начать запись в целевом файле
    )




