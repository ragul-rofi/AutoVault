import psycopg2
from psycopg2 import sql

def authenticate_user(email,password):
    try:
        conn = psycopg2.connect(
            dbname="autovault",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
    )
        cur = conn.cursor()
        query = sql.SQL("select id,name, role from users where email = %s and password = %s")
        cur.execute(query,(email,password))
        result = cur.fetchone()
        cur.close()
        conn.close()

        return result # None if not found
    except Exception as e:
        print("Database error: ",e)
        return None

