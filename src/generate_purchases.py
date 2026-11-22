from db import get_connection
import random
from decimal import Decimal



def get_market_quotes(cur):
    query = '''
        select m.commodity_id, m.trade_date, m.price, c.currency, c.unit, c.ticker                        
        from core.market_quotes as m
        join core.commodities as c
        on m.commodity_id = c.id
    '''

    cur.execute(query)

    rows = cur.fetchall()
    return rows

def get_suppliers(cur):
    query = '''
        select id, name                   
        from core.suppliers
    '''

    cur.execute(query)

    rows = cur.fetchall()
    return rows

def generate_quantity(unit):
    # генерация случайного веса
    if unit == 'gram':
        return random.randint(100, 2000)
    elif unit == 'ton':
        return random.randint(10, 100)
    else:
        raise ValueError(f"Unknown unit: {unit}")

def generate_unit_price(supplier_name, market_price):
    # генерация закупочной цены
    dict_markups = {
        "Альфа Металл": (1, 4),
        "ПромРесурс": (10, 18),
        "СеверСнаб": (-2, 3),
        "ТехМеталл": (-5, 20),
        "Глобал Сырье": (4, 10)
    }

    if supplier_name in dict_markups:
        low, high = dict_markups[supplier_name]
        markup = random.randint(low, high)

        unit_price = market_price * (1 + Decimal(markup) / Decimal(100))

        return unit_price
    else:
        raise ValueError(f"Unknown supplier_name: {supplier_name}")

def generate_transport_cost(supplier_name, unit, quantity):
    # генерация стоимости транспортировки
    transport_tariffs = {
        "Альфа Металл": {
            "ton": (40000, 70000),
            "gram": (60, 100)
        },
        "ПромРесурс": {
            "ton": (5000, 15000),
            "gram": (10, 30)
        },
        "СеверСнаб": {
            "ton": (15000, 30000),
            "gram": (30, 60)
        },
        "ТехМеталл": {
            "ton": (5000, 80000),
            "gram": (10, 120)
        },
        "Глобал Сырье": {
            "ton": (25000, 50000),
            "gram": (40, 80)
        }
    }

    if supplier_name in transport_tariffs:
        q = transport_tariffs[supplier_name]
        if unit in q:
            low, high = q[unit]
            price = random.randint(low, high)
            transport_cost = price * quantity
        else:
            raise ValueError(f"Unknown unit: {unit}")

        return transport_cost
    else:
        raise ValueError(f"Unknown supplier_name: {supplier_name}")

def generate_insurance_cost(ticker, quantity, unit_price, exchange_rate):
    # страхование груза
    insurance_rates = {
        "GLDRUB_TOM": (20, 80),
        "COPPER": 	(10, 30),
        "ALUM": (10, 30)
    }


    if ticker in insurance_rates:
        low, high = insurance_rates[ticker]
        rate = Decimal(random.randint(low, high)) / Decimal(10000)
        final_cost = quantity * unit_price * exchange_rate
        insurance_cost = final_cost * rate
        return insurance_cost.quantize(Decimal("0.01"))
    else:
        raise ValueError(f"{ticker}")

def get_exchange_rate(cur, trade_date, currency):
    # получение курса валюты
    query = '''
        select rate_rub FROM core.currency_rates
        where currency_code = 'USD' and rate_date <= %s
        order by rate_date
        desc
        limit 1
    '''

    currency = currency.upper()
    if currency == 'RUB':
        return Decimal(1)
    elif currency == 'USD':
        cur.execute(query, (trade_date,))
        trade_currency = cur.fetchone()
        if trade_currency is None:
            raise ValueError(f"No suitable date found {trade_date}")
        else:
            return trade_currency[0]
    else:
        raise ValueError(f"Unsupported currency type {currency}")

def generate_purchases(cur, market_quotes, suppliers, count):
    # генерация закупок
    res = []

    for _ in range(count):
        random_mq = random.choice(market_quotes)
        random_s = random.choice(suppliers)

        commodity_id, trade_date, market_price, currency, unit, ticker = random_mq
        supplier_id, supplier_name = random_s

        quantity = generate_quantity(unit)
        unit_price = generate_unit_price(supplier_name, market_price)
        transport_cost = generate_transport_cost(supplier_name, unit, quantity)
        exchange_rate = get_exchange_rate(cur, trade_date, currency)
        insurance_cost = generate_insurance_cost(ticker, quantity, unit_price, exchange_rate)

        purchases = {
            "supplier_id": supplier_id,
            "commodity_id": commodity_id,
            "purchase_date": trade_date,
            "currency": currency,
            "unit_price": unit_price,
            "transport_cost": transport_cost,
            "insurance_cost": insurance_cost,
            "quantity": quantity
        }

        res.append(purchases)

    return res

def insert_purchases(cur, purchases):
    query = '''
        INSERT INTO core.purchases (supplier_id, commodity_id, purchase_date, quantity, unit_price, currency, transport_cost, insurance_cost)
        VALUES (%(supplier_id)s, %(commodity_id)s, %(purchase_date)s, %(quantity)s, %(unit_price)s, %(currency)s, %(transport_cost)s, %(insurance_cost)s)
    '''

    cur.executemany(query, purchases)
    cnt = cur.rowcount

    return cnt

def purchases_exists(cur):
    query = '''
        select exists (select 1 from core.purchases)
    '''
    cur.execute(query)

    return cur.fetchone()[0]

def main():
    random.seed(42)
    with get_connection() as conn:
        with conn.cursor() as cur:
            market_quotes = get_market_quotes(cur)
            suppliers = get_suppliers(cur)

            if not purchases_exists(cur):
                purchases = generate_purchases(cur, market_quotes, suppliers, 3000)
                cnt = insert_purchases(cur, purchases)
                print(f"Purchases inserted: {cnt}")
            else:
                print(f"Purchases already exist. Skipping generation")



main()