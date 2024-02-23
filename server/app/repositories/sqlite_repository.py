import sqlite3

def connect_to_database(database_name):
    try:
        connection = sqlite3.connect(database_name)
        return connection
    except Exception as ex:
        print("Error while attempt to connecting to db:" + ex)

