import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from authentification_gspread import connection_elephant_db

def map():
    conn = connection_elephant_db()
    cur = conn.cursor()
    print("Connection to Elephant established")

    # Fetch data from the database
    #cur.execute(f'SELECT latitude, longitude, org_name, num_volunteers FROM organizations') #should fetch data from org and join with date_scheduled to get available_spots and filter on date!
    #cur.execute(f'SELECT o.latitude, o.longitude, o.org_name, ds.available_spots FROM Organizations o '
    #        f'JOIN date_schedule ds ON o.org_id = ds.org_id_fk;')
    cur.execute("""SELECT o.latitude, o.longitude, o.org_name, ds.available_spots 
    FROM Organizations o 
    JOIN date_schedule ds 
    ON o.org_id = ds.org_id_fk;""")
    locations = cur.fetchall()

    if locations:                 
        map = folium.Map(location=[31.0461, 34.8516], zoom_start=8,
                            min_zoom=6, max_zoom=12, tiles="OpenStreetMap", lang='en')

        # Define the boundaries of Israel
        bounds = [(29.5, 34.2), (33.5, 35.9)]
        # Restrict the map to show only Israel
        map.fit_bounds(bounds)

        coordinates = []
        # Add markers for each location and populate coordinates list
        for location_info in locations:
            # Assuming the first column contains location names
            location_name = location_info[2]
            # Assuming the second column contains latitude
            lat = float(location_info[0])
            # Assuming the third column contains longitude
            lon = float(location_info[1])
            # Assuming the fourth column contains number of volunteers needed
            num_volunteers_needed = int(location_info[3])
            print(f'num of volunteers:', num_volunteers_needed)
            # Append coordinates to the list
            coordinates.append([lat, lon, num_volunteers_needed])

            # Create marker
            popup_text = f"{location_name}<br>Volunteers Needed: {num_volunteers_needed}"
            folium.Marker([lat, lon], popup=popup_text).add_to(map)

        # Add heatmap layer
        print(coordinates[2])
        HeatMap(coordinates,min_opacity=0.4,radius=20).add_to(map)

            # Display the map
        final_map = folium_static(map)
    else:
        st.write(
            "Failed to fetch data from Google Sheets. Please check your credentials")
    
    return final_map
