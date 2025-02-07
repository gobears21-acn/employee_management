# training_detail/views.py
from django.shortcuts import render
import MySQLdb

def get_db_connection():
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",  # 确保包含密码
        db="system_development_t06"
    )
    return db

def employee_training_history(request):
    db = get_db_connection()
    cursor = db.cursor()
    user = request.user.username  # 使用当前登录用户的用户名

    cursor.execute("""SELECT t1.training_code , t1.training_name , t1.duration , t1.lead_manager_id  
                FROM training_details t1  INNER JOIN training_transaction
                on  training_transaction.training_code = t1.training_code
                WHERE training_transaction.eid = %s ;""", [str(user)])
    
    columns = [col[0] for col in cursor.description]  # 获取列名
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]  # 将元组列表转换为字典列表
    
    cursor.close()
    db.close()
    
    return render(request, 'training_detail/training_history.html', {'training_history': result, 'user': user})