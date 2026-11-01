from db import get_connection

query = """
    INSERT INTO core.market_quotes (commodity_id, trade_date, price)
    SELECT
        c.id,
        r.trade_date::DATE,
        r.price::NUMERIC
    FROM raw.market_quotes AS r
    JOIN core.commodities AS c
        ON r.ticker = c.ticker
    WHERE CASE
        WHEN r.price ~ '^[0-9]+(\.[0-9]+)?$'
        THEN r.price::NUMERIC > 0
        ELSE FALSE
    END
        AND pg_input_is_valid(trade_date, 'date')
    ON CONFLICT (commodity_id, trade_date) DO NOTHING;
"""

reject_query = """
    INSERT INTO raw.rejected_quotes (raw_quote_id, reason)
    SELECT
        id,
        CASE
            WHEN price !~ '^[0-9]+(\.[0-9]+)?$'
            THEN 'INVALID PRICE'
            ELSE 'NON-POSITIVE PRICE'
        END
    FROM raw.market_quotes AS r
    WHERE CASE
        WHEN r.price ~ '^[0-9]+(\.[0-9]+)?$'
        THEN r.price::NUMERIC <= 0
        ELSE TRUE
    END
    ON CONFLICT (raw_quote_id) DO NOTHING;
"""

reject_date_query = """
    INSERT INTO raw.rejected_quotes (raw_quote_id, reason)
    SELECT 
        id,
        'INVALID DATE'
    FROM raw.market_quotes
    WHERE NOT pg_input_is_valid(trade_date, 'date')
    ON CONFLICT (raw_quote_id) DO NOTHING;
"""

def execute_query(cur, *, query, message):
    cur.execute(query)
    print(f"{message}: {cur.rowcount}")


with get_connection() as conn:
    with conn.cursor() as cur:
        execute_query(cur, query=reject_date_query, message="Rejected dates")
        execute_query(cur, query=reject_query, message="Rejected quotes")
        execute_query(cur, query=query, message="Quotes inserted")