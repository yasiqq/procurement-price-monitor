ALTER TABLE raw.market_quotes
ADD CONSTRAINT uq_raw_market_quotes_ticker_date
UNIQUE (ticker, trade_date);