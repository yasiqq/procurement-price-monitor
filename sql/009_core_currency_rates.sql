CREATE TABLE IF NOT EXISTS core.currency_rates (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rate_date DATE NOT NULL,
    currency_code TEXT NOT NULL,
    rate_rub NUMERIC CHECK(rate_rub > 0) NOT NULL,

    UNIQUE(rate_date, currency_code)
);