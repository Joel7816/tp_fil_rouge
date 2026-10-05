import pandas as pd
from typing import Literal
from pathlib import Path

def write_df_in_file(df: pd.DataFrame, path:str, format: Literal["csv","parquet"]) -> None:
    """Use to write a dataframe in a file on the disk, to save the data"""
    p= path.split("/")
    file_name= p[-1]
    pa= Path("/".join(p[:-1])+"/")
    absolute_path= pa.resolve()
    new_folder= Path(absolute_path)
    new_folder.mkdir(parents=True, exist_ok=True)
    if format=="csv":
        df.to_csv(path, index=False)
    elif format == 'parquet':
        df.to_parquet(path, index=False)
    else:
        raise ValueError("Vérifier le format de votre fichier. On créé du CSV ou du PARQUET")
    
    return None