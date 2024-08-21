 # TO CREATE TABLE 
import mysql.connector as sql

conn = sql.connect(host='localhost', user='root', passwd='charansingh', database='python')
c1 = conn.cursor()

if conn.is_connected():
    print("Connection successful")
else:
    print("Error try later again")

def table_creation():
    create_user_table = """CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), contact INT(12), deposited VARCHAR(255), balance VARCHAR(255))"""
    with conn.cursor() as cursor:
        cursor.execute(create_user_table)
        conn.commit()

table_creation()
