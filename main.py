import requests
import json
import os
import csv
import sys

# get token using user-password dictionary
def get_token():
    root_api = 'https://developyr-api.azurewebsites.net/api/auth'
    username = 'admin'
    password = 'password123'
    creds = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(root_api, json=creds, headers=headers)

    print(response)
    if response.status_code == 200:
        json_data = response.json()
        print(json_data)
        with open('token.json','w') as f:
            json.dump(json_data,f)
        return json_data
    else:
        return "Unsuccessful"

# authenticate to the api using the token
def get_data(offset, limit, data_type: str):
    keys_dict = {
                'offset' : offset, 
                 'limit' : limit
                 }
    with open('token.json') as f:
        token_dict= json.load(f)
    # token_dict = get_token()
    token = token_dict['token']
    base_URL = 'https://developyr-api.azurewebsites.net/api'
    api = f"{base_URL}/{data_type}"
    headers = {'Authorization': f'Bearer {token}'}
    # print(headers)
    response = requests.get(api, headers=headers, params=keys_dict)
    print(response)
    print(response.url)
    if response.status_code == 200:
        print("success")
        people_data = response.json()['data']
        # print(people_data)
        return people_data
    else:
        return "Unauthorized access"





if __name__ == '__main__':
    # get_token()
    data = get_data(0,10,'clients')
    # print(data)
    header = data[0].keys()
    csv_writer = csv.DictWriter(sys.stdout, fieldnames= header)
    # print(csv_writer)
    csv_writer.writeheader()
    csv_writer.writerows(data)
