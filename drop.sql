begin transaction;

drop table if exists stock_metadata cascade;
drop table if exists stock_history cascade;
drop table if exists customer cascade;
drop table if exists transaction cascade;
drop table if exists portfolio cascade;
drop table if exists userdata cascade;

end transaction;
