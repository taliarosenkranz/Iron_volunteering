import psycopg2

from authentification_gspread import connection_elephant_db

def update_available_spots():
    #  create connection to db
    conn = connection_elephant_db()
    cur = conn.cursor()
    print("Connection to Elephant established")

    try:
        # Query to update available spots based on volunteers per day
        update_query = """
            UPDATE date_schedule 
            SET available_spots = available_spots - (
                SELECT COUNT(*) 
                FROM volunteers_per_day 
                WHERE volunteers_per_day.date = date_schedule.date 
                AND volunteers_per_day.organization_fk_id = date_schedule.org_id_fk
            )
            WHERE date IN (
                SELECT date 
                FROM volunteers_per_day
            );
        """

        # Execute the update query
        cur.execute(update_query)

        # Commit the changes
        conn.commit()
        print("Available spots updated successfully.")
        #return result

    except Exception as e:
        print("Error occurred:", e)
        # Rollback the transaction if an error occurs
        conn.rollback()

    finally:
        # Close the connection
        conn.close()
    
    

