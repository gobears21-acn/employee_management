# employee/views.py
from django.shortcuts import render
import MySQLdb
db = MySQLdb.connect(
    host="localhost",
    user="root",
    db="system_development_t06"
)
 

def employee_training_history(request):
    cursor = db.cursor()
    user = request.user
    user = 'akira.yamamoto'
 
    cursor.execute("""SELECT t1.training_code , t1.training_name , t1.duration , t1.lead_manager_id  
                FROM training_details t1  INNER JOIN training_transaction
                on  training_transaction.training_code = t1.training_code
                WHERE training_transaction.eid = %s ;""", [str(user)])
    
    columns = [col[0] for col in cursor.description]  # Get column names
    data = cursor.fetchall()
 
            # Convert list of tuples into a list of dictionaries
    result = [dict(zip(columns, row)) for row in data]
    # Close the cursor and connection
    cursor.close()
    db.close()
    
    
    return render(request, 'employee/training_history.html', {'training_history' :result , 'user':user})
