import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

a = ('Токио', 20, 'облачно')

try:
    conn = psycopg2.connect(host=os.getenv("host"),
                            user=os.getenv("user"),
                            password=os.getenv("password"),
                            database=os.getenv("dbname"),
                            port=os.getenv("port")
                            )

    conn.autocommit = True

    # cursor
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO weather (city_name, temp, conditions) VALUES (%s, %s, %s)", a
        )

except Exception as e:
    print('Error', e)
finally:
    if conn:
        conn.close()
