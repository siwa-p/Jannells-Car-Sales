import os
import csv
import pandas as pd
from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from load_db import get_data
from test import test_db
from sqlalchemy.orm import sessionmaker

user = os.getenv('PG_USER')
password = os.getenv('PG_PASSWORD')
host = os.getenv('PG_HOST')
port = os.getenv('PG_PORT')
db = os.getenv('PG_DB')
csv_name = 'data/client_contact_status.csv'
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}',echo=True)

Base = declarative_base()

# define the database model
class Clients(Base):
    __tablename__ = 'clients'
    id = Column('id', String, primary_key=True)
    company = Column('company', String)
    name = Column('name', String)
    address = Column('address', String)
    email = Column('email', String)
    phone = Column('phone', String)
    sales_rep = Column('sales_rep', String)

    def __repr__(self):
        return f"<Clients(id='{self.id}', company='{self.company}', name='{self.name}', address='{self.address}', email='{self.email}', phone='{self.phone}', sales_rep='{self.sales_rep}')>"

class clientcontactstatus(Base):
    __tablename__ = 'client_contact_status'
    id = Column('id', String, primary_key=True)
    name = Column('name', String)
    can_email = Column('can_email', Integer)
    can_call = Column('can_call', Integer)

    def __repr__(self):
        return f"<ClientContactStatus(id='{self.id}', name='{self.name}', can_email={self.can_email}, can_call={self.can_call})>"    


def insert_clients(data):
    try:
        client_items = [Clients(**datum) for datum in data]
        session.add_all(client_items)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")

def insert_csv(data):
    for d in data:
        for key, value in d.items():
            if value == 'null':
                d[key] = None
    try:
        csv_items = [clientcontactstatus(**datum) for datum in data]
        session.add_all(csv_items)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")

def load_api(table_name:str):
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
            insert_clients(data_queried)
            offset += limit

def load_csv(filepath:str):
    data_read = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)
            data_read.append(row)
    insert_csv(data_read)
    return None


if __name__ == '__main__':
    
    # Create tables if they do not exist

    Session = sessionmaker(bind = engine)
    session = Session()
    Base.metadata.create_all(engine)
    load_api('clients')
    load_csv(csv_name)
    session.close()

    # # run sql from stored procs
    # # run table_overview.sql 
    
    # now use this SELECT * FROM client_contact_status_view to convert to csv
    # df = pd.read_sql("SELECT * FROM client_contact_status_view", engine)
    # df.to_csv("data/client_contact_status_view.csv", index=False)
    
    # finally test
    # test_db()