SELECT weeks,
	 n_s,
     round(ifNULL((n_s - Original_number)/Original_number*100,0),2) || '%' percentage_growth
FROM (
SELECT weeks,
	   CAST(n_s AS FLOAT)n_s,
       CAST(LAG(n_s,1,0) OVER ( ORDER BY weeks) AS FLOAT) Original_number
FROM (
SELECT CASE 
  			WHEN daytime BETWEEN '01' AND '07' THEN 'Week 1'
   			WHEN daytime BETWEEN '08' AND '14' THEN 'Week 2'
  			WHEN daytime BETWEEN '15' AND '21' THEN 'Week 3'
  			WHEN daytime BETWEEN '22' AND '31' THEN 'Week 4'
 	   END weeks,
  	   sum(reserve_visitors)n_s
FROM (
SELECT strftime('%d',substr(visit_datetime,7,4) || "-" || substr(visit_datetime,4,2) || "-" ||substr(visit_datetime,1,2))daytime,
	   sum(reserve_visitors)reserve_visitors
FROM restaurants_visitors r
WHERE substr(visit_datetime,7,4) || "-" || substr(visit_datetime,4,2) || "-" ||substr(visit_datetime,1,2)  >= '2017-05-01'
GROUP BY 1 )dates
GROUP bY 1)dd )dfinal
