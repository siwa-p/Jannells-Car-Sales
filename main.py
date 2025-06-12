import os
import pandas as pd
from sqlalchemy import create_engine
from load_db import load_all_pandas, load_all_sqlalchemy, load_csv_pandas, load_csv_sqlalchemy
from test import test_db

if __name__ == '__main__':
    user = os.getenv('PG_USER')
    password = os.getenv('PG_PASSWORD')
    host = os.getenv('PG_HOST')
    port = os.getenv('PG_PORT')
    db = os.getenv('PG_DB')
    csv_name = 'data/client_contact_status.csv'
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # load_all_pandas('people', engine)
    # load_all_pandas('clients', engine)
    # load_csv_pandas(csv_name, engine)
    
    # load_all_sqlalchemy('people', engine)
    load_all_sqlalchemy('clients', engine)
    load_csv_sqlalchemy(csv_name, engine)    
    
    # # run sql from stored procs
    # # run table_overview.sql 
    
    # # now use this SELECT * FROM client_contact_status_view to convert to csv
    # df = pd.read_sql("SELECT * FROM client_contact_status_view", engine)
    # df.to_csv("data/client_contact_status_view.csv", index=False)
    
    # # finally test
    # test_db()