import pandas as pd
from typing import Literal
from pathlib import Path

def save_dataframe(df: pd.DataFrame, path:str, file_format: Literal["csv","parquet"]) -> None:
    """Use to write a dataframe in a file on the disk, to save the data"""
    if not(file_format in ("csv","parquet")):
        raise ValueError("Error! Check if you use a correct format: csv or parquet ")
    else:
        #we want to use slash as sepator. If there are back-slash, we replace them with slash
        sep= "/"
        p= path.split(sep)
        file_name= p[-1]
        pa= Path(p.join(p[:-1])+ sep)
        #create an asbolute path if it is not one
        absolute_path= pa.resolve()
        new_folder= Path(absolute_path)
        new_folder.parent.mkdir(parents=True, exist_ok=True)
        if file_format=="csv":
            df.to_csv(path, index=False)
        elif file_format == 'parquet':
            df.to_parquet(path, index=False)
    return None