# %%

import datetime
from tqdm import tqdm

import pandas as pd
import sqlalchemy

# %%

def import_query(path):
    with open(path) as open_file:
        query = open_file.read()
    return query

query = import_query('life_cycle.sql')
# print(query.format(date='2025-12-01')) 
# %%

engine_app = sqlalchemy.create_engine('sqlite:///../../data/loyalty-system/database.db')
engine_analytical = sqlalchemy.create_engine('sqlite:///../../data/analytics/database.db')

# %%


def date_range(start, stop):
    # parse once to date objects
    start_dt = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    stop_dt = datetime.datetime.strptime(stop, '%Y-%m-%d').date()
    dates = []
    cur = start_dt
    while cur <= stop_dt:
        dates.append(cur.isoformat())   # return strings like '2025-01-01'
        cur += datetime.timedelta(days=1)
    return dates

dates = date_range('2024-03-01','2025-12-01')

for i in tqdm(dates):
    with engine_analytical.connect() as con:
        try:
            query_delete = f"DELETE FROM life_cycle WHERE dtRef = date('{i}', '-1 day')"
            con.execute(sqlalchemy.text(query_delete))
            con.commit()
        except Exception as err:
            print(err)

    query_format = query.format(date=i)
    df = pd.read_sql(query_format, engine_app)
    df.to_sql('life_cycle', engine_analytical, index=False, if_exists='append') 

# %%
# with engine_analytical.connect() as con:

#     query_delete = f"DELETE FROM life_cycle"
#     print(query_delete)
#     con.execute(sqlalchemy.text(query_delete))
#     con.commit()

# %%
