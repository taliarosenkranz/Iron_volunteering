import psycopg2
import streamlit as st
from ui_query_func import qury_table, pull_data_from_table
from login_page import log_in
from Geocoding import long_lat_add
from maping import map
from trigger_org_schedule_date import update_date_schedule
from authentification_gspread import pull_data_from_sheets, insert_data, connection_elephant_db
#file for calling functions necessary for the UI

#page to choose if volunteer or organization
def main(): #landing page
    st.title("Iron Volunteering")

    st.subheader("Help out where you are needed most")

    menu = ["Volunteer", "Organization"]
    choice = st.sidebar.selectbox("Select Role", menu)  
    
    st.write("Do you already have an account? Then Login! If you're new here, welcome! Click Register")

    if choice == "Volunteer":
        st.subheader("Hi Volunteer!")
        log_in("Volunteers")
        url = "https://forms.gle/qDfoUqctbXcrUKwh6" #link to vol form
        # register button with redirecting link to form
        button_html = f"""<a href="{url}" target="_blank"><button style='color: #31333F; background-color: #ccc; padding: 10px 24px; border-radius: 8px; border: none; cursor: pointer;'>Register</button></a>"""
        if st.markdown(button_html, unsafe_allow_html=True):
            print("we are in the if after button was clicked")
            #creates connection to db
            conn = connection_elephant_db()
            cur = conn.cursor() # always need this after calling connection_elephant function
            data_volunteers = pull_data_from_sheets("Volunteers (Responses)")
            table_volunteers = insert_data(
            cur=cur,
            table_name='volunteers',
            column_table_names=['v_name', 'last_name', 'v_email', 'v_phone', 'v_psw'],
            column_sheet_names=['first name', 'last name', 'Email Address', 'phone',
                                'Please create a strong password to log in (max 18 characters)'],
            data_row=data_volunteers)
            conn.commit()
            cur.close()
            conn.close()
            
    
    else:
        st.subheader("Log in as an organization if you have an account")
        log_in("organizations") #entering table name for query in the function
        url = "https://forms.gle/RRY5k2CYbzugaRcr9" #link to orga form
        # register button with redirecting link to form 
        button_html = f"""<a href="{url}" target="_blank"><button style='color: #31333F; background-color: #ccc; padding: 10px 24px; border-radius: 8px; border: none; cursor: pointer;'>Register</button></a>"""
        if st.markdown(button_html, unsafe_allow_html=True): 
            print("button was clicked and user was redirected")
            conn = connection_elephant_db()
            cur = conn.cursor()
            data_organizations = pull_data_from_sheets("Iron volunteers_organizations (Responses)")
            table_organizations = insert_data(
            cur=cur,
            table_name='organizations',
            column_table_names=['org_name', 'num_volunteers', 'address', 'org_phone', 'url', 'description', 'org_email',
                                'category', 'org_psw', 'city'],
            column_sheet_names=['Organization name', 'Spots available per day (insert just numbers)', 'Address',
                                'Phone number', 'Website', 'Description about the organization', 'Email Address',
                                'Category', 'Please create a strong password to log in (max 18 characters)',
                                'City'],
            data_row=data_organizations)
            conn.commit()
            cur.close()
            conn.close()
            print("updating date_schedule")
            update_date_schedule()
            print("done updating date_schedule")
            
            print("done calling available spots function")
            #update table with lat long 
            print("calling the long_lat function")
            long_lat_add()
            print("lat long func done")


#main_page = main()
# run the main functin to start Streamlit application
if __name__ == "__main__":
    main()




