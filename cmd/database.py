import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect_to_database():
    try:
        conn = psycopg2.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("dbname"),
            port=os.getenv("port")
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print('Error:', e)
        return None


def close_database_connection(conn):
    if conn:
        conn.close()


def get_weather():
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM weather")
                return cur.fetchall()
        except Exception as e:
            print('Error:', e)
        finally:
            close_database_connection(conn)

    return []


def insert_weather(a):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO weather (city_name, temp, conditions) VALUES (%s, %s, %s)", a
                )
        except Exception as e:
            print('Error:', e)
        finally:
            close_database_connection(conn)
