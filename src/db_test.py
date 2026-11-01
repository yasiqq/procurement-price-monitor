import psycopg
from db import get_connection

try:
    with get_connection() as conn:
        print("Connected!")

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM core.commodities;")
            result = cur.fetchone()
            print(result)

except psycopg.OperationalError as error:
    print(f'Database connection failed: {error}')