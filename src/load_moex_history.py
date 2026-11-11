from db import get_connection
from moex_iss_reader import read_quotes_from_iss
import psycopg

quest = read_quotes_from_iss()

query = """
    INSERT INTO raw.moex_history (BOARDID, TRADEDATE, SHORTNAME, SECID, OPEN, LOW, HIGH, CLOSE, NUMTRADES, WAPRICE)
    VALUES (%(BOARDID)s, %(TRADEDATE)s, %(SHORTNAME)s, %(SECID)s, %(OPEN)s, %(LOW)s, %(HIGH)s, %(CLOSE)s, %(NUMTRADES)s, %(WAPRICE)s)
    ON CONFLICT (TRADEDATE, SECID) DO NOTHING
"""

try:
    with get_connection() as conn:
        print("Connected!")
        with conn.cursor() as cur:
            cur.executemany(query, quest)

except psycopg.OperationalError as error:
    print(f'Database connection failed: {error}')
