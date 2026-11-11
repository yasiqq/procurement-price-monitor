from db import get_connection

query = """
    INSERT INTO core.market_quotes (commodity_id, trade_date, price)
    SELECT
        c.id,
        r.TRADEDATE::DATE,
        r.CLOSE::NUMERIC
    FROM raw.moex_history AS r
    JOIN core.commodities AS c
        ON c.ticker = r.SECID
    WHERE CASE
        WHEN pg_input_is_valid(r.CLOSE, 'numeric')
        THEN r.CLOSE::NUMERIC > 0
        ELSE FALSE
    END
        AND pg_input_is_valid(r.TRADEDATE, 'date')
    ON CONFLICT (commodity_id, trade_date)
    DO UPDATE SET
        price = EXCLUDED.price
    WHERE core.market_quotes.price IS DISTINCT FROM EXCLUDED.price;
"""

def execute_query(cur, *, query, message):
    cur.execute(query)
    print(f"{message}: {cur.rowcount}")


with get_connection() as conn:
    with conn.cursor() as cur:
        execute_query(cur, query=query, message="Quotes affected")