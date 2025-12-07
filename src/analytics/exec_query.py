#%%
import argparse
import datetime
from tqdm import tqdm

import pandas as pd
import sqlalchemy
#%%
def import_query(path):
    with open(path) as open_file:
        query = open_file.read()
    return query

def date_range(start, stop, monthly=False):
    # parse once to date objects
    start_dt = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    stop_dt = datetime.datetime.strptime(stop, '%Y-%m-%d').date()
    dates = []
    cur = start_dt
    while cur <= stop_dt:
        dates.append(cur.isoformat())   # return strings like '2025-01-01'
        cur += datetime.timedelta(days=1)

    if monthly:
        return [i for i in dates if i.endswith('01')]
    
    return dates

def exec_query(table, db_origin, db_target, dt_start, dt_stop, monthly=False):
    engine_app = sqlalchemy.create_engine(f'sqlite:///../../data/{db_origin}/database.db')
    engine_analytical = sqlalchemy.create_engine(f'sqlite:///../../data/{db_target}/database.db')

    query = import_query(f'{table}.sql')
    dates = date_range(dt_start, dt_stop, monthly)

    for i in tqdm(dates):
        with engine_analytical.connect() as con:
            try:
                query_delete = f"DELETE FROM {table} WHERE dtRef = date('{i}', '-1 day')"
                con.execute(sqlalchemy.text(query_delete))
                con.commit()
            except Exception as err:
                print(err)

        query_format = query.format(date=i)
        df = pd.read_sql(query_format, engine_app)
        df.to_sql(f'{table}', engine_analytical, index=False, if_exists='append') 

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--table',  type=str)
    parser.add_argument('--db_origin',  choices= ['loyalty-system', 'education-platform', 'analytics'], default='loyalty-system')
    parser.add_argument('--db_target',  choices= ['analytics'], default='analytics')

    now = datetime.datetime.now().strftime('%Y-%m-%d')
    parser.add_argument('--start', type=str, default=now)
    parser.add_argument('--stop', type=str, default=now)
    parser.add_argument('--monthly', action='store_true')

    args = parser.parse_args()

    exec_query(args.table, args.db_origin, args.db_target, args.start, args.stop, args.monthly)

if __name__ == '__main__':
    main()