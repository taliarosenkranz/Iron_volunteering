from authentification_gspread import pull_data_from_sheets, insert_data, cur, conn

#pull data from sheets
data_volunteers = pull_data_from_sheets("Volunteers (Responses)") #variable referred to as data_row in insert_data func
#UNCOMMENT BELOW ONCE FORM WAS CREATED FOR THESE. ENTER APPROPRIATE SHEET NAME
#data_volunteers = pull_data_from_sheets("organizations (Responses)")
#data_volunteers = pull_data_from_sheets("login (Responses)")

table_volunteers = insert_data(
    #cursor=cur, 
    table_name='volunteers', 
    column_table_names=['name', 'last_name', 'email', 'phone'], 
    column_sheet_names = ['first name','last name', 'email', 'phone'],
    data_row=data_volunteers
)
conn.commit()  
cur.close()
conn.close()