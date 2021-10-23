import psycopg2 as pg
import pandas as pd
import json

def connect_ppg2():    
    
    creds = json.load(open("db_cred.json", 'r'))
    try:
        print('Connecting to the PostgreSQL Database...\n')

        conn = pg.connect(
               database=creds["PG_DB_NAME"],
               user=creds["PG_UN"],
               password= creds["PG_DB_PW"],
               host=creds["DB_HOST"],
               port=creds["PORT"],
            )
    except:
        print('Connection Has Failed...\n') 
    return conn


def create_df_from_ppg2(query, conn):
    # print('Executing SQL Query & Saving To DataFrame...')
    return pd.read_sql_query(query, conn)
