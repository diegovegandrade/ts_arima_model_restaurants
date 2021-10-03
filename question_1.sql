WITH holiday AS( 
SELECT calendar_date
FROM date_info dt
WHERE holiday_flg = 1),
rest as 
(
SELECT id,
	   substr(visit_datetime,7,4) || "-" || substr(visit_datetime,4,2) || "-" ||substr(visit_datetime,1,2) as visit_datetime_1,
       sum(reserve_visitors)sum_num_visitors
FROM restaurants_visitors
GROUP BY 1,2
),
store AS
(
  SELECT *
  FROM store_info
)
SELECT dfinal.id,
	   dfinal.genre_name,
       round(dfinal.avg_per_rest,2)avg_per_rest
FROM (
SELECT r2.id,
	   st.genre_name,
       avg(sum_num_visitors)avg_per_rest
FROM rest r2
INNER JOIN holiday h ON r2.visit_datetime_1 = h.calendar_date
INNER JOIN store st ON st.store_id = r2.id
GROUP BY 1,2)dfinal
ORDER BY 3 DESC
LIMIT 5;
