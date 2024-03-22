import psycopg2
import streamlit as st
from ui_query_func import qury_table, pull_data_from_table

#file for calling functions necessary for the UI

#page showing all organizations in table format
query = qury_table('organizations')
data = pull_data_from_table(query)

#displaying data in Streamlit
st.title("Volunteering options")
st.dataframe(data)
