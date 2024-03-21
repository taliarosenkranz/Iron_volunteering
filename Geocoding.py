import requests

# Define the base URL for the Nominatim API
nominatim_base_url = 'https://nominatim.openstreetmap.org/search'

# Define the address you want to geocode
address = '39 Gordon J.L., Tel-Aviv, IL'

# Construct the request URL
url = f'{nominatim_base_url}?q={address}&format=json'

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

        print(f'Latitude: {latitude}, Longitude: {longitude}')
    else:
        print('No results found.')
else:
    print('Failed to retrieve data from the API.')