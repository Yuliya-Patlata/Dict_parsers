import numpy as np
import pandas as pd
import shutil

from pathlib import Path
from itertools import chain
from cre_write_dirs_paths import cre_write_dirs
from writers_to_excel import write_to_excel_with_given_path
from funcs_transform_by_method_priority import try_to_read_xlsx,transform_by_method_priority
from funcs_transform_by_worker_methods import by_workers_returns_2_dfs
from nice_df_print import print_df_cols

if __name__=='__main__':
    #folder to read
    READ_DIR_xlsx_all_deps = Path('/home/dream/PycharmProjects/Dict_parsers/READ_FILES/TRANSFORM/')

    (w_path_by_dep_met_prior, w_path_by_dep_worker_met,\
     w_path_by_dep_worker_tot_harm, w_path_concat_all_deps) = cre_write_dirs()

    conc_lst_by_dep_met_prior = []
    conc_lst_by_dep_worker_met =[]
    conc_lst_by_dep_worker_tot_harm =[]

    for full_path_to_dep_file_xlsx in READ_DIR_xlsx_all_deps.glob('*.xlsx'):

        raw_df = try_to_read_xlsx(full_path_to_dep_file_xlsx)

        df_by_dep_met_prior = transform_by_method_priority(raw_df)
        write_to_excel_with_given_path(df_by_dep_met_prior,w_path_by_dep_met_prior,sep_or_conc='sep')
        conc_lst_by_dep_met_prior.append(df_by_dep_met_prior)

        (df_by_dep_worker_met, df_by_dep_worker_tot_harm) = by_workers_returns_2_dfs(raw_df)

        write_to_excel_with_given_path(df_by_dep_worker_met,w_path_by_dep_worker_met, sep_or_conc='sep')
        conc_lst_by_dep_worker_met.append(df_by_dep_worker_met)

        write_to_excel_with_given_path(df_by_dep_worker_tot_harm,w_path_by_dep_worker_tot_harm,sep_or_conc='sep')
        conc_lst_by_dep_worker_tot_harm.append(df_by_dep_worker_tot_harm)


    conc_df_by_dep_met_prior = pd.concat(conc_lst_by_dep_met_prior,ignore_index=False)
    write_to_excel_with_given_path(conc_df_by_dep_met_prior,w_path_concat_all_deps,\
                                   sep_or_conc='conc_df_by_dep_met_prior' )

    dist_methods_by_dep_with_harm = conc_df_by_dep_met_prior[['dep_shortname', 'harmful_factors', 'm_group_longname']]\
        .drop_duplicates(subset=['dep_shortname', 'm_group_longname']).reset_index(drop=True)
    write_to_excel_with_given_path(dist_methods_by_dep_with_harm, w_path_concat_all_deps, \
                                   sep_or_conc='conc_dist_methods_by_dep_with_harm')

    lst_dist_total_harm = list(set(chain.from_iterable(dist_methods_by_dep_with_harm['harmful_factors'].dropna())))
    print('dist_total_harm=>\n', lst_dist_total_harm)
    conc_df_dist_total_harm = pd.DataFrame({'dist_harm':lst_dist_total_harm})
    write_to_excel_with_given_path(conc_df_dist_total_harm,w_path_concat_all_deps, \
                                   sep_or_conc='conc_df_dist_total_harm')

    conc_df_by_dep_worker_met = pd.concat(conc_lst_by_dep_worker_met,ignore_index=False)
    write_to_excel_with_given_path(conc_df_by_dep_worker_met, w_path_concat_all_deps,\
                                   sep_or_conc='conc_df_by_dep_worker_met')

    conc_df_by_dep_worker_tot_harm = pd.concat(conc_lst_by_dep_worker_tot_harm, ignore_index=False)
    write_to_excel_with_given_path(conc_df_by_dep_worker_tot_harm,w_path_concat_all_deps,\
                                   sep_or_conc='conc_df_by_dep_worker_tot_harm')



    print("conc_df_by_dep_met_prior=>")
    print_df_cols(conc_df_by_dep_met_prior)

'''
        # Вигрузка в ексель
        START_of_nested_dirs = Path("/home/dream/PycharmProjects/Dict_parsers/WRITE_FILES/")
        START_of_nested_dirs.mkdir(parents=True, exist_ok=True)

        
        #######

        #######
        t_by_method_priority_xlsx = str(TRANSFORMED_XLSX_dir_path) + '/' + dep_filename_xlsx
        print('t_by_method_priority_xlsx=>', t_by_method_priority_xlsx)
        with pd.ExcelWriter(t_by_method_priority_xlsx, mode='w') as writer:
            new_matrix.to_excel(
                excel_writer=writer,  # файл, в который будем записывать
                sheet_name='t_by_method_priority',  # название листа, на который писать
                index=True,  # записывать ли индекс таблицы
                startrow=0,  # строка, с которой начать запись в целевом файле
                startcol=0  # столбец, с которого начать запись в целевом файле
            )'''




