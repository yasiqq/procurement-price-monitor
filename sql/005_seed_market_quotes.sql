INSERT INTO core.market_quotes(commodity_id, trade_date, price)
VALUES(1, '2026-10-28', 12500.5000)
ON CONFLICT (commodity_id, trade_date) DO NOTHING;