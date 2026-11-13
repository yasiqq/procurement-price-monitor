WITH prepared AS (
    SELECT
        rate_date,
        currency_id,
        nominal,
        value,

        CASE
            WHEN rate_date ~ '^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$'
            THEN SUBSTRING(rate_date FROM 7 FOR 4) || '-' ||
                 SUBSTRING(rate_date FROM 4 FOR 2) || '-' ||
                 SUBSTRING(rate_date FROM 1 FOR 2)
            ELSE NULL
        END AS parsed_date,

        REPLACE(value, ',', '.') AS parsed_value,
        REPLACE(nominal, ',', '.') AS parsed_nominal
    FROM raw.cbr_currency_rates
),
validated AS (
    SELECT *
    FROM prepared
    WHERE pg_input_is_valid(parsed_date, 'date')
      AND pg_input_is_valid(parsed_value, 'numeric')
      AND pg_input_is_valid(parsed_nominal, 'numeric')
),
normalized AS (
    SELECT
        parsed_date::DATE AS rate_date,
        CASE currency_id
            WHEN 'R01235' THEN 'USD'
            ELSE NULL
        END AS currency_code,
        parsed_value::NUMERIC AS rate_value,
        parsed_nominal::NUMERIC AS nominal_value
    FROM validated
),
valid_rates AS (
    SELECT
        rate_date,
        currency_code,
        rate_value / nominal_value AS rate_rub
    FROM normalized
    WHERE currency_code IS NOT NULL
      AND rate_value > 0
      AND nominal_value > 0
)
INSERT INTO core.currency_rates (rate_date, currency_code, rate_rub)
SELECT rate_date, currency_code, rate_rub
FROM valid_rates
ON CONFLICT (rate_date, currency_code)
DO UPDATE SET
    rate_rub = EXCLUDED.rate_rub
WHERE core.currency_rates.rate_rub IS DISTINCT FROM EXCLUDED.rate_rub;