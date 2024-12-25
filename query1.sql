CREATE TABLE query1 AS
SELECT  
    p.Title, 
    p.Posting_location AS location, 
    p.Company_name AS company, 
    s.Max_salary, 
    s.Min_salary,
    p.Job_id
FROM job_posting p
LEFT JOIN salary s ON s.Job_id = p.Job_id
WHERE s.Max_salary <> 0 
AND s.Min_salary <> 0
AND p.Company_name <> ''
GROUP BY 
    p.Title, 
    p.Posting_location, 
    p.Company_name, 
    s.Max_salary, 
    s.Min_salary,
    p.Job_id;

/*
SELECT Title
FROM query1
GROUP BY Title, location, company, Max_salary, Min_salary
HAVING COUNT(*) > 1;
*/





