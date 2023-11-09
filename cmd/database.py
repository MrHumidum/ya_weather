import psycopg2
import os
from dotenv import load_dotenv
import datetime

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
        print('Error connect_to_database:', e)
        return None


def close_database_connection(conn):
    if conn:
        conn.close()


def get_weather():
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT time, city_name, temp, conditions FROM weather")
                return cur.fetchall()
        except Exception as e:
            print('Error get_weather:', e)
        finally:
            close_database_connection(conn)

    return []


def insert_weather(a):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cur.execute(
                    "INSERT INTO weather (time, city_name, temp, conditions) VALUES (%s, %s, %s, %s)",
                    (current_time, a[0], a[1], a[2])
                )
        except Exception as e:
            print('Error insert_weather:', e)
        finally:
            close_database_connection(conn)


def clear_weather():
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM weather",
                )
        except Exception as e:
            print('Error clear_weather:', e)
        finally:
            close_database_connection(conn)


def sign_up_func(a):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    a
                )
        except Exception as e:
            print('Error sign_up_func:', e)
        finally:
            close_database_connection(conn)


def sign_in_func(username, password):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT username,password from users "
                    f"where username like '{username}' and password like '{password}'",
                )
                return cur.fetchall()
        except Exception as e:
            print('Error sign_in_func:', e)
        finally:
            close_database_connection(conn)
