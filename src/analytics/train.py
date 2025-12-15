# %%
import pandas as pd
import sqlalchemy

con = sqlalchemy.create_engine("sqlite:///../../data/analytics/database.db")

#%%

#SAMPLE - IMPORT DO DADOS
df = pd.read_sql('abt_fiel', con)
df.head()