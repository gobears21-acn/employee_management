
from django.shortcuts import render
import MySQLdb

# Establish the database connection
db = MySQLdb.connect(
    host="localhost",
    user="root",
    db="system_development_t06"
)
# View to display feedback for an employee
# def feedback(request, eid):
#     cursor = db.cursor()
#     # user = request.user
#     user = eid
 
#     # cursor.execute("SELECT * FROM `feedback_employee` WHERE EID = 'user'")
#     cursor.execute("SELECT * FROM `feedback_employee` WHERE EID = %s;", [str(user)])
#     comments = cursor.fetchall()[0]
#     print(comments)
#     person = comments[0]
#     people_lead_comment = comments[1]
#     supervisor_comment = comments[2]
#     # Close the cursor and connection
#     cursor.close()
#     db.close()
   


#     return render(request, 'feedback/show_feedback.html', {'user': user, 'person': person, 'people_lead_comment': people_lead_comment, 'supervisor_comment': supervisor_comment})
def feedback(request, eid):
    cursor = db.cursor()
    user = eid

    # Execute the query
    cursor.execute("SELECT * FROM `feedback_employee` WHERE EID = %s;", [str(user)])
    comments = cursor.fetchall()

    # Check if any comments were found
    if comments:
        # Assuming the first row contains the relevant feedback
        comment = comments[0]
        person = comment[0]
        people_lead_comment = comment[1]
        supervisor_comment = comment[2]
    else:
        # Handle the case where no feedback is found
        person = None
        people_lead_comment = None
        supervisor_comment = None

    # Close the cursor and connection
    # cursor.close()
    # db.close()

    return render(request, 'feedback.html', {
        'user': user,
        'person': person,
        'people_lead_comment': people_lead_comment,
        'supervisor_comment': supervisor_comment
    })

