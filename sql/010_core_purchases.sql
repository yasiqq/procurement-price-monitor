CREATE TABLE IF NOT EXISTS core.purchases (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_id INTEGER REFERENCES core.suppliers(id) NOT NULL,
    commodity_id INTEGER REFERENCES core.commodities(id) NOT NULL,
    purchase_date DATE NOT NULL,
    quantity NUMERIC CHECK (quantity > 0) NOT NULL,
    unit_price NUMERIC CHECK (unit_price > 0) NOT NULL,
    currency TEXT CHECK (currency IN ('RUB', 'USD')) NOT NULL,
    transport_cost NUMERIC CHECK (transport_cost >= 0) NOT NULL,
    insurance_cost NUMERIC CHECK (insurance_cost >= 0) NOT NULL
);