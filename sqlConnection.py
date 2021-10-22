import psycopg2 as pg
import pandas as pd
import json

creds = json.load(open("db_cred.json", 'r'))

def connect_ppg2():    
    try:
        print('Connecting to the PostgreSQL Database...')

        conn = pg.connect(
               database=creds["PG_DB_NAME"],
               user=creds["PG_UN"],
               password= creds["PG_DB_PW"],
               host=creds["DB_HOST"],
               port=creds["PORT"],
            )
    except:
        print('Connection Has Failed...') 
    return conn


def create_df_from_ppg2(query, conn):
    print('Executing SQL Query & Saving To DataFrame...')
    print(query)
    return pd.read_sql_query(query, conn)


conn = connect_ppg2()

q = 'SELECT * FROM Users ORDER BY id ASC'

df = create_df_from_ppg2(q,conn)



print(df['email'])