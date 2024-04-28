import pandas as pd
import numpy as np
import os

list_tables_names = os.listdir("Planilhas")

list_tables = [pd.read_excel(io=f"Planilhas/{table_name}") for table_name in list_tables_names]

final_table = pd.concat(list_tables)

final_table = final_table.replace(np.nan, "None")

final_table.to_excel("Planilha_final.xlsx", index=False)