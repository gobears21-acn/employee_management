from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm
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

def admin_search(request):
    db = get_db_connection()
    query = request.GET.get('q')
    try:
        with db.cursor() as cursor:
            if query:
                cursor.execute("SELECT * FROM employee_details WHERE username LIKE %s", ('%' + query + '%',))
            else:
                cursor.execute("SELECT * FROM employee_details")
            
            columns = [col[0] for col in cursor.description]  # Get column names
            data = cursor.fetchall()
            users = [dict(zip(columns, row)) for row in data]  # Convert list of tuples into a list of dictionaries

            return render(request, 'admin_search/admin_search.html', {'users': users})
    except MySQLdb.Error as e:
        print("Database error:", e)
        return render(request, 'admin_search/admin_search.html', {'users': []})
    finally:
        db.close()

def delete_user(request, user_id):
    db = get_db_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM employee_details WHERE id = %s", (user_id,))
            db.commit()
        return redirect('admin_search')
    except MySQLdb.Error as e:
        print("Database error:", e)
        return redirect('admin_search')
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
                        INSERT INTO employee_details (employee_name, employee_number, email, date_of_birth, role, management_level, home_office, team_id, position, pl_id, manager_id, profile_image)
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
                return redirect('admin_search')
            except MySQLdb.Error as e:
                print("Database error:", e)
                return render(request, 'admin_search/add_user.html', {'form': form})
            finally:
                db.close()
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin_search/add_user.html', {'form': form})