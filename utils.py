
 # save to .env and replace existing
def write_to_dotenv(json_data):
    with open('.env', 'r') as file:
        lines = file.readlines()
    with open('.env', 'w') as file:
        for line in lines:
            if not line.strip().startswith('API_TOKEN'):
                file.write(line)
        file.write(f"API_TOKEN={json_data['token']}\n")


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