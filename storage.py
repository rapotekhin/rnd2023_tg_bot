import pandas as pd

from config import TablePath

class RamStorageFactory:
    users_data = {}
    df = pd.read_csv(TablePath)

RamStorage = RamStorageFactory()