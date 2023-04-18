create materialized view past100prices as 
(
SELECT
  * 
FROM (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date desc) AS r,
    t.*
  FROM
    stock_history t) x
WHERE
  x.r <= 100
);