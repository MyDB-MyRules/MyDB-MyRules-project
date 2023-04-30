begin transaction;

drop table if exists stock_metadata cascade;
drop table if exists stock_history cascade;
drop table if exists customer cascade;
drop table if exists transaction cascade;
drop table if exists portfolio cascade;
drop table if exists userdata cascade;
drop table if exists derivatives cascade;

create table customer (
    id varchar not null,
    name varchar not null,
    balance numeric,
    current_value numeric default 0,
    invested_amount numeric default 0,
    primary key (id)
);

create table userdata (
    customer_id varchar not null,
    name varchar not null,
    username varchar not null,
    email varchar not null,
    password varchar not null,
    primary key (username),
    constraint fk_userdata_customer_id
    foreign key (customer_id)
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
    buyer_id varchar not null,
    seller_id varchar not null,
    stock_id varchar not null,
    date date not null,
    num_shares numeric not null,
    price_per_share numeric not null,
    constraint fk_transaction_stock_id
    foreign key (stock_id)
    references stock_metadata (symbol),
    constraint fk_transaction_buyer_id
    foreign key (buyer_id)
    references customer (id),
    constraint fk_transaction_seller_id
    foreign key (seller_id)
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

create table derivatives (
    id varchar not null,
    buyer_id varchar not null,
    seller_id varchar not null,
    stock_id varchar not null,
    date date not null,
    num_shares numeric not null,
    price_per_share numeric not null,
    execution_time numeric not null,
    premium numeric default 0,
    derivative_type varchar not null,
    primary key(id),
    constraint fk_derivatives_stock_id
    foreign key (stock_id)
    references stock_metadata (symbol),
    constraint fk_derivatives_buyer_id
    foreign key (buyer_id)
    references customer (id),
    constraint fk_derivatives_seller_id
    foreign key (seller_id)
    references customer (id)
);


drop index if exists idx_userdata;
drop index if exists idx_stock_history;
drop index if exists idx_stock_metadata;
drop index if exists idx_transaction;
drop index if exists idx_portfolio;

create index idx_userdata on userdata(username, password);
create index idx_stock_history on stock_history(date, symbol);
create index idx_stock_metadata on stock_metadata(symbol);
create index idx_transaction on transaction(id);
create index idx_portfolio on portfolio(stock_id);

create
or replace function log() returns trigger language plpgsql as 
$$ begin
insert into portfolio values(new.id, 'ADANIPORTS', 0, 0, 0);
insert into portfolio values(new.id, 'ASIANPAINT', 0, 0, 0);
insert into portfolio values(new.id, 'AXISBANK', 0, 0, 0);
insert into portfolio values(new.id, 'BAJAJAUTO', 0, 0, 0);
insert into portfolio values(new.id, 'BAJAJFINSV', 0, 0, 0);
insert into portfolio values(new.id, 'BAJFINANCE', 0, 0, 0);
insert into portfolio values(new.id, 'BHARTIARTL', 0, 0, 0);
insert into portfolio values(new.id, 'BPCL', 0, 0, 0);
insert into portfolio values(new.id, 'BRITANNIA', 0, 0, 0);
insert into portfolio values(new.id, 'CIPLA', 0, 0, 0);
insert into portfolio values(new.id, 'COALINDIA', 0, 0, 0);
insert into portfolio values(new.id, 'DRREDDY', 0, 0, 0);
insert into portfolio values(new.id, 'EICHERMOT', 0, 0, 0);
insert into portfolio values(new.id, 'GAIL', 0, 0, 0);
insert into portfolio values(new.id, 'GRASIM', 0, 0, 0);
insert into portfolio values(new.id, 'HCLTECH', 0, 0, 0);
insert into portfolio values(new.id, 'HDFC', 0, 0, 0);
insert into portfolio values(new.id, 'HDFCBANK', 0, 0, 0);
insert into portfolio values(new.id, 'HEROMOTOCO', 0, 0, 0);
insert into portfolio values(new.id, 'HINDALCO', 0, 0, 0);
insert into portfolio values(new.id, 'HINDUNILVR', 0, 0, 0);
insert into portfolio values(new.id, 'ICICIBANK', 0, 0, 0);
insert into portfolio values(new.id, 'INDUSINDBK', 0, 0, 0);
insert into portfolio values(new.id, 'INFRATEL', 0, 0, 0);
insert into portfolio values(new.id, 'INFY', 0, 0, 0);
insert into portfolio values(new.id, 'IOC', 0, 0, 0);
insert into portfolio values(new.id, 'ITC', 0, 0, 0);
insert into portfolio values(new.id, 'JSWSTEEL', 0, 0, 0);
insert into portfolio values(new.id, 'KOTAKBANK', 0, 0, 0);
insert into portfolio values(new.id, 'LT', 0, 0, 0);
insert into portfolio values(new.id, 'M&M', 0, 0, 0);
insert into portfolio values(new.id, 'MARUTI', 0, 0, 0);
insert into portfolio values(new.id, 'NESTLEIND', 0, 0, 0);
insert into portfolio values(new.id, 'NTPC', 0, 0, 0);
insert into portfolio values(new.id, 'ONGC', 0, 0, 0);
insert into portfolio values(new.id, 'POWERGRID', 0, 0, 0);
insert into portfolio values(new.id, 'RELIANCE', 0, 0, 0);
insert into portfolio values(new.id, 'SBIN', 0, 0, 0);
insert into portfolio values(new.id, 'SHREECEM', 0, 0, 0);
insert into portfolio values(new.id, 'SUNPHARMA', 0, 0, 0);
insert into portfolio values(new.id, 'TATAMOTORS', 0, 0, 0);
insert into portfolio values(new.id, 'TATASTEEL', 0, 0, 0);
insert into portfolio values(new.id, 'TCS', 0, 0, 0);
insert into portfolio values(new.id, 'TECHM', 0, 0, 0);
insert into portfolio values(new.id, 'TITAN', 0, 0, 0);
insert into portfolio values(new.id, 'ULTRACEMCO', 0, 0, 0);
insert into portfolio values(new.id, 'UPL', 0, 0, 0);
insert into portfolio values(new.id, 'VEDL', 0, 0, 0);
insert into portfolio values(new.id, 'WIPRO', 0, 0, 0);
insert into portfolio values(new.id, 'ZEEL', 0, 0, 0);
return null;
end 
$$;

drop trigger if exists add_to_portfolio on customer;

CREATE TRIGGER add_to_portfolio
  after insert
  ON customer
  FOR EACH ROW
  EXECUTE PROCEDURE log();


end transaction;
