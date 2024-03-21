import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2
import os
import urllib.parse as up
import requests

#creating connection to google sheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/taliarosenkranz/Documents/Developers_Institute/DI_bootcamp_github/Hackathon/iron_volunteering/google_api_key.json', scope)
client = gspread.authorize(creds)

def connection_elephant_db():
#creating connection to db elephant
    up.uses_netloc.append("postgres")
    DATABASE_URL = 'postgres://dpcrpkft:oWD6EIHE9BHR7GzSktVfCw7FXZ1CX6Lr@castor.db.elephantsql.com/dpcrpkft'
    url = up.urlparse(DATABASE_URL)
    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    return conn

#functions are called in insert_data.py file
def pull_data_from_sheets(sheet_name):
    sheet = client.open(sheet_name).sheet1 #name of google sheets created through forms
    #sheet_volunteers = client.open("Volunteers (Responses)").sheet1 #name of google sheets created through forms
    data = sheet.get_all_records()
    print(data)
    return data

def insert_data(table_name, column_table_names, column_sheet_names, data_row, cur):
    #inserting data from sheets to db table
    placeholders = ', '.join(['%s'] * len(column_table_names)) # %s placeholders for sql query values
    column_table_names_str = ', '.join(column_table_names) #transfers from list values to one long string
    insert_query = f'INSERT INTO {table_name} ({column_table_names_str}) VALUES ({placeholders})' #SQL Query

    for item in data_row:
        # Extracting values in the order of column names in sheets saving in tuple variable 
        values = tuple(item[col] for col in column_sheet_names) 
        cur.execute(insert_query, values)



 


