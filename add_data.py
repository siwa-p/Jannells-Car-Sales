import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

def main():
    csv_name = 'sample.csv'
    user = os.getenv('PG_USER')
    password = os.getenv('PG_PASSWORD')
    host = os.getenv('PG_HOST')
    port = os.getenv('PG_PORT')
    db = os.getenv('PG_DB')
    table_name = os.getenv('PG_TABLE')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=1000)
    df = next(df_iter)  # skips header

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')  # header first
    df.to_sql(name=table_name, con=engine, if_exists='append')

if __name__ == "__main__":
    main()