import psycopg2
from datetime import datetime, timedelta
from authentification_gspread import connection_elephant_db

def update_date_schedule():

    #  create connection to db
    conn = connection_elephant_db()
    cur = conn.cursor()
    print("Connection to Elephant established")
    try:
        # Query organizations to get org_id and Total spots per day
        cur.execute("SELECT org_id, num_volunteers FROM Organizations")
        organizations = cur.fetchall()
        print("SQL organizations run successful")
        # Iterate over each day of 2024
        current_date = datetime(2024, 3,23)
        end_date = datetime(2024, 3, 25)
        while current_date <= end_date:
            # Iterate over each organization
            for org_id, num_volunteers in organizations:
                # Insert row into date_schedule table
                cur.execute("""
                   INSERT INTO date_schedule (date, available_spots, org_id_fk)
                   VALUES (%s, %s, %s)
               """, (current_date, num_volunteers, org_id))
            # Move to the next day
            current_date += timedelta(days=1)
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        conn.commit()
        conn.close()



