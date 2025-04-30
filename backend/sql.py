import mysql.connector
from mysql.connector import Error

def create_connection(hostname, uid, pwd, dbname):
    conn=None
    try:
        conn=mysql.connector.connect(
            host = hostname,
            user = uid,
            password = pwd,
            database = dbname
        )
    except Error as e:
        print("Error is ", e)
    return conn

def execute_read_query(myconn, sql):
    rows = None
    mycursor = myconn.cursor(dictionary=True)
    try:
        mycursor.execute(sql)
        rows = mycursor.fetchall()
        return rows
    except Error as e:
        print("Error is ", e)

def execute_update_query(myconn, sql):
    mycursor = myconn.cursor(dictionary=True)
    try:
        mycursor.execute(sql)
        myconn.commit()
    except Error as e:
        print('Error is', e)
 