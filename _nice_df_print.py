import pandas as pd
import numpy as np
import textwrap
from tabulate import tabulate
from colorama import Fore, Style

LIME = '\033[93m'   # лимонно-жовтий
RESET = Style.RESET_ALL

def print_df_cols(df, col_widths=None, n=None):
    """
    Друк DataFrame з переносами рядків по заданій ширині колонок
    або з авто-підбором ширини, якщо col_widths не передано.

    Нові можливості:
      • мінімальна ширина = 3
      • автоширина, але не більше за 25
      • лимонно-жовтий колір заголовків
    """

    # 1. Рядки для друку
    df_print = df.head(n).copy() if n is not None else df.copy()

    # 2. Якщо ширини не задані — авто-режим з обмеженням
    if col_widths is None:
        col_widths = {}
        for col in df_print.columns:
            max_len = max(
                [len(str(col))] +
                [len(str(v)) for v in df_print[col]]
            )

            # автоширина з обмеженням
            width = max(3, min(max_len, 25))
            col_widths[col] = width

    # 3. Вибираємо потрібні колонки
    cols = list(col_widths.keys())
    df_wrapped = df_print[cols].copy()

    # 4. Функція переносу значень
    def wrap_value(x, width):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return ""

        if isinstance(x, (list, tuple, np.ndarray, pd.Series)):
            x = ", ".join(str(i) for i in x)

        s = str(x)
        return "\n".join(textwrap.wrap(s, width=width)) if s else ""

    # 5. Переносимо значення в осередках
    for col, width in col_widths.items():
        df_wrapped[col] = df_wrapped[col].apply(lambda x: wrap_value(x, width))

    '''# 6. Формуємо кольорові заголовки з переносами
    wrapped_headers = ["ROW"]
    for col, width in col_widths.items():
        wrapped = "\n".join(textwrap.wrap(col, width=width))

        # лимонно-жовтий + скидання кольору
        wrapped = f"\033[93m{wrapped}\033[0m"

        wrapped_headers.append(wrapped)'''

    '''####BAD Формуємо список назв колонок з переносами та фарбуванням
    wrapped_headers = []
    for col in df.columns:
        width = col_widths[col]
        name = col

        # перенос назви на частини по width символів
        parts = [name[i:i + width] for i in range(0, len(name), width)]

        # фарбуємо КОЖНУ частину
        colored_parts = [f"{LIME}{p:<{width}}{RESET}" for p in parts]

        wrapped_headers.append(colored_parts)

    # визначаємо висоту «блоку» заголовків
    max_lines = max(len(parts) for parts in wrapped_headers)

    # друк заголовків
    for line_idx in range(max_lines):
        row = []
        for parts in wrapped_headers:
            if line_idx < len(parts):
                row.append(parts[line_idx])
            else:
                row.append(" " * len(parts[0]))  # пустий рядок тієї ж ширини
        print(" | ".join(row))'''

    # 7. Додаємо нумерацію рядків
    df_wrapped.insert(0, "ROW", range(df_wrapped.shape[0]))

    # 8. Вивід таблиці
    print(
        tabulate(
            df_wrapped,
            headers=wrapped_headers,
            tablefmt="grid",
            showindex=False
        )
    )


# ---- Приклад використання ----

# 1) Друк ВСІХ колонок з авто-підбором ширини
# print_df_cols(raw_df)

# 2) Друк перших 20 рядків з авто-підбором ширини
# print_df_cols(raw_df, n=20)

# 3) Друк з ручними ширинами
# print_df_cols(raw_df, {
#     'dangerous_factors': 45,
#     'dang_clean': 45,
#     'cap_letters': 20
# })


'''
def print_df_cols(df, col_widths, n=None):
    """
    Друк DataFrame з переносами рядків по заданій ширині колонок
    з красивим табличним форматуванням через tabulate.

    df          : DataFrame
    col_widths  : dict {column_name: width_in_chars}
    n           : число рядків для виводу або None для всього df
    """

    # Беремо перші n рядків
    df_print = df.head(n).copy() if n is not None else df.copy()

    # Лишаємо тільки потрібні колонки
    df_wrapped = df_print[list(col_widths.keys())].copy()

    def wrap_value(x, width):
        """Переносить текст по ширині. Працює для str/list/ndarray/None."""
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return ""

        # списки, Series, numpy arrays → переносимо кожен елемент
        if isinstance(x, (list, tuple, np.ndarray, pd.Series)):
            x = ", ".join(str(i) for i in x)

        s = str(x)
        return "\n".join(textwrap.wrap(s, width=width)) if s else ""

    # обгортання тексту для кожної колонки
    for col, width in col_widths.items():
        df_wrapped[col] = df_wrapped[col].apply(lambda x: wrap_value(x, width))

    # Додаємо нумерацію рядків
    df_wrapped.insert(0, "ROW", range(df_wrapped.shape[0]))

    # Виводимо красиво таблицю
    print(tabulate(df_wrapped, headers=df_wrapped.columns, tablefmt="grid", showindex=False))'''


