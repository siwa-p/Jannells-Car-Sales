import requests
import os
import pandas as pd
from utils import write_to_dotenv, check_status_code, json_to_postgres_sqlalchemy, json_to_postgres_csv, json_to_postgres_pandas
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


def load_header(sample_data, table_name, engine):
    data_df= pd.DataFrame(sample_data)
    # To do : Fix data types before loading to sql
    # print(data_df.dtypes)
    data_df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)  # create table with headers
    

def load_all_pandas(table_name:str, engine):
    is_data = None
    sample_data = get_data(0,5,table_name)
    if sample_data:
        is_data = True
        load_header(sample_data, table_name, engine)
    offset = 0
    limit = 10
    while is_data:
        data_queried = get_data(offset, limit, table_name)
        if not data_queried:
            is_data = False
        else:
            json_to_postgres_pandas(data_queried,table_name,engine)
            offset += limit

def load_all_sqlalchemy(table_name:str, engine):
    is_data = None
    sample_data = get_data(0,5,table_name)
    if sample_data:
        is_data = True
    offset = 0
    limit = 10
    while is_data:
        data_queried = get_data(offset, limit, table_name)
        if not data_queried:
            is_data = False
        else:
            json_to_postgres_sqlalchemy(data_queried,table_name,engine)
            offset += limit

# csv using Pandas
def load_csv_pandas(filepath:str, engine):
    df_iter = pd.read_csv(filepath, iterator=True, chunksize=100, index_col = None)
    df = next(df_iter)  # first chunk
    table_name = 'client_contact_status'
    # cast data types
    df['can_call'] = df['can_call'].astype('Int64')
    df['can_email'] = df['can_email'].astype('Int64')
    
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)  # header first
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)


# csv using sqlalchemy
def load_csv_sqlalchemy(filepath:str, engine):
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