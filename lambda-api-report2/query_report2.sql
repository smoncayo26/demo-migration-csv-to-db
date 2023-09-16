SELECT department_id,
 (select department from departments where id=department_id) "department",
  COUNT(1) "hired"
  FROM (
 SELECT * from (SELECT *,EXTRACT(YEAR FROM datetime) AS year
  FROM hired_employees) t
 ) t
 WHERE t.year=2021
 GROUP BY department_id
 HAVING COUNT(1)>(SELECT AVG(tb.hired) FROM (SELECT COUNT(1) "hired" FROM hired_employees
GROUP BY department_id)tb)
 ORDER BY hired desc