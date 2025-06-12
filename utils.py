from sqlalchemy import create_engine, insert, Table, MetaData, Column, String, Boolean, Integer
import pandas as pd


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


def json_to_postgres_pandas(data, table_name: str, engine):
    data_df = pd.DataFrame(data)
    data_df.to_sql(name=table_name, con=engine, if_exists='append', index=False)


def json_to_postgres_sqlalchemy(data, table_name:str, engine):
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
    
# the columns are hardcoded, hence the need for two methods
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

