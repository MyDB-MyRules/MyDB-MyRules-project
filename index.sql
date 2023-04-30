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


