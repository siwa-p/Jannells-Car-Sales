import requests
import json
import os
import csv
import sys
import pandas as pd
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
        # save to .env and replace existing
        with open('.env', 'r') as file:
            lines = file.readlines()
        with open('.env', 'w') as file:
            for line in lines:
                if not line.strip().startswith('API_TOKEN'):
                    file.write(line)
            file.write(f"API_TOKEN={json_data['token']}\n")
        return json_data
    else:
        return "Unsuccessful"

# authenticate to the api using the token
def get_data(offset, limit, data_type: str):
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
        load_dotenv()
        token = os.getenv('API_TOKEN')
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api, headers=headers, params=keys_dict)
    
    people_data = response.json()['data']
            # print(people_data)
    
    return people_data


def check_status_code(response):
    status_code = response.status_code
    if status_code == 200:
        return True
    elif status_code == 401:
        print("Token expired.")
        return False
    else:
        print(f"Unauthorized access. Status code: {status_code}")
        return False

def json_to_postgres(data, table_name:str):
    user = os.getenv('PG_USER')
    password = os.getenv('PG_PASSWORD')
    host = os.getenv('PG_HOST')
    port = os.getenv('PG_PORT')
    db = os.getenv('PG_DB')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    data_df = pd.DataFrame(data)

    table_name = table_name
    data_df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')  # header first
    data_df.to_sql(name=table_name, con=engine, if_exists='append')


if __name__ == '__main__':
    # get_token()
    data = get_data(0,10,'people')
    json_to_postgres(data, 'people')
    # print(data)
    # header = data[0].keys()
    # csv_writer = csv.DictWriter(sys.stdout, fieldnames= header)
    # # print(csv_writer)
    # csv_writer.writeheader()
    # csv_writer.writerows(data)
