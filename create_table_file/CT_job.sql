create table benefits(
    Job_id varchar(255),
    Inferred int,
    Job_type varchar(255)
);

create table job_industry(
    Job_id varchar(10),
    Industry_id varchar(4),
    primary key(Job_id,Industry_id)
);

create table job_skill(
    Job_id varchar(10),
    Skill_addr varchar(5),
    primary key(Job_id)
);

create table salary(
    Salary_id int,
    Job_id varchar(10),
    Max_salary DOUBLE,
    Med_salary DOUBLE,
    Min_salary DOUBLE,
    Pay_period varchar(10),
    Currency varchar(10),
    Compensation_type varchar(20)
);

LOAD DATA LOCAL INFILE './archive/jobs/benefits.csv'
INTO TABLE benefits
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './archive/jobs/job_industries.csv'
INTO TABLE job_industry
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES;


LOAD DATA LOCAL INFILE './archive/jobs/job_skills.csv'
INTO TABLE job_skill
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './archive/jobs/salaries.csv'
INTO TABLE salary
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES;