from db import get_connection
from cbr_reader import read_quotes_from_cbr
import psycopg

quest = read_quotes_from_cbr()

query = """
    INSERT INTO raw.cbr_currency_rates (rate_date, currency_id, nominal, value, vunit_rate)
    VALUES (%(Date)s, %(Id)s, %(Nominal)s, %(Value)s, %(VunitRate)s)
    ON CONFLICT (rate_date, currency_id) 
    DO UPDATE SET 
        value = EXCLUDED.value
"""

try:
    with get_connection() as conn:
        print("Connected!")
        with conn.cursor() as cur:
            cur.executemany(query, quest)

except psycopg.OperationalError as error:
    print(f'Database connection failed: {error}')
