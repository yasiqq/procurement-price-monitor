from db import get_connection

query = """
    INSERT INTO core.market_quotes (commodity_id, trade_date, price)
    SELECT 
        c.id, 
        TO_DATE(r.trade_date, 'YYYYMMDD'), 
        r.price_close::NUMERIC
    FROM raw.moex_csv_quotes AS r
    JOIN core.commodities AS c
        ON r.ticker = c.ticker
    WHERE CASE
        WHEN r.price_close ~ '^[0-9]+(\.[0-9]+)?$'
        THEN r.price_close::NUMERIC > 0
        ELSE FALSE
    END
        AND pg_input_is_valid(r.trade_date, 'date')
    ON CONFLICT (commodity_id, trade_date) 
    DO UPDATE SET
        price = EXCLUDED.price
    WHERE core.market_quotes.price IS DISTINCT FROM EXCLUDED.price;
"""

reject_query = r"""
    INSERT INTO raw.rejected_moex_csv_quotes (raw_quote_id, reason)
    SELECT
        r.id,
        CASE
            WHEN r.price_close !~ '^[0-9]+(\.[0-9]+)?$'
                THEN 'INVALID PRICE'
            ELSE 'NON-POSITIVE PRICE'
        END
    FROM raw.moex_csv_quotes AS r
    WHERE CASE
        WHEN r.price_close ~ '^[0-9]+(\.[0-9]+)?$'
            THEN r.price_close::NUMERIC <= 0
        ELSE TRUE
    END
    ON CONFLICT (raw_quote_id) DO NOTHING;
"""

reject_date_query = """
    INSERT INTO raw.rejected_moex_csv_quotes (raw_quote_id, reason)
    SELECT
        r.id,
        'INVALID DATE'
    FROM raw.moex_csv_quotes AS r
    WHERE r.trade_date !~ '^[0-9]{8}$'
       OR NOT pg_input_is_valid(r.trade_date, 'date')
    ON CONFLICT (raw_quote_id) DO NOTHING;
"""

def execute_query(cur, *, query, message):
    cur.execute(query)
    print(f"{message}: {cur.rowcount}")


with get_connection() as conn:
    with conn.cursor() as cur:
        execute_query(cur, query=reject_date_query, message="Rejected dates")
        execute_query(cur, query=reject_query, message="Rejected quotes")
        execute_query(cur, query=query, message="Quotes affected")