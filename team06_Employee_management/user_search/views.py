from django.shortcuts import render
import MySQLdb

def get_db_connection():
    # Establish the database connection
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",  # Make sure to include the password if needed
        db="system_development_t06"
    )
    return db

def user_search(request):
    db = get_db_connection()
    query = request.GET.get('q')
    try:
        with db.cursor() as cursor:
            if query:
                cursor.execute("SELECT * FROM employee_details WHERE Employee_Name LIKE %s", ('%' + query + '%',))
            else:
                cursor.execute("SELECT * FROM employee_details")
            
            columns = [col[0] for col in cursor.description]  # Get column names
            data = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in data]  # Convert list of tuples into a list of dictionaries

            return render(request, 'user_search/user_search.html', {'users': result})
    except MySQLdb.Error as e:
        print("Database error:", e)
        return render(request, 'user_search/user_search.html', {'users': []})
    finally:
        db.close()




def welcome(request):
    return render(request, 'welcome.html')

def team(request):
    return render(request, 'team.html')