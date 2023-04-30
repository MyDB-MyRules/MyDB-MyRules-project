drop trigger if exists add_to_portfolio on customer;

CREATE TRIGGER add_to_portfolio
  after insert
  ON customer
  FOR EACH ROW
  EXECUTE PROCEDURE log();