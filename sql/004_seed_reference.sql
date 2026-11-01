INSERT INTO core.commodities (name, ticker, source, unit, currency)
VALUES ('Золото','GLDRUB_TOM','moex_iss', 'gram', 'RUB'),
    ('Медь','COPPER','moex_csv', 'ton', 'USD'),
    ('Алюминий','ALUM','moex_csv', 'ton', 'USD')
ON CONFLICT DO NOTHING;
