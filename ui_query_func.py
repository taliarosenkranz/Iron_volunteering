import pandas as pd
import psycopg2
from authentification_gspread import connection_elephant_db

conn = connection_elephant_db()
cur = conn.cursor()

def qury_table(table_name):
    #query = f'SELECT * FROM {table_name}'
    query = f'SELECT name, num_volunteers as "available spots", address,phone, email, url as Website, description FROM organizations {table_name}'
    return query

def pull_data_from_table(query): #data of all signed up organization to be displayed in UI
    cur.execute(query)
    results = cur.fetchall()

    columns = [desc[0] for desc in cur.description]
    results_df = pd.DataFrame(results, columns=columns)
    
    #cur.close()
    #conn.close()
    
    return results_df
