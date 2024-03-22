from authentification_gspread import pull_data_from_sheets, insert_data, connection_elephant_db

#creates connection to db
conn = connection_elephant_db()
cur = conn.cursor() # always need this after calling connection_elephant function

#pull data from sheets
data_volunteers = pull_data_from_sheets("Volunteers (Responses)") #variable referred to as data_row in insert_data func
#UNCOMMENT BELOW ONCE FORM WAS CREATED FOR THESE. ENTER APPROPRIATE SHEET NAME
#data_volunteers = pull_data_from_sheets("organizations (Responses)")
#data_volunteers = pull_data_from_sheets("login (Responses)")

table_volunteers = insert_data(
    cur=cur, 
    table_name='volunteers', 
    column_table_names=['v_name', 'last_name', 'v_email', 'v_phone'], 
    column_sheet_names = ['first name','last name', 'email', 'phone'],
    data_row=data_volunteers
)
conn.commit()  
cur.close()
conn.close()