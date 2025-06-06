import requests
import json
import os
import csv
import sys
import pandas as pd
from utils import write_to_dotenv, check_status_code
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv(override=True)

# get token using user-password dictionary
def get_token():
    root_api = 'https://developyr-api.azurewebsites.net/api/auth'
    username = os.getenv('API_USERNAME')
    password = os.getenv('API_PASSWORD')
    creds = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(root_api, json=creds, headers=headers)

    print(response)
    if response.status_code == 200:
        json_data = response.json()
        write_to_dotenv(json_data)
        return "token obtained"
    else:
        return "token not obtained"


def get_data(offset, limit, data_type: str = 'people'):
    keys_dict = {
                'offset' : offset, 
                 'limit' : limit
                 }
    token = os.getenv('API_TOKEN')
    base_URL = 'https://developyr-api.azurewebsites.net/api'
    api = f"{base_URL}/{data_type}"
    headers = {'Authorization': f'Bearer {token}'}
    # print(headers)
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



def json_to_postgres(data, table_name: str, engine):
    data_df = pd.DataFrame(data)
    data_df.to_sql(name=table_name, con=engine, if_exists='append', index=False)


def load_header(sample_data, table_name, engine):
    data_df= pd.DataFrame(sample_data)
    data_df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)  # create table with headers

def load_all(table_name:str, engine):
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
            json_to_postgres(data_queried,table_name,engine)
            offset += limit



if __name__ == '__main__':
    user = os.getenv('PG_USER')
    password = os.getenv('PG_PASSWORD')
    host = os.getenv('PG_HOST')
    port = os.getenv('PG_PORT')
    db = os.getenv('PG_DB')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # load_all('people', engine)
    # load_all('clients', engine)
