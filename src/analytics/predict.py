# %%
import pandas as pd

import sqlalchemy

con = sqlalchemy.create_engine("sqlite:///../../data/analytics/database.db")

model = pd.read_pickle('model_fiel.pkl')

#%%

data = pd.read_sql('SELECT * FROM abt_fiel', con)

predict = model['model'].predict_proba(data[model['features']])[:,1]

data['predict'] = predict

data
# %%
