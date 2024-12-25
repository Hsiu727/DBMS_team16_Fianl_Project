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

select * from query2 limit 100;

drop table query2;
