create table company(
    Company_id varchar(10),
    Company_name varchar(50),
    State varchar(50),
    Country varchar(50),
    City varchar(50),
    Address varchar(50),
    URL varchar(100),
    primary key(Company_id)
);

create table company_industry(
    Company_id varchar(10),
    Industry_name varchar(50),
    primary key(Company_id)
);

create table company_speciality(
    Company_id varchar(10),
    Speciality varchar(50),
    primary key(Company_id)
);

-- Delete
create table employee_count(
    Company_id varchar(10),
    Employee_count bigint,
    Follower_count bigint,
    time_recorded bigint,
    primary key(Company_id)
);

LOAD DATA LOCAL INFILE './archive/companies/company_industries.csv'
INTO TABLE company_industry
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './archive/companies/companies.csv'
INTO TABLE company
CHARACTER SET latin1
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './archive/companies/company_specialities.csv'
INTO TABLE company_speciality
CHARACTER SET latin1
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './archive/companies/employee_counts.csv'
INTO TABLE employee_count
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;