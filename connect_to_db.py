# IMPORTS---------------------------------------------------------
import mysql.connector
# ----------------------------------------------------------------

def get_db_connection():
    return mysql.connector.connect(
<<<<<<< HEAD
        host = "localhost",
        user = "root",
        password = "password",
        database = "database"
=======
        host = "host",
        user = "user",
        password = "password",
        database = "database-name"
>>>>>>> 5b7e476f2b42daad6edf07bc8623d93e88a1516c
    )
