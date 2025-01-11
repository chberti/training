# csv_importer.py
import sqlalchemy
import pandas as pd
import json
from pathlib import Path

def connect_to_db(user, pwd, host, db):
    connection_uri = f"postgresql://user:pwd@host:5432/db"
    db_engine_dwh = sqlalchemy.create_engine(connection_uri)
    return db_engine_dwh

#db_session = connect_to_db(
#    user = 'postgremaster',
#    pwd = 'JIHYkhjza3UE87345983GVCE',
#    host = 'postgres',
#    db = 'main'
#)

this_dir = Path(__file__).parent

def send_data(df, table, db_session):
    df.to_sql(name = table,
              con = db_session
              )

def csv_parse(file_path):
    with open(this_dir / 'data_schemas.json', 'r') as file:
        data_schemas = json.load(file)
    # Extraction du CSV et nommage des colonnes
    df = pd.read_csv(file_path, delimiter = ';')
    df = df.rename(columns = {'dataFirstNames':'first_names',
                         'dataLastName': 'last_name',
                         'dataEmail': 'email',
                         'dataPhone': 'phone',
                         'dataFax': 'fax',
                         'dataTitle': 'title',
                         'dataJobTitle': 'job_title',
                         'dataPositionType': 'job_type',
                         'dataOrganization': 'org_name',
                         'dataJobStartDate': 'start_date',
                         'dataURI': 'org_vivo_uri'
                         })

    # Extraction des prénoms
    df['first_name'] = df['first_names'].str.split(',', expand=True)[0]
    df['middle_name'] = (df['first_names'].str.split(',', expand=True)[1]).fillna('')

    # Génération de tous les ids
    all_id_df = df
    for schema in data_schemas.keys():
        all_id_df = generate_id(df = all_id_df,
                                columns = data_schemas[schema]['id_columns'],
                                column_name = data_schemas[schema]['column_id_name'])
    # Envoi de chaque DF à la base de données
    db_session = connect_to_db(
       user = 'postgremaster',
       pwd = 'JIHYkhjza3UE87345983GVCE',
       host = 'postgres',
       db = 'main'
    )
    for schema in data_schemas.keys():
        limited_df = extract_data(df = all_id_df, columns = data_schemas[schema]['columns'])
        send_data(
            df = limited_df,
            table = schema,
            db_session = db_session
        )
    nb_lignes = all_id_df.count()
    schema = all_id_df.describe()
    return (nb_lignes, schema)

def generate_id(df, columns, column_name):
    df[column_name] = df[columns].apply(lambda x: '_'.join(str(x)), axis = 1)
    return df

def extract_data(df, columns):
    pruned_df = df[columns]
    return pruned_df

def import_data(df, category, id_column, data_schemas):
    id_columns = data_schemas[category]['id_columns']
    df_with_id = generate_id(df = df, columns = id_columns, column_name = id_column)
    pruned_df = extract_data(df_with_id, data_schemas[category]['columns'])
    return pruned_df