SELECT 
  (select department from departments where id = department_id) "department", 
  (select job from jobs where id = job_id) "job", 
  SUM(CASE WHEN Q = "1" THEN 1 ELSE 0 END) Q1, 
  SUM(CASE WHEN Q = "2" THEN 1 ELSE 0 END) Q2, 
  SUM(CASE WHEN Q = "3" THEN 1 ELSE 0 END) Q3, 
  SUM(CASE WHEN Q = "4" THEN 1 ELSE 0 END) Q4 
FROM 
(SELECT * from (SELECT *,
EXTRACT(YEAR FROM datetime) AS YEAR,
QUARTER( DATETIME) AS "Q" FROM hired_employees) t) bt 
WHERE 
  bt.year = 2021 
GROUP BY 
  department_id, job_id 
ORDER BY 
  department, job