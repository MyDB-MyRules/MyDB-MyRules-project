begin transaction;

drop table if exists stock_metadata cascade;
drop table if exists stock_history cascade;
drop table if exists customer cascade;
drop table if exists transaction cascade;
drop table if exists portfolio cascade;
drop table if exists userdata cascade;

create table customer (
    id varchar not null,
    name varchar not null,
    balance numeric,
    current_value numeric default 0,
    invested_amount numeric default 0,
    primary key (id)
);

create table userdata (
    id varchar not null,
    name varchar not null,
    username varchar not null,
    email varchar not null,
    password varchar not null,
    primary key (id),
    constraint fk_userdata_customer_id
    foreign key (id)
    references customer (id)
);

create table stock_metadata (
    company_name varchar not null,
    industry varchar,
    symbol varchar not null,
    isin_code varchar not null,
    price_per_share numeric,
    primary key (symbol)
);

create table transaction (
    id varchar not null,
    customer_id varchar not null,
    stock_id varchar not null,
    date date not null,
    num_shares numeric not null,
    price_per_share numeric not null,
    buy_or_sell boolean not null,
    primary key (id),
    constraint fk_transaction_stock_id
    foreign key (stock_id)
    references stock_metadata (symbol),
    constraint fk_transaction_customer_id
    foreign key (customer_id)
    references customer (id)
);

create table portfolio (
    customer_id varchar not null,
    stock_id varchar not null,
    num_shares numeric,
    invested_amount numeric,
    current_value numeric,
    primary key (customer_id, stock_id),
    constraint fk_portfolio_customer
    foreign key (customer_id)
    references customer (id),
    constraint fk_portfolio_stock
    foreign key (stock_id)
    references stock_metadata (symbol)
);

create table stock_history (
    date date not null,
    symbol varchar not null,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume numeric,
    turnover numeric,
    primary key (date, symbol),
    constraint fk_symbol_stock_metadata
    foreign key (symbol)
    references stock_metadata(symbol)
);

end transaction;
