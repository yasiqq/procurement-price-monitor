CREATE TABLE IF NOT EXISTS raw.moex_csv_quotes (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticker TEXT NOT NULL,
    per TEXT,
    trade_date TEXT NOT NULL,
    trade_time TEXT,
    price_open TEXT,
    price_high TEXT,
    price_low TEXT,
    price_close TEXT NOT NULL,
    VOL TEXT,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (ticker, trade_date)
);
