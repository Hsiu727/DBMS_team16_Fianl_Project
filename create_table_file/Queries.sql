-- Query 1
CREATE TABLE query1 AS
SELECT  
    p.Title, p.Posting_location AS location, 
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


-- Query2
create table query2 as 
select 
    jp.Title as Title,
    jp.Company_name as Company
from job_posting jp
left join
(
    select Job_id 
    from job_skill js
    left join skills s on s.Skill_addr=js.Skill_addr
    where s.Skill_name = 'Education'
) as new_table
on jp.Job_id = new_table.Job_id;


-- 





