CREATE TABLE query1 AS
SELECT  
    p.Title, 
    p.Posting_location AS location, 
    p.Company_name AS company, 
    s.Max_salary, 
    s.Min_salary,
    p.Job_id,
    ss.Skill_name,
    s.Currency
FROM job_posting p
LEFT JOIN salary s ON s.Job_id = p.Job_id
LEFT JOIN job_skill js on js.Job_id = p.Job_id
LEFT JOIN skills ss on js.Skill_addr = ss.Skill_addr
WHERE s.Max_salary <> 0 
AND s.Min_salary <> 0
AND p.Company_name <> ''
AND Skill_name is not NULL
GROUP BY 
    p.Title, 
    p.Posting_location, 
    p.Company_name, 
    s.Max_salary, 
    s.Min_salary,
    p.Job_id,
    ss.Skill_name,
    s.Currency
Order by p.Views;

/*
SELECT Title
FROM query1
GROUP BY Title, location, company, Max_salary, Min_salary
HAVING COUNT(*) > 1;
*/





