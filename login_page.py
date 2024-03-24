import streamlit as st
from datetime import datetime
import psycopg2
import bcrypt
from authentification_gspread import connection_elephant_db
from ui_query_func import qury_table, pull_data_from_table,query_volunteers_per_day,query_user_history
from maping import map
from sign_up_form import sign_up

def check_user(username,password, table_name):
    try:
        #create connection to db
        conn = connection_elephant_db()
        cur = conn.cursor()
        print("Connection to Elephant established")

        if table_name == "Volunteers":
            cur.execute(f'SELECT v_psw FROM {table_name} where v_name = %s',(username,)) # NOT SURE IF QUERY RUNS
            user_record = cur.fetchone() #saves one row of the query in a tuple 
            print("SQL volunteers run successful")
        elif table_name == "organizations":
            cur.execute(f'SELECT org_psw FROM {table_name} where org_name = %s',(username,)) # NOT SURE IF QUERY RUNS:
            user_record = cur.fetchone() #saves one row of the query in a tuple 
            print("SQL organizations run successful")
        else:
            print("error with table name")
            
        if user_record: #if user_record is not null meaning the query found data in the table
            stored_password = user_record[0] #saving password from db in this variable
            if stored_password == password: 
                print("password match")
                #cur.close()
                #conn.close()
                return True
            else:
                print("passwords are not matching")
            #if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')): #method that check if entered pw and pw in db matches
            #    print("password correct")
            #     return True  # Password matches
        else:
            print("User data not found. Try again or register to create an account")
            return False
        
            
    except Exception as e:
        print(f'An error occured {e}')

    finally:  
        print("done checking user")
        #cur.close()
        #conn.close()

def log_in(table_name):
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'login_attempted' not in st.session_state:
        st.session_state.login_attempted = False
    
    username = st.text_input("Username", key="usern")
    password = st.text_input("Password", key="psw", type='password')
    print(password)

    if st.button('Login', key= "login button") and not st.session_state.logged_in:
        st.session_state.login_attempted = True
        if check_user(username,password, table_name): #calling func to check if user entered existing un and psw
            st.success(f'Logged in as {username}')
            st.session_state.logged_in = True
        else:
            #print("registration function should be called now")
            st.error("Log in was not successful")
        
        #entering table name for query in the function
    if st.session_state.logged_in:
        if table_name == "Volunteers":
            selected_date = st.date_input("Select a date:", datetime.today(), key='vol_date') #USE selected_date in map query
            st.write("Selected Date:", selected_date)
            final_map = map()
            query = qury_table('organizations')
            data = pull_data_from_table(query)
            print("here after calling table")
            sign_up(selected_date)
            ##displaying all organization options (orga table)
            st.title("Volunteering options")
            st.dataframe(data)

            #showing history table
            st.title(f'{username}s volunteering history: ')
            query_history = query_user_history(username, selected_date)
            history_data = pull_data_from_table(query_history)
            st.dataframe(history_data)
        else: #organizations page!
            #displayed in orga account
            print("AM I EVEN HERE WHERE I SHOULD BE?")
            query = query_volunteers_per_day(username) 
            print("DID I MAKE IT TO HERE??")
            print(query)
            data = pull_data_from_table(query)
            st.subheader(f'{username}s signed up volunteers for selected date: ')
            st.dataframe(data)
    else:
        print("user not logged in")


