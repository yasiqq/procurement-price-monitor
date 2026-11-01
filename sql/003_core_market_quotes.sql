CREATE TABLE IF NOT EXISTS core.market_quotes (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    commodity_id INTEGER NOT NULL REFERENCES core.commodities(id),
    trade_date DATE NOT NULL,
    price NUMERIC(18, 4) NOT NULL,

    UNIQUE (commodity_id, trade_date)
);