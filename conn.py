import mysql.connector

def execute(query, params=None):
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Directioner123",
    database="LeadManagementDB")

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result