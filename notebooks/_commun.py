import pandas as pd
from typing import Literal

def write_df_in_file(df: pd.DataFrame, path:str, format: Literal["csv","parquet"]) -> None:
    """Use to write a dataframe in a file on the disk, to save the data"""
    if format=="csv":
        df.to_csv(path, index=False)
    else:
        df.to_parquet(path, index=False)