from db import get_connection

query = """
    INSERT INTO core.currency_rates (rate_date, currency_code, rate_rub)
SELECT
    r.rate_date,
    'USD',
    r.rate_value / r.nominal_value
FROM (
    SELECT
        currency_id,

        CASE
            WHEN rate_date ~ '^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$'
                 AND pg_input_is_valid(
                     SUBSTRING(rate_date FROM 7 FOR 4) || '-' ||
                     SUBSTRING(rate_date FROM 4 FOR 2) || '-' ||
                     SUBSTRING(rate_date FROM 1 FOR 2),
                     'date'
                 )
            THEN (
                SUBSTRING(rate_date FROM 7 FOR 4) || '-' ||
                SUBSTRING(rate_date FROM 4 FOR 2) || '-' ||
                SUBSTRING(rate_date FROM 1 FOR 2)
            )::DATE
            ELSE NULL
        END AS rate_date,

        CASE
            WHEN pg_input_is_valid(REPLACE(value, ',', '.'), 'numeric')
            THEN REPLACE(value, ',', '.')::NUMERIC
            ELSE NULL
        END AS rate_value,

        CASE
            WHEN pg_input_is_valid(nominal, 'numeric')
            THEN nominal::NUMERIC
            ELSE NULL
        END AS nominal_value

    FROM raw.cbr_currency_rates
) AS r
WHERE r.currency_id = 'R01235'
    AND r.rate_date IS NOT NULL
    AND r.rate_value > 0
    AND r.nominal_value > 0
ON CONFLICT (rate_date, currency_code)
DO UPDATE SET
    rate_rub = EXCLUDED.rate_rub
WHERE core.currency_rates.rate_rub IS DISTINCT FROM EXCLUDED.rate_rub;
"""

def execute_query(cur, *, query, message):
    cur.execute(query)
    print(f"{message}: {cur.rowcount}")


with get_connection() as conn:
    with conn.cursor() as cur:
        execute_query(cur, query=query, message="Currency rates affected")