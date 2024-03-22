from authentification_gspread import pull_data_from_sheets, insert_data, connection_elephant_db

#creates connection to db
conn = connection_elephant_db()
cur = conn.cursor() # always need this after calling connection_elephant function

#pull data from sheets
data_volunteers = pull_data_from_sheets("Volunteers (Responses)") #variable referred to as data_row in insert_data func
#UNCOMMENT BELOW ONCE FORM WAS CREATED FOR THESE. ENTER APPROPRIATE SHEET NAME
data_organizations = pull_data_from_sheets("Iron volunteers_organizations (Responses)")


table_volunteers = insert_data(
    cur=cur, 
    table_name='volunteers', 
    column_table_names=['v_name', 'last_name', 'v_email', 'v_phone', 'v_psw'],
    column_sheet_names=['first name','last name', 'Email Address', 'phone',
                        'Please create a strong password to log in (max 18 characters)'],
    data_row=data_volunteers
)


table_organizations = insert_data(
    cur=cur,
    table_name='organizations',
    column_table_names=['org_email', 'org_psw', 'org_name', 'address','city', 'org_phone', 'url', 'description',
                        'category', 'num_volunteers'],
    column_sheet_names=['Email Address', 'Please create a strong password to log in (max 18 characters)',
                        'Organization name', 'Address',	'Phone number',	'Website',
                        'Description about the organization', 'Category',
                        'Spots available per day (insert just numbers)', 'city'],
    data_row=data_volunteers
)

conn.commit()
cur.close()
conn.close()
