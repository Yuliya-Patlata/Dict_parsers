import pandas as pd


def write_to_excel_with_given_path(df,path,sep_or_conc):
    if sep_or_conc == 'sep':
        file_name = df.iloc[0]['dep_shortname']
        path_xlsx = str(path) + '/' + file_name +".xlsx"
    else:
        file_name = sep_or_conc
        path_xlsx = str(path) + '/' + file_name +".xlsx"

    print('path_xlsx', path_xlsx)
    with pd.ExcelWriter(path_xlsx, mode='w') as writer:
        df.to_excel(
            excel_writer=writer,  # файл, в который будем записывать
            sheet_name= file_name,  # название листа, на который писать
            index=True,  # записывать ли индекс таблицы
            startrow=0,  # строка, с которой начать запись в целевом файле
            startcol=0  # столбец, с которого начать запись в целевом файле
        )
    return
