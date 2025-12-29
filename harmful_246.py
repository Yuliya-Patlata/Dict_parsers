from pydoc import replace

import numpy as np
import pandas as pd
import shutil
import re
import psycopg
from sqlalchemy import create_engine, text

from pathlib import Path
from split_by_reg_exp import split_upper_tail, show_compare
from nice_df_print import print_df_cols
#from virt_levels import cre_virt_level

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def cre_virt_level(sublevel_no,sublevels_quantity, max_sublevels_depth ):
    virt_level = sublevel_no
    #print('type(sublevels_quantity)=>', type(sublevels_quantity))
    #print(max_sublevels_depth)
    num_of_added_zeros = max_sublevels_depth - sublevels_quantity

    for l in range(0, num_of_added_zeros ):
        virt_level = virt_level + '.0'
        #pass
    return virt_level

path_2_chem_xlsx = '/home/dream/PycharmProjects/Dict_parsers/READ_FILES/CHEM_FACTORS/246_factors.xlsx'
raw_df = pd.read_excel(path_2_chem_xlsx,
                   engine='openpyxl',
                   header = 0,
                   dtype_backend="pyarrow")
# Чистка пробілів
raw_df = raw_df.applymap(lambda x: x.strip() if isinstance(x,str) else x)
#print('raw_df=>\n', raw_df)
raw_df.insert(0, "row_no", range(1, len(raw_df)+1))
# чистимо колонку sublevel_no від крапок у кінці
raw_df['sublevel_no'] = (
    raw_df['sublevel_no']
    .astype(str)       # на випадок NaN або чисел
    .str.strip()       # прибираємо зайві пробіли
    .str.rstrip('.')   # видаляємо всі крапки з кінця рядка
)

# регулярка як pattern
split_upper_tail.pattern = re.compile(r'(?<=[а-яґєіїА-ЯҐЄІЇ])([А-ЯҐЄІЇ](?:[, \n]*[А-ЯҐЄІЇ])*)\b')
# застосування до всього DataFrame
raw_df[["dang_clean", "cap_letters"]] = raw_df["dangerous_factors"].apply(
    lambda x: pd.Series(split_upper_tail(x)))
show_compare(raw_df, n= 10)# n= len(raw_df)

raw_df.insert(2,'sublevels_quantity',raw_df['sublevel_no'].astype(str) \
    .str.split('.') \
    .map(len) )
raw_df['sublevels_quantity'].astype(int)
print('raw_df.sublevels_quantity.dtype=>',raw_df.sublevels_quantity.dtype)

max_sublevels_depth=raw_df['sublevels_quantity'].max()
#print('max_sublevels_depth=>', max_sublevels_depth)

raw_df.insert(
    3,  # позиція колонки
    'virtual_level',
    raw_df.apply(lambda row: cre_virt_level( \
        row['sublevel_no'],row['sublevels_quantity'], max_sublevels_depth),axis=1)

)

sub_cols = [ f'L{i}'for i in range(1,max_sublevels_depth+1)]
print('sub_cols=>', sub_cols)
for pos_no in range (0,max_sublevels_depth,1):
    print('pos_no=>', pos_no)
    col_name = sub_cols[pos_no]
    print('col_name=>', col_name)
    raw_df.insert(pos_no, col_name, np.nan)

test = raw_df['virtual_level'].iloc[0].split('.')
print('test=>', test)

raw_df[sub_cols]=raw_df['virtual_level'].apply(
    lambda row: pd.Series(dict(zip(sub_cols,row.split('.'))))
)
raw_df.insert(6,'sub_no',raw_df['sublevel_no'].astype(str).map(lambda s: s.replace('.','_')))
print_df_cols(raw_df, n=3)
#Вигрузка в postgres
engine = create_engine('postgresql+psycopg://lucid:1@localhost:5432/ula_real')
raw_df.to_sql(name='harmful_246', con=engine, index=False,if_exists='replace')

#Вигрузка в ексель
START_of_nested_dirs = Path("/home/dream/PycharmProjects/Dict_parsers/WRITE_FILES/")
START_of_nested_dirs.mkdir(parents=True, exist_ok=True)

HARMFUL_CHEM_XLSX_dir_path = START_of_nested_dirs /'HARMFUL_CHEM'/'XLSX'
if HARMFUL_CHEM_XLSX_dir_path.exists():
    shutil.rmtree(HARMFUL_CHEM_XLSX_dir_path)
HARMFUL_CHEM_XLSX_dir_path.mkdir(parents=True, exist_ok=True)
#######

#######
path_harmful_246_xlsx = str(HARMFUL_CHEM_XLSX_dir_path) + '/Harmful_246.xlsx'
print('path_harmful_246_xlsx=>', path_harmful_246_xlsx)
with pd.ExcelWriter(path_harmful_246_xlsx, mode='w') as writer:
    raw_df.to_excel(
        excel_writer=writer,  # файл, в который будем записывать
        sheet_name='harmful_246',  # название листа, на который писать
        index=True,  # записывать ли индекс таблицы
        startrow=0,  # строка, с которой начать запись в целевом файле
        startcol=0  # столбец, с которого начать запись в целевом файле
    )



'''
print_df_cols(raw_df, {
    'row_no':7,
    'sublevel_no':11,
    'sublevels_quantity':7,
    'virtual_level':11,
    'periodicity':11,
    'dangerous_factors': 20,
    'dang_clean': 20,
    'cap_letters': 11,
    'doctors':10,
    'med_investigations':11,
    'contradictions':15
}, n=2)#'''


#print("type(raw_df['sublevel_no')=>", type(raw_df['sublevel_no']))
#print_df_cols(raw_df, n=10)

#print(raw_df.info())





