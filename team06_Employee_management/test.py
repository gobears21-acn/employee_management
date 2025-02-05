import mysql

try:
    # Step 1: Connect to the database
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",  # Make sure to include the password if required
        db="system_development_06"
    )

    # Step 2: Create a cursor object
    cursor = db.cursor()

    # Step 3: Execute an SQL query
    cursor.execute("SELECT * FROM employee_details")

    # Step 4: Fetch the result
    data = cursor.fetchone()
    print(data)

except MySQLdb.Error as e:
    print(f"Error connecting to MySQL database: {e}")

finally:
    # Step 5: Close the cursor and connection
    if cursor:
        cursor.close()
    if db:
        db.close()