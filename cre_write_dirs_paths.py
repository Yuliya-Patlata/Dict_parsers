import shutil

from pathlib import Path

def cre_write_dirs():
    # basic folder to write
    WRITE_START_of_nested_dirs = Path("/home/dream/PycharmProjects/Dict_parsers/WRITE_FILES/")
    WRITE_START_of_nested_dirs.mkdir(parents=True, exist_ok=True)

    TRANSFORMED_XLSX_dir_path = Path(str(WRITE_START_of_nested_dirs) +'/'+'TRANSFORMED')
    if TRANSFORMED_XLSX_dir_path.exists():
        shutil.rmtree(TRANSFORMED_XLSX_dir_path)
    TRANSFORMED_XLSX_dir_path.mkdir(parents=True, exist_ok=True)

    BY_DEP_BY_METHOD_BY_PRIORITY_XLSX_dir_path = Path(str(TRANSFORMED_XLSX_dir_path) +'/'+'BY_DEP_BY_METHOD_BY_PRIORITY')
    if BY_DEP_BY_METHOD_BY_PRIORITY_XLSX_dir_path.exists():
        shutil.rmtree(BY_DEP_BY_METHOD_BY_PRIORITY_XLSX_dir_path)
    BY_DEP_BY_METHOD_BY_PRIORITY_XLSX_dir_path.mkdir(parents=True, exist_ok=True)

    BY_DEP_BY_WORKER_BY_METHOD_XLSX_dir_path = Path(str(TRANSFORMED_XLSX_dir_path)+ '/'+'BY_DEP_BY_WORKER_BY_METHOD')
    if BY_DEP_BY_WORKER_BY_METHOD_XLSX_dir_path.exists():
        shutil.rmtree(BY_DEP_BY_WORKER_BY_METHOD_XLSX_dir_path)
    BY_DEP_BY_WORKER_BY_METHOD_XLSX_dir_path.mkdir(parents=True, exist_ok=True)

    TOTAL_HARM_BY_WORKER_BY_DEP_XLSX_dir_path = Path(str(TRANSFORMED_XLSX_dir_path)+'/'+'TOTAL_HARM_BY_WORKER_BY_DEP')
    if TOTAL_HARM_BY_WORKER_BY_DEP_XLSX_dir_path.exists():
        shutil.rmtree(TOTAL_HARM_BY_WORKER_BY_DEP_XLSX_dir_path)
    TOTAL_HARM_BY_WORKER_BY_DEP_XLSX_dir_path.mkdir(parents=True, exist_ok=True)

    CONCAT_ALL_DEPS_XLSX_dir_path =Path(str(TRANSFORMED_XLSX_dir_path) +'/'+'CONCAT_ALL_DEPS')
    if CONCAT_ALL_DEPS_XLSX_dir_path.exists():
        shutil.rmtree(CONCAT_ALL_DEPS_XLSX_dir_path)
    CONCAT_ALL_DEPS_XLSX_dir_path.mkdir(parents=True, exist_ok=True)


    return (BY_DEP_BY_METHOD_BY_PRIORITY_XLSX_dir_path,
            BY_DEP_BY_WORKER_BY_METHOD_XLSX_dir_path,
            TOTAL_HARM_BY_WORKER_BY_DEP_XLSX_dir_path,
            CONCAT_ALL_DEPS_XLSX_dir_path)