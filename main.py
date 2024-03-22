import psycopg2
import streamlit as st
from ui_query_func import qury_table, pull_data_from_table
from login_page import log_in
#file for calling functions necessary for the UI

#page to choose if volunteer or organization
def main(): #landing page
    st.title("Iron Volunteers")
    st.subheader("Help out where you are needed most")

    menu = ["Volunteer", "Organization"]
    choice = st.sidebar.selectbox("Select Role", menu)

    if choice == "Volunteer":
        st.subheader("Hi Volunteer!")
        st.write("Do you already have an account?")
        st.write("Do you want to register to see volunteering options and their demand?")
        if st.button("Login"):
            log_in("Volunteers")
        elif st.button("Register"):
            st.write("Do you want to register to see volunteering options and their demand?")
            # CALL FUNCTION FOR REGISTRATION
            pass
      

        

    else:
        st.subheader("Log in as an organization if you have an account")
        login_organization = log_in("organizations") #entering table name for query in the function


#page showing all organizations in table format
main_page = main()




#in the end close connection here??
#cur.close()
#conn.close()