
import requests
import os
import pandas as pd
from utils import write_to_dotenv, check_status_code
from sqlalchemy import create_engine
from dotenv import load_dotenv
from load_db import load_all, load_csv
from test import test_db
from utils import run_sql
if __name__ == '__main__':
    user = os.getenv('PG_USER')
    password = os.getenv('PG_PASSWORD')
    host = os.getenv('PG_HOST')
    port = os.getenv('PG_PORT')
    db = os.getenv('PG_DB')
    csv_name = 'data/client_contact_status.csv'
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # load_all('people', engine)
    # load_all('clients', engine)
    # load_csv(csv_name, engine)
    
    # run sql from postgres engine
    # run creating_tables.sql
    # run inserting_tables.sql
    
    # now use this SELECT * FROM client_contact_status_view to convert to csv
    df = pd.read_sql("SELECT * FROM client_contact_status_view", engine)
    df.to_csv("data/client_contact_status_view.csv", index=False)
    
    # finally test
    test_db()