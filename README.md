**Iron Volunteering for Operation Swards of Iron** 

Iron volunteering is a platform that connects people that are interested to help out organizations which are dedicated to support soldiers, displaced families and anyone who has been affected by the war.

Whats extra specicial about this platform? We show the demand, meaning the number of people needed, at each volunteering organization per day, updated when people sign up. This way you will avoid driving to a place that already has enough helpers on that day and you can share your time where it is needed most!

By registering to our platform, volunteers can sign up right inside the app to the most demanded organization with only a few clicks and also track their working history for their own benefit.

Organizations that want to be displayed on our map can create an account and will automatically pop up on the map, making them available for sign ups. When logged in, the organization can also see the details of the volunteers that are signed up to come by on any selected day.


**To do when cloning the repo to run locally:**
1. pip install -r requirements.txt
2. Generate google api secret key 
3. In authentication_gspread.py file, exchange 'creds' variable with path to where secret key is saved. 
````creds = ServiceAccountCredentials.from_json_keyfile_name('your_path_here/google_api_key.json', scope)````
4. to run application: 
 ````streamlit run main.py````


 💙 Ariel & Talia  🤍

Partial Demo of the platform:

https://github.com/taliarosenkranz/Iron_volunteering/assets/85115270/40c15b37-671d-400e-b075-97056be24a79

