select
    symbol
from
    stock_metadata;

with a as (
    select
        row_number() over() as index,
        close
    from
        stock_history
    where
        symbol = :s
),
b as (
    select
        a1.close as close1,
        a2.close as close2,
        a1.index
    from
        a a1,
        a a2
    where
        a1.index = a2.index -1
)
select
    index,
    close2 - close1 as return
from
    b;

select
    *
from
    Stock_history
where
    symbol = :s;

with a as (
    select
        *
    from
        stock_history
    where
        symbol = :s
),
b as (
    select
        *
    from
        stock_history
    where
        symbol = :s
)
select
    a.date,
    a.close as close1,
    b.close as close2
from
    a,
    b
where
    a.date = b.date;

select
    sum(close) / 30
from
    stock_history
where
    symbol = :s
order by
    date desc
limit
    30;

select
    *
from
    past100prices
where
    symbol = :s;

with old as (
    select
        close
    from
        stock_history
    where
        symbol = :s
        and date = :s
),
latest as (
    select
        close,
        date
    from
        stock_history
    where
        symbol = :s
    order by
        date desc
    limit
        1
)
select
    ((latest.close - old.close) / old.close) * 100 as pnl
from
    old,
    latest;

with old as (
    select
        symbol,
        close
    from
        stock_history
    where
        date = :s
),
latest as (
    select
        symbol,
        close,
        date
    from
        stock_history
    order by
        date desc
    limit
        1
), pnl as (
    select
        symbol,
        ((latest.close - old.close) / old.close) * 100 as pnl
    from
        old,
        latest
    where
        old.symbol = latest.symbol
    order by
        pnl desc
    limit
        10;

)
select
    *
from
    pnl
where
    pnl > :s;

with old as (
    select
        symbol,
        close
    from
        stock_history
    where
        date = :s
),
latest as (
    select
        symbol,
        close,
        date
    from
        stock_history
    order by
        date desc
    limit
        1
)
select
    symbol,
    ((latest.close - old.close) / old.close) * 100 as pnl
from
    old,
    latest
where
    old.symbol = latest.symbol
order by
    pnl desc
limit
    10;

SELECT
    max(id)
FROM
    Transaction;

SELECT
    *
from
    StockMetadata
where
    symbol = stock_id;

SELECT
    *
from
    Customer
where
    id = user_id;

Update
    Customer
SET
    balance = :s,
    current_value = :s,
    invested_amount = :s;

INSERT INTO
    Transaction (
        id,
        customer,
        stock,
        date,
        num_shares,
        price_per_share,
        buy_or_sell
    )
VALUES
    (:s, :s, :s, :s, :s, :s, :s);

SELECT
    *
from
    Portfolio
where
    customer = buyt.user_id
    and stock = buyt.stock_id;

UPDATE
    Portfolio
SET
    num_shares = :s,
    investes_amount = :d,
    current_value = :d
WHERE
    customer = :s
    and stock = :s;

INSERT INTO
    Derivatives (
        id,
        customer,
        stock,
        date,
        num_shares,
        price_per_share,
        buy_or_sell,
        execution_date,
        premium,
        derivative_type
    )
VALUES
    (:s, :s, :s, :s, :s, :s, :s);

INSERT INTO
    Derivatives (
        id,
        customer,
        stock,
        date,
        num_shares,
        price_per_share,
        buy_or_sell,
        execution_date,
        premium,
        derivative_type
    )
VALUES
    (:s, :s, :s, :s, :s, :s, :s);

insert into
    customer(id, name, balance)
VALUES
    (customer_id, name, init_balance);

insert into
    userdata(username, password, customer_id, name, email)
VALUES
    (username, password, customer_id, name, email);

delete from
    userdata
where
    userdata.username = username;

select
    customer_id
from
    userdata a
where
    a.username = username
    and a.password = password;