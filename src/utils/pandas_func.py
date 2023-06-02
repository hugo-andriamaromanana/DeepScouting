import pandas as pd
from os import path

def read_csv(path):
    return pd.read_csv(path, index_col= 'outcome_type')