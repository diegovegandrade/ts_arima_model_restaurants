SELECT day_of_week_1,
	   round(avg(sum_visitors),2) || '%' avg_visitors 
FROM (
SELECT id,
	   date_visit,
       CASE 
  			WHEN day_of_week = 'Monday' THEN '1-Monday'
   			WHEN day_of_week = 'Tuesday' THEN '2-Tuesday'
  			WHEN day_of_week = 'Wednesday' THEN '3-Wednesday'
  			WHEN day_of_week = 'Thursday' THEN '4-Thursday'
  			WHEN day_of_week = 'Friday' THEN '5-Friday'
  			WHEN day_of_week = 'Saturday' THEN '6-Saturday'
  			WHEN day_of_week = 'Sunday' THEN '7-Sunday'
  	   end AS day_of_week_1,
       sum_visitors
FROM (
SELECT id,
	   substr(visit_datetime,7,4) || "-" || substr(visit_datetime,4,2) || "-" ||substr(visit_datetime,1,2)date_visit,
       sum(reserve_visitors)sum_visitors
FROM restaurants_visitors r
GROUP BY 1,2)d1
INNER JOIN date_info dt ON dt.calendar_date = d1.date_visit)de
GROUP BY 1
