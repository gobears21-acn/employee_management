from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import MySQLdb

# def get_db_connection():
#     # Establish the database connection
#     db = MySQLdb.connect(
#         host="localhost",
#         user="root",
#         passwd="",  # Make sure to include the password if needed
#         db="system_development_t06"
#     )
#     return db



# def team(request):
#     query = request.user

#     db = get_db_connection()
#     query = request.GET.get('team_identifier')
#     try:
#         with db.cursor() as cursor:
#             if query:
#                 cursor.execute("SELECT * FROM team_details WHERE team_id = %s", (query,))
#                 team_data = cursor.fetchone()
#                 if team_data:
#                     team_id = team_data[0]  # Assuming the first column is the team ID
#                     cursor.execute("SELECT * FROM employee_details WHERE Team_ID = %s", (team_id,))
#                     members_data = cursor.fetchall()
#                     columns = [col[0] for col in cursor.description]
#                     members = [dict(zip(columns, row)) for row in members_data]
#                 else:
#                     members = []
#             else:
#                 with db.cursor() as cursor:
#                     cursor.execute("SELECT * FROM `employee_details` WHERE EID = %s;", [str(request.user)])
#                     team = cursor.fetchall()[0][8]
#                     if team:
#                         cursor.execute("SELECT * FROM team_details WHERE team_id = %s", (team,))
#                         team_data = cursor.fetchone()
#                         if team_data:
#                             team_id = team_data[0]  # Assuming the first column is the team ID
#                             cursor.execute("SELECT * FROM employee_details WHERE Team_ID = %s", (team_id,))
#                             members_data = cursor.fetchall()
#                             columns = [col[0] for col in cursor.description]
#                             members = [dict(zip(columns, row)) for row in members_data]
#                         else:
#                             members = []
#                     else:
#                         members = []
#                     return render(request, 'team/team.html', {'members': members, 'query': query})
#             return render(request, 'team/team.html', {'members': members, 'query': query})
#     except MySQLdb.Error as e:
#         print("Database error:", e)
#         return render(request, 'team/team.html', {'members': [], 'query': query})
#     finally:
#         db.close()

def get_db_connection():
    # Establish the database connection
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",  # Make sure to include the password if needed
        db="system_development_t06"
    )
    return db

def help(request):
    return render(request, 'help.html')

@login_required
def team(request):
    db = get_db_connection()
    query = request.GET.get('team_identifier')
    user_id = request.user.username  # Assuming the username is the same as EID
    try:
        with db.cursor() as cursor:
            if query:
                cursor.execute("SELECT * FROM team_details WHERE team_id = %s", (query,))
                team_data = cursor.fetchone()
                if team_data:
                    team_id = team_data[0]  # Assuming the first column is the team ID
                    cursor.execute("SELECT * FROM employee_details WHERE Team_ID = %s", (team_id,))
                    members_data = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]
                    members = [dict(zip(columns, row)) for row in members_data]
                else:
                    members = []
            else:
                cursor.execute("SELECT * FROM `employee_details` WHERE EID = %s;", [str(request.user)])
                team = cursor.fetchall()[0][8]
                if team:
                    cursor.execute("SELECT * FROM team_details WHERE team_id = %s", (team,))
                    team_data = cursor.fetchone()
                    if team_data:
                        team_id = team_data[0]  # Assuming the first column is the team ID
                        cursor.execute("SELECT * FROM employee_details WHERE Team_ID = %s", (team_id,))
                        members_data = cursor.fetchall()
                        columns = [col[0] for col in cursor.description]
                        members = [dict(zip(columns, row)) for row in members_data]
                    else:
                        members = []
                else:
                    members = []

            # Get current logged-in user's profile image
            cursor.execute("SELECT Profile_Image FROM employee_details WHERE EID = %s", [user_id])
            user_image = cursor.fetchone()[0]

            return render(request, 'team/team.html', {'members': members, 'query': query, 'user_image': user_image})
    except MySQLdb.Error as e:
        print("Database error:", e)
        return render(request, 'team/team.html', {'members': [], 'query': query, 'user_image': None})
    finally:
        db.close()