CREATE TABLE query1 AS
SELECT  
    p.Title, 
    p.Posting_location AS location, 
    p.Company_name AS company, 
    s.Max_salary, 
    s.Min_salary
FROM job_posting p
LEFT JOIN salary s 
ON s.Job_id = p.Job_id
WHERE s.Max_salary IS NOT NULL AND s.Min_salary IS NOT NULL
ORDER BY s.Max_salary DESC;

drop table query1;
