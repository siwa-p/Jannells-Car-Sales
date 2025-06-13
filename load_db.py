import requests
import os
from utils import write_to_dotenv, check_status_code
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