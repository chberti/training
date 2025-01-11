# csv_importer.py
import sqlalchemy
import pandas as pd
import json
from pathlib import Path

# Variables globales
this_dir = Path(__file__).parent

# Interactions avec la Base de données
def connect_to_db(user, pwd, host, db):
    connection_uri = f"postgresql://{user}:{pwd}@{host}:5432/{db}"
    db_engine_dwh = sqlalchemy.create_engine(connection_uri)
    return db_engine_dwh

def load_data(table):
    db_session = connect_to_db(
        user='postgremaster',
        pwd='JIHYkhjza3UE87345983GVCE',
        host='postgres',
        db='main'
    )
    df = pd.read_sql(
              sql = f"SELECT * FROM {table}",
              con = db_session
              )
    return df