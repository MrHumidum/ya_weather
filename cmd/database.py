import psycopg2
import datetime
import requests

MY_TOKEN = open('txts/token.txt').readline()


def openweathermap(city_name):
    appid = MY_TOKEN
    try:
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={appid}&lang=ru&units=metric")
        data = res.json()
        return {'icoid': data['weather'][0]['icon'],
                "Погода": data['weather'][0]['description'],
                "Температура": int(data['main']['temp'])}
    except Exception as e:
        print("Error openweathermap:", e)
        pass


def connect_to_database():
    host, user, password, port, database = open('txts/databasetxt.txt').readline().split(", ")
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        print('connect_to_database', conn)
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
            return 'username'
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
