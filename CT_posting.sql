create table job_posting(
    Job_id varchar(10),
    Company_name varchar(50),
    Title varchar(255),
    Description varchar(255),
    Max_salary int,
    Pay_period varchar(50),
    Location varchar(255),
    Company_id varchar(10),
    Views int,
    Med_salary int,
    Min_salary int,
    Formatted_work_type varchar(50),
    Applies int,
    Original_listed_time bigint,
    Remote_allowed bigint,
    Job_posting_url varchar(255),
    Application_url varchar(255),
    Application_type varchar(20),
    Expiry bigint,
    Closed_time bigint,
    Formatted_experience_level varchar(255),
    Skills_desc varchar(50),
    Listed_time bigint,
    Posting_domain varchar(50),
    Sponsored int,
    Work_type varchar(50),
    Currency varchar(50),
    Compensation_type varchar(50),
    Normalized_salary int,
    Zip_code int,
    Fips int,
    primary key (Job_id)
);

LOAD DATA LOCAL INFILE './archive/postings.csv'
INTO TABLE job_posting
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES;