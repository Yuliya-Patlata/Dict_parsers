import pandas as pd
import re
import textwrap
import numpy as np
from tabulate import tabulate

'''pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)'''

'''path_2_xlsx = '/home/dream/PycharmProjects/Dict_parsers/READ_FILES/246_new_dang _factors_native_excell.xlsx'
raw_df = pd.read_excel(path_2_xlsx,
                       engine='openpyxl',
                       header=0,
                       dtype_backend="pyarrow")

# Чистка пробілів
raw_df = raw_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)'''


def split_upper_tail(text):
    """
    Розділяє слова і великі літери на кінцях слів регуляркою
    та повертає очищений текст і список великих літер
    """
    if not isinstance(text, str):
        return text, None

    # видаляємо недруковані символи та зайві пробіли
    text_clean = re.sub(r'\s+', ' ', text).strip()

    # шукаємо блоки великих літер (А-ЯҐЄІЇ), розділені комами
    cap_letters = split_upper_tail.pattern.findall(text_clean)

    # видаляємо знайдені великі літери з тексту
    dang_clean = split_upper_tail.pattern.sub('', text_clean).strip()

    # нормалізація ком та пробілів
    dang_clean = re.sub(r'\s*,\s*', ', ', dang_clean)
    dang_clean = re.sub(r'\s+', ' ', dang_clean)

    return dang_clean, cap_letters if cap_letters else None

'''
# регулярка як pattern
split_upper_tail.pattern = re.compile(r'(?<=[а-яґєіїА-ЯҐЄІЇ])([А-ЯҐЄІЇ](?:[, \n]*[А-ЯҐЄІЇ])*)\b')
# застосування до всього DataFrame
raw_df[["dang_clean", "cap_letters"]] = raw_df["dangerous_factors"].apply(
    lambda x: pd.Series(split_upper_tail(x)))'''

# красивий вивід
def show_compare(df, n=10):
    for idx, row in df.head(n).iterrows():
        print(f"ROW {idx}:")
        print("  ORIGINAL:   ", row["dangerous_factors"])
        print("  CLEANED:    ", row["dang_clean"])
        print("  LETTERS:    ", row["cap_letters"])
        print("-" * 80)

#show_compare(raw_df, n=len(raw_df))





