from db import get_connection
from csv_reader import read_quotes_from_csv
import psycopg


quotes = read_quotes_from_csv()


query = """
    INSERT INTO raw.market_quotes (ticker, trade_date, price, source)
    VALUES (%(ticker)s, %(trade_date)s, %(price)s, %(source)s)
    ON CONFLICT (ticker, trade_date) DO NOTHING;
"""

try:
    with get_connection() as conn:
        print("Connected!")
        with conn.cursor() as cur:
            cur.executemany(query, quotes)
            cnt = cur.rowcount

            print(f"Quote inserted: {cnt}!")

except psycopg.OperationalError as error:
    print(f'Database connection failed: {error}')
