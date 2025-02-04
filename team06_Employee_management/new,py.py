import MySQLdb

cnx = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="ipl")


# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = cnx.cursor()

rows = cur.execute('SELECT * FROM `batsman_record`')
print(rows)
for i in rows.fetchall():
    print(i)