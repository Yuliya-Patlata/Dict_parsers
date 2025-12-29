import pandas as pd
import numpy as np
import textwrap
from tabulate import tabulate

# кольори для термінала (лимонно-жовтий + скидання)
LIME = '\033[93m'
RESET = '\033[0m'



def print_df_cols(df: pd.DataFrame, col_widths: dict | None = None, n: int | None = None):
    """
    Друк DataFrame з переносами рядків і кольоровими заголовками.
    Припускає, що колонка row_no вже є у DataFrame на позиції 0.

    Параметри:
    - df : pd.DataFrame
    - col_widths : dict або None
        Якщо dict: {col_name: width_in_chars, ...}. Якщо None — авто-підбір.
    - n : int або None
        Кількість рядків для виводу (подібно до head). Якщо None — всі рядки.
    """

    # --- 1) Вибір фрейму для друку (перші n рядків якщо вказано) ---
    df_print = df.head(n).copy() if n is not None else df.copy()

    # --- 2) Автопідбір ширини, якщо не передано ---
    if col_widths is None:
        col_widths = {}
        for col in df_print.columns:
            # максимальна довжина текстового представлення в колонці
            try:
                max_val_len = df_print[col].astype(str).map(len).max()
            except Exception:
                max_val_len = max(len(str(v)) for v in df_print[col])
            max_len = max(len(str(col)), int(max_val_len or 0))
            width = max(3, min(max_len, 25))
            col_widths[col] = width

    # --- 3) Вибір колонок для друку (ті, що відсутні, ігноруємо) ---
    cols_present = [c for c in col_widths if c in df_print.columns]
    df_wrapped = df_print[cols_present].copy()

    # --- 4) Функція wrap для значень ---
    def wrap_value(x, width):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return ""
        if isinstance(x, (list, tuple, np.ndarray, pd.Series)):
            x = ", ".join(str(i) for i in x)
        s = str(x)
        wrapped_lines = textwrap.wrap(s, width=width) or [""]
        return "\n".join(wrapped_lines)

    # --- 5) Переносимо значення у клітинках ---
    for col in cols_present:
        width = col_widths[col]
        df_wrapped[col] = df_wrapped[col].apply(lambda x: wrap_value(x, width))

    # --- 6) Формуємо заголовки з переносом і фарбуванням кожної частини ---
    wrapped_headers = []
    for col in cols_present:
        width = col_widths[col]
        name = str(col)
        parts = [name[i:i + width] for i in range(0, len(name), width)] or [""]
        colored_parts = [f"{LIME}{p.ljust(width)}{RESET}" for p in parts]
        header_str = "\n".join(colored_parts)
        wrapped_headers.append(header_str)

    # --- 7) Друк через tabulate ---
    print(tabulate(df_wrapped, headers=wrapped_headers, tablefmt="grid", showindex=False))
