import mysql.connector



def insert_data(query,):
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Directioner123",
    database="LeadManagementDB")

    cursor= connection.cursor()
    cursor.execute(query)
    connection.commit()



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

def update_data(query):
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Directioner123",
    database="LeadManagementDB")

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
