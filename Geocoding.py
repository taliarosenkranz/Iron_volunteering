import requests
import psycopg2
import urllib.parse as up
from authentification_gspread import insert_data, connection_elephant_db


# Define the base URL for the Nominatim API
nominatim_base_url = 'https://nominatim.openstreetmap.org/search'
def long_lat_add():

    #  create connection to db
    conn = connection_elephant_db()
    cur = conn.cursor()
    print("Connection to Elephant established")
    try:
        cur.execute(f'SELECT address,city FROM organizations where latitude = 0')
        organizations = cur.fetchall()  # saves one row of the query in a tuple
        print("SQL organizations run successful")

        for org in organizations:
            address, city = org
            # Construct the request URL
            url = f'{nominatim_base_url}?q={address}, {city}&format=json'

            # Send the HTTP GET request to the API
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                # Extract latitude and longitude from the response
                if data:
                    latitude = data[0]['lat']
                    longitude = data[0]['lon']

                    # Update the organizations table with latitude and longitude
                    cur.execute("UPDATE organizations SET latitude = %s, longitude = %s WHERE address = %s",
                                (latitude, longitude, address))
                    conn.commit()
                    print(f'Organization with address {address}: Latitude - {latitude}, Longitude - {longitude}')
                else:
                    print(f'Organization with address {address}: No results found for address {address}, {city}')
            else:
                print(f'Organization with address {address}: Failed to retrieve data from the API.')
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()
long_lat_add()