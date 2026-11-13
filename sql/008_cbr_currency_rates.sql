CREATE TABLE IF NOT EXISTS raw.cbr_currency_rates (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rate_date TEXT NOT NULL,
    currency_id TEXT NOT NULL,
    nominal TEXT,
    value TEXT,
    vunit_rate TEXT,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (rate_date, currency_id)
);