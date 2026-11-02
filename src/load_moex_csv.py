from db import get_connection
from csv_reader import read_quotes_from_csv
import psycopg


quotes = read_quotes_from_csv()


query = """
    INSERT INTO raw.moex_csv_quotes (ticker, per, trade_date, trade_time, price_open, price_high, price_low, price_close,vol)
    VALUES (%(<TICKER>)s, %(<PER>)s, %(<DATE>)s, %(<TIME>)s, %(<OPEN>)s, %(<HIGH>)s, %(<LOW>)s, %(<CLOSE>)s, %(<VOL>)s)
    ON CONFLICT (ticker, trade_date)
    DO UPDATE SET
        price_open = EXCLUDED.price_open, 
        price_high = EXCLUDED.price_high, 
        price_low = EXCLUDED.price_low, 
        price_close = EXCLUDED.price_close,
        vol = EXCLUDED.vol;
"""

try:
    with get_connection() as conn:
        print("Connected!")
        with conn.cursor() as cur:
            cur.executemany(query, quotes)
            cnt = cur.rowcount

            print(f"Quotes affected: {cnt}!")

except psycopg.OperationalError as error:
    print(f'Database connection failed: {error}')
