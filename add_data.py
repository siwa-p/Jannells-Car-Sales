import os
import pandas as pd
from sqlalchemy import create_engine

# params should have all the variables
def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    csv_name = 'output.csv'

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=10000)

    df = next(df_iter) # skips header

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace') # header first

    df.to_sql(name=table_name, con=engine, if_exists='append')
