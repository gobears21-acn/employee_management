from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm
from django.contrib import messages
import MySQLdb

def get_db_connection():
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",  # Make sure to include the password if needed
        db="system_development_t06"
    )
    return db


def is_admin(user):
    return user.username == 'myadmin'

from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.username == 'myadmin'

@login_required
@user_passes_test(is_admin)
def admin_search(request):
    db = get_db_connection()
    query = request.GET.get('q')
    user_id = request.user.username  # Assuming the username is the same as EID
    try:
        with db.cursor() as cursor:
            if query:
                cursor.execute("SELECT * FROM employee_details WHERE Employee_Name LIKE %s", ('%' + query + '%',))
            else:
                cursor.execute("SELECT * FROM employee_details")
            
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            users = [dict(zip(columns, row)) for row in data]

            # 获取当前登录用户的 EID
            user_eid = request.user.username
            # 获取当前登录用户的头像
            cursor.execute("SELECT Profile_Image FROM employee_details WHERE EID = %s", [user_id])
            user_image = cursor.fetchone()[0]

            return render(request, 'admin_search/admin_search.html', {'users': users, 'user_eid': user_eid, 'user_image': user_image})
    except MySQLdb.Error as e:
        print("Database error:", e)
        return render(request, 'admin_search/admin_search.html', {'users': [], 'user_eid': None, 'user_image': None})
    finally:
        db.close()



def delete_user(request, EID):
    db = get_db_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM employee_details WHERE EID = %s", (EID,))
            db.commit()
        return redirect('admin_search:admin_search')
    except MySQLdb.Error as e:
        print("Database error:", e)
        return redirect('admin_search:admin_search')
    finally:
        db.close()


def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            db = get_db_connection()
            try:
                with db.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO employee_details (Employee_Name, Employee_Number, Email, Date_of_Birth, Role, Management_Level, Home_Office, Team_ID, Position, PL_ID, Manager_ID, Profile_Image)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        form.cleaned_data['employee_name'],
                        form.cleaned_data['employee_number'],
                        form.cleaned_data['email'],
                        form.cleaned_data['date_of_birth'],
                        form.cleaned_data['role'],
                        form.cleaned_data['management_level'],
                        form.cleaned_data['home_office'],
                        form.cleaned_data['team_id'],
                        form.cleaned_data['position'],
                        form.cleaned_data['pl_id'],
                        form.cleaned_data['manager_id'],
                        form.cleaned_data['profile_image']
                    ))
                    db.commit()
                return redirect('admin_search:admin_search')
            except MySQLdb.Error as e:
                print("Database error:", e)
                return render(request, 'admin_search/add_user.html', {'form': form})
            finally:
                db.close()
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin_search/add_user.html', {'form': form})

def employee_detail(request, id):
    db = get_db_connection()
    user = id
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM `employee_details` WHERE EID = %s;", [str(user)])
        userdata = cursor.fetchall()[0]
        employee_id = userdata[1]
        name = userdata[0]
        role = userdata[5]
        email = userdata[3]
        location = userdata[7]
        level = userdata[6]
        image = userdata[12]
        
        cursor.execute("SELECT * FROM `team_details` WHERE team_id = %s;", [str(userdata[8])])
        team = cursor.fetchall()[0]
        teamname = team[1]
 
        cursor.execute("""SELECT t1.EID as eid, t2.manager_id, t2.manager_name, t4.project_name,t3.pl_id,t3.pl_name,t5.project_name
                                FROM `employee_details` as t1
                                INNER JOIN
                                manager_details as t2
                                ON t1.Manager_ID = t2.manager_id
                                INNER JOIN
                                people_lead_details as t3
                                ON t1.PL_ID = t3.pl_id
                                INNER JOIN
                                team_details as t4
                                ON t2.team_id = t4.team_id
                                INNER JOIN
                                team_details as t5
                                ON t3.team_id = t5.team_id
                                WHERE eid = %s;""", [str(user)])
        add_info = cursor.fetchall()[0]
        manager_id = add_info[1]
        manager_name = add_info[2]
        man_project_name = add_info[3]
        pl_id = add_info[4]
        pl_name = add_info[5]
        pl_project_name = add_info[6]
 
    except:
        messages.error(request, 'User Data Found')
    
    username = ' '.join(str(user).split('.')).title()
    return render(request, 'user_search/employee_detail.html', {'username': username,
                                                'user': user,
                                                'employee_id': employee_id, 
                                                'name': name,
                                                'role': role,
                                                'email': email,
                                                'location': location,
                                                'level': level,
                                                'teamname': teamname,
                                                'manager_id': manager_id,
                                                'image': image,
                                                'manager_name': manager_name,
                                                'man_project_name': man_project_name,
                                                'pl_id': pl_id,
                                                'pl_name': pl_name,
                                                'pl_project_name': pl_project_name,
                                                })