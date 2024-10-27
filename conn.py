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

def delete_lead(email):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Directioner123",
        database="LeadManagementDB"
    )

    cursor = connection.cursor()
    
    # Use a parameterized DELETE query
    delete_query = "DELETE FROM data_lead WHERE email = %s"
    
    try:
        cursor.execute(delete_query, (email,))  # Pass email as a parameter
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Print error if one occurs
    finally:
        cursor.close()
        connection.close()