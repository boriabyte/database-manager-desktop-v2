# IMPORTS---------------------------------------------------------
import mysql.connector
# ----------------------------------------------------------------

def get_db_connection():
    return mysql.connector.connect(
        host = "host",
        user = "user",
        password = "password",
        database = "database-name"
    )
