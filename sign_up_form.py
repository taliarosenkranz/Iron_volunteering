from re import T
import streamlit as st
from authentification_gspread import insert_data, connection_elephant_db
from ui_query_func import query_org_dropdown, pull_data_from_table
from update_available_spots import update_available_spots

#form to sign up for volunteering at certain orga on certain day

conn = connection_elephant_db()
cur = conn.cursor()

def insert_data(table_name, column_table_names, column_form_names, data_row, cur):
    #inserting data from sheets to db table
    placeholders = ', '.join(['%s'] * len(column_table_names)) # %s placeholders for sql query values
    column_table_names_str = ', '.join(column_table_names) #transfers from list values to one long string
    insert_query = f'INSERT INTO {table_name} ({column_table_names_str}) VALUES ({placeholders})' #SQL Query

    for item in data_row:
        # Extracting values in the order of column names in sheets saving in tuple variable 
        values = tuple(data_row) 
        cur.execute(insert_query, values)

def sign_up(selected_date):
    query_org_names = query_org_dropdown()
    print('query',query_org_names)
    data = pull_data_from_table(query_org_names)
    print('data', data)
    dropdown_options = data['org_name'].tolist()
    print('options', dropdown_options)
    

    with st.form(key="sign_up", clear_on_submit=True):
        user_fk_id = 400
        organization_fk_id = 404
        user_name = st.text_input("First Name: ")
        user_lastname = st.text_input("Last Name: ")
        date = selected_date
        organization_name = st.selectbox("Choose an organization:", dropdown_options) 
        submit_button = st.form_submit_button("Sign up!")
    if submit_button:
        st.success("Thank you! You are signed up and ready to help our country")
        column_names = ["user_fk_id","organization_fk_id", "user_name", "user_lastname", "date", "organization_name"]
        column_form_names = ["user_fk_id","organization_fk_id","user_name", "user_lastname", "date", "organization_name"]

        volunteer_sign_up_data = [[user_fk_id,organization_fk_id, user_name, user_lastname, date, organization_name]]  # Wrapped in an extra list
        insert_data('volunteers_per_day', column_names, column_form_names, volunteer_sign_up_data[0], cur)
        print("calling available spots function")
        update_available_spots() #updating the volunteers_per_day
        print("done with updating available spots")
    print("data hopefully added to vpd table")
        #return 


