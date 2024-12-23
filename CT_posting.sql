create table job_posting(
    Job_id varchar(10),
    Company_name varchar(50),
    Title varchar(255),
    Posting_description varchar(255),
    Posting_location varchar(255),
    Company_id varchar(10),
    Views int,
    Formatted_work_type varchar(50),
    Applies int,
    Original_listed_time bigint,
    Job_posting_url varchar(255),
    Application_type varchar(20),
    Expiry bigint,
    Listed_time bigint,
    Sponsored int,
    Work_type varchar(50),
    primary key (Job_id)
);

/*
job_id,
company_name,
title,
description,
location,
company_id,
views,
formatted_work_type,
original_listed_time,
job_posting_url,
application_type,
expiry,
listed_time,
posting_domain,
sponsored,
work_type
*/

LOAD DATA LOCAL INFILE 'archive/postings.csv'
INTO TABLE job_posting
CHARACTER SET latin1
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES;