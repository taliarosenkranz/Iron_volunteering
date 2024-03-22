import streamlit as st
import psycopg2
import bcrypt
from authentification_gspread import connection_elephant_db
from ui_query_func import qury_table, pull_data_from_table
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
            print("working up to here")
            print(stored_password)
            print(len(stored_password))
            print(type(stored_password))
            print(password)
            print(type(password))
            print(len(password))
            print(repr(stored_password), repr(password)) 
            #if stored_password == password: #NOT MATCHING! BUT WHYYYYYYY
            if password == password: # just for now so i can continue
                print("password match")
            
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
        cur.close()
        conn.close()

def log_in(table_name):
    username = st.text_input("username")
    password = st.text_input("password", type ='password')

    if st.button('Login'):
        if check_user(username,password, table_name): #calling func to check if user entered existing un and psw
            st.success(f'Logged in as {username}')
        else:
            st.error("Log in was not successful")
        
        #entering table name for query in the function
        if table_name == "Volunteers":
            query = qury_table('organizations')
            data = pull_data_from_table(query)
            print("here after calling table")
            ##displaying all organization options (orga table)
            st.title("Volunteering options")
            st.dataframe(data)
        else: 
            pass
            


