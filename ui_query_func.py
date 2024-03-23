import pandas as pd
import psycopg2
from datetime import datetime
import streamlit as st
from authentification_gspread import connection_elephant_db


conn = connection_elephant_db()
cur = conn.cursor()

def qury_table(table_name): #WHICH TABLE
    query = f'SELECT org_name as Name, num_volunteers as "available spots", address, org_phone, org_email, url as Website, description FROM {table_name}'
    return query

def query_user_history(username, selected_date):
    query = f"SELECT date, organization_name FROM volunteers_per_day WHERE user_name = '{username}' and date = '{selected_date}'"
    print(query)
    return query
def pull_data_from_table(query): #data of all signed up organization displayed in UI of volunteers page
    cur.execute(query)
    results = cur.fetchall()

    columns = [desc[0] for desc in cur.description]
    results_df = pd.DataFrame(results, columns=columns)
    
    #cur.close()
    #conn.close()
    
    return results_df

def query_volunteers_per_day(username):
    # Single date selection
    selected_date = st.date_input("Select a date:", datetime.today(), key='info_for_orga')
    st.write("Selected Date:", selected_date)
    #query = f"SELECT date, user_name, user_lastname FROM volunteers_per_day WHERE org_name = '{username}' AND date = {selected_date}"
    query = f"""SELECT vpd.date, o.org_name, vpd.user_name, vpd.user_lastname 
                FROM volunteers_per_day vpd 
                JOIN organizations o ON o.org_id = vpd.organization_fk_id 
                WHERE o.org_name = '{username}' AND vpd.date = '{selected_date}';"""
    return query

def query_org_dropdown():
    query = "select org_name from organizations"
    return query