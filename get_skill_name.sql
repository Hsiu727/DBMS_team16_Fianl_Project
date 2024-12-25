create table skill_dictionary as 
select Distinct s.Skill_name as Name
from job_skill js
left join skills s on s.Skill_addr = js.Skill_addr
order by Name;
