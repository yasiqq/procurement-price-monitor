create or replace view mart.purchase_analytics as (
    with purchase_prices as (
        -- цены за единицу сырья в рублях
        select p.id as purchase_id, p.purchase_date, s.name as supplier_name, c.name as commodity_name, p.quantity, p.unit_price, market_quote.trade_date AS market_date, market_quote.price AS market_price, currency_rate.rate_date AS exchange_rate_date, currency_rate.rate_rub AS exchange_rate,
            p.currency AS purchase_currency, c.currency AS market_currency, c.unit AS commodity_unit, p.transport_cost, p.insurance_cost,

            case
                when p.currency = 'RUB' then p.unit_price
                when p.currency = 'USD' then p.unit_price * currency_rate.rate_rub
            end as purchase_unit_price_rub,

            case
                when c.currency = 'RUB' then market_quote.price
                when c.currency = 'USD' then market_quote.price * currency_rate.rate_rub
            end as market_unit_price_rub

        from core.purchases as p

        join core.suppliers as s
            on p.supplier_id = s.id
        join core.commodities as c
            on p.commodity_id = c.id

        left join lateral  (
        select
            mq.commodity_id,
            mq.trade_date,
            mq.price
        from core.market_quotes as mq
        where mq.commodity_id = p.commodity_id and
            mq.trade_date <= p.purchase_date
        order by mq.trade_date desc limit 1
    ) as market_quote on true

        left join lateral (
        select
            cr.rate_date,
            cr.currency_code,
            cr.rate_rub
        from core.currency_rates as cr
        where cr.currency_code = 'USD' and
            cr.rate_date <= p.purchase_date
        order by cr.rate_date desc limit 1
    ) as currency_rate on true
    ),
        purchase_costs as (
        -- расчёт стоимости сырья и полной стоимости закупки
            select
                *,
                round(quantity * purchase_unit_price_rub, 2) as goods_cost_rub,
                round(quantity * market_unit_price_rub, 2) as market_cost_rub,
                round(
                    quantity * purchase_unit_price_rub
                    + transport_cost
                    + insurance_cost,
                    2
                ) as total_cost_rub
            from purchase_prices
    )
    select
        *,
        round(goods_cost_rub - market_cost_rub, 2) as price_deviation_rub,
        round((goods_cost_rub - market_cost_rub) / nullif(market_cost_rub, 0) * 100, 2) as price_deviation_pct,
        round(total_cost_rub - market_cost_rub, 2) as total_deviation_rub,
        round((total_cost_rub - market_cost_rub) / nullif(market_cost_rub, 0) * 100, 2) as total_deviation_pct
    from purchase_costs
);