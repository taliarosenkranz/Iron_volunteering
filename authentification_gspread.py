import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2
import os
import urllib.parse as up
import requests


# Use creds to create a client to interact with the Google Drive API

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/taliarosenkranz/Documents/Developers_Institute/DI_bootcamp_github/Hackathon/iron_volunteering/google_api_key.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Volunteers (Responses)").sheet1
data = sheet.get_all_records()


print(data)
print('##################')



up.uses_netloc.append("postgres")
DATABASE_URL = 'postgres://dpcrpkft:oWD6EIHE9BHR7GzSktVfCw7FXZ1CX6Lr@castor.db.elephantsql.com/dpcrpkft'
url = up.urlparse(DATABASE_URL)
conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)
cur = conn.cursor()

# Assuming your table schema and form align perfectly
# Adapt the INSERT statement according to your table's schema
insert_query = 'INSERT INTO volunteers (name, last_name, email, phone) VALUES (%s, %s, %s, %s)'

for item in data:
    values = (item['first name'], item['last name'], item['email'], item['phone']) 
    cur.execute(insert_query, values)

conn.commit()  # Commit the transaction
cur.close()
conn.close()
