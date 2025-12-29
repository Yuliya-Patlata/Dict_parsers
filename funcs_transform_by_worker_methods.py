import numpy as np
import pandas as pd
from itertools import chain
import shutil
from pathlib import Path
from nice_df_print import print_df_cols

#def agr_lst(pd_col_of_lists):

def by_workers_returns_2_dfs(raw_df):
    modif_raw_df = raw_df.copy()
    modif_raw_df.insert(1,'worker_pib', np.nan)
    workers_pib_lst = (modif_raw_df.columns[4:]).tolist()
    print("workers_pib_lst=>", workers_pib_lst)
    df_by_workers_pib=pd.DataFrame()
    total_harm_by_workers = pd.DataFrame()
    for pib in workers_pib_lst:
        print(pib)
        one_worker_df = modif_raw_df.copy()
        cols_2_drop = [ x for x in workers_pib_lst if x!= pib ]
        print('cols_2_drop=>', cols_2_drop)

        one_worker_df =one_worker_df.drop(columns=cols_2_drop,axis=1)
        one_worker_df = one_worker_df.dropna(subset = pib)

        one_worker_df['worker_pib'] = pib
        one_worker_df.rename(columns={pib:'priority'}, inplace=True)
        one_worker_df = one_worker_df.sort_values(by='priority')
        #print('one_worker_df.columns=>', one_worker_df.columns)


        total_harm_by_one_worker = (one_worker_df.iloc[0][['dep_shortname', 'worker_pib','m_group_longname','harmful_factors']]).to_frame().T
        #print('total_harm_by_one_worker=>', total_harm_by_one_worker)
        total_harm = list(set(chain.from_iterable(one_worker_df['harmful_factors'].dropna())))
        total_methods = (str(set(one_worker_df['m_group_longname']))).join('\n;')
        #total_methods = list(set(chain.from_iterable(one_worker_df['m_group_longname'].dropna())))
        #print('total_harm=>', total_harm)
        print('total_methods =>',total_methods)

        total_harm_by_one_worker.rename(columns={'harmful_factors':'total_harm_set',\
                                                 'm_group_longname': 'total_methods_set'}, inplace=True)

        #total_harm_by_one_worker['total_harm_set'] = (',').join(total_harm)
        total_harm_by_one_worker.iloc[0]['total_harm_set'] = total_harm
        #total_harm_by_one_worker['total_methods_set'] = total_methods
        total_harm_by_one_worker.iloc[0]['total_methods_set'] = total_methods

        total_harm_by_workers = pd.concat([total_harm_by_workers,total_harm_by_one_worker], axis=0 )
        #print('total_harm_by_workers=>\n', total_harm_by_workers)

        df_by_workers_pib = pd.concat([df_by_workers_pib, one_worker_df], axis=0)
        #print('df_by_workers_pib=>\n', df_by_workers_pib)

    return df_by_workers_pib, total_harm_by_workers
'''
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

dep_filename_xlsx = "МАТРИЦЯ_1_Екотоксикологія.xlsx"
folder_xlsx_all_deps = '/home/dream/PycharmProjects/Dict_parsers/READ_FILES/TRANSFORM/'
path_to_1_dep_file = folder_xlsx_all_deps + dep_filename_xlsx

raw_df = pd.read_excel(path_to_1_dep_file,
                       engine='openpyxl',
                       sheet_name=0,
                       header=0,
                       dtype_backend="pyarrow")
#print(raw_df)
col_names_lst = ['dep_shortname', 'harmful_factors', 'm_group_longname']
raw_df = raw_df.rename(columns=dict(zip(raw_df.columns[:3], col_names_lst)))
print(raw_df.columns)
#raw_df.insert(1,'worker_pib', np.nan)
#print(raw_df)
#df_by_worker
#new_matrix = raw_df[['dep_shortname', 'harmful_factors', 'm_group_longname']].copy()
'''
'''
df_by_workers_pib, total_harm_by_workers = by_workers_returns_2_dfs(raw_df)
print('total_harm_by_workers')
print_df_cols(total_harm_by_workers)
print("df_by_workers_pib=>")
print_df_cols(df_by_workers_pib)

'''

'''


#Вигрузка в ексель df_by_workers_pib у папку 'BY_WORKER_BY_METHODS'
START_of_nested_dirs = Path("/home/dream/PycharmProjects/Dict_parsers/WRITE_FILES/")
START_of_nested_dirs.mkdir(parents=True, exist_ok=True)

TRANSFORMED_XLSX_dir_path = START_of_nested_dirs / 'TRANSFORMED' / 'BY_WORKER_BY_METHODS'
if TRANSFORMED_XLSX_dir_path.exists():
    shutil.rmtree(TRANSFORMED_XLSX_dir_path)
TRANSFORMED_XLSX_dir_path.mkdir(parents=True, exist_ok=True)

t_by_worker_method_xlsx = str(TRANSFORMED_XLSX_dir_path) + '/' + dep_filename_xlsx
print('t_by_worker_method_xlsx=>', t_by_worker_method_xlsx)
with pd.ExcelWriter(t_by_worker_method_xlsx, mode='w') as writer:
    df_by_workers_pib.to_excel(
        excel_writer=writer,  # файл, в который будем записывать
        sheet_name='harmful_246',  # название листа, на который писать
        index=True,  # записывать ли индекс таблицы
        startrow=0,  # строка, с которой начать запись в целевом файле
        startcol=0  # столбец, с которого начать запись в целевом файле
    )

#Вигрузка в ексель total_harm_by_workers у папку 'TOTAL_HARM_BY_WORKER'
START_of_nested_dirs = Path("/home/dream/PycharmProjects/Dict_parsers/WRITE_FILES/")
START_of_nested_dirs.mkdir(parents=True, exist_ok=True)

TRANSFORMED_XLSX_dir_path = START_of_nested_dirs / 'TRANSFORMED' / 'TOTAL_HARM_BY_WORKER'
if TRANSFORMED_XLSX_dir_path.exists():
    shutil.rmtree(TRANSFORMED_XLSX_dir_path)
TRANSFORMED_XLSX_dir_path.mkdir(parents=True, exist_ok=True)

tot_harm_by_worker_xlsx = str(TRANSFORMED_XLSX_dir_path) + '/' + dep_filename_xlsx
print('tot_harm_by_worker_xlsx=>', tot_harm_by_worker_xlsx)
with pd.ExcelWriter(tot_harm_by_worker_xlsx, mode='w') as writer:
    total_harm_by_workers.to_excel(
        excel_writer=writer,  # файл, в который будем записывать
        sheet_name='harmful_246',  # название листа, на который писать
        index=False,  # записывать ли индекс таблицы
        startrow=0,  # строка, с которой начать запись в целевом файле
        startcol=0  # столбец, с которого начать запись в целевом файле
    )
'''



