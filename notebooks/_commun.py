import pandas as pd
from typing import Literal
from pathlib import Path

def save_dataframe(df: pd.DataFrame, path:str, file_format: Literal["csv","parquet"]) -> None:
    """Use to write a dataframe in a file on the disk, to save the data"""
    if not(file_format in ("csv","parquet")):
        raise ValueError("Error! Check if you use a correct format: csv or parquet ")
    
    absolute_path= Path(path).resolve()
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    if file_format=="csv":
        df.to_csv(absolute_path, index=False)
    elif file_format == 'parquet':
        df.to_parquet(absolute_path, index=False)
    return None
