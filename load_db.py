import requests
import os
import pandas as pd
from utils import write_to_dotenv, check_status_code
from sqlalchemy import create_engine, insert, Table, MetaData, Column, String, Boolean, Integer
from dotenv import load_dotenv
import csv

load_dotenv(override=True)

# get token using user-password dictionary
def get_token():
    root_api = 'https://developyr-api.azurewebsites.net/api/auth'
    username = os.getenv('API_USERNAME')
    password = os.getenv('API_PASSWORD')
    creds = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(root_api, json=creds, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        write_to_dotenv(json_data)
        return "token obtained"
    else:
        return "token not obtained"


def get_data(offset:int=0, limit:int = 10, data_type: str = 'people'):
    keys_dict = {
                'offset' : offset, 
                 'limit' : limit
                 }
    token = os.getenv('API_TOKEN')
    base_URL = 'https://developyr-api.azurewebsites.net/api'
    api = f"{base_URL}/{data_type}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api, headers=headers, params=keys_dict)
    is_response = check_status_code(response)
    if not is_response:
        get_token()    
        load_dotenv(override=True)
        token = os.getenv('API_TOKEN')
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api, headers=headers, params=keys_dict)
    data = response.json()['data']
    return data

# def json_to_postgres(data, table_name: str, engine):
#     data_df = pd.DataFrame(data)
#     data_df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

def json_to_postgres_api(data, table_name:str, engine):
    # data is a list of dictionaries
    metadata = MetaData()
    if metadata.tables:
        table = metadata.tables[table_name]
    else:
        table = Table(
            table_name,
            metadata,
            Column('id', String, primary_key=True),
            Column('company', String),
            Column('name', String),
            Column('address', String),
            Column('email', String),
            Column('phone', String),
            Column('sales_rep', String),
        )
        metadata.create_all(engine) 
    with engine.connect() as connection:
        for d in data:
            stmt = insert(table).values(d)
            connection.execute(stmt)
        connection.commit()
    

def json_to_postgres_csv(data, table_name:str, engine):
    # data is a list of dictionaries
    metadata = MetaData()
    if metadata.tables:
        table = metadata.tables[table_name]
    else:
        table = Table(
            table_name,
            metadata,
            Column('id', String, primary_key=True),
            Column('name', String),
            Column('can_email', Integer),
            Column('can_call', Integer),
        )
        metadata.create_all(engine) 
    with engine.connect() as connection:
        for d in data:
            for key, value in d.items():
                if value == 'null':
                    d[key] = None
            stmt = insert(table).values(d)
            connection.execute(stmt)
        connection.commit()
    

def load_header(sample_data, table_name, engine):
    data_df= pd.DataFrame(sample_data)
    data_df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)  # create table with headers

def load_all(table_name:str, engine):
    is_data = None
    sample_data = get_data(0,5,table_name)
    if sample_data:
        is_data = True
        # load_header(sample_data, table_name, engine)
    offset = 0
    limit = 10
    while is_data:
        data_queried = get_data(offset, limit, table_name)
        if not data_queried:
            is_data = False
        else:
            json_to_postgres_api(data_queried,table_name,engine)
            offset += limit

## using Pandas
# def load_csv(filepath:str, engine):
#     df_iter = pd.read_csv(filepath, iterator=True, chunksize=100)
#     df = next(df_iter)  # first chunk
#     table_name = 'client_contact_status'
#     df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')  # header first
#     df.to_sql(name=table_name, con=engine, if_exists='append')

def load_csv(filepath:str, engine):
    data_read = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)
            data_read.append(row)
    table_name = 'client_contact_status'
    json_to_postgres_csv(data_read, table_name, engine)
    return None
        
# if __name__ == '__main__':
#     load_csv('data/client_contact_status.csv')