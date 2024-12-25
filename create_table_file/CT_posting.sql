create table job_posting(
    Job_id varchar(10),
    Company_name varchar(50),
    Title varchar(255),
    Posting_location varchar(255),
    Company_id varchar(10),
    Views int,
    Formatted_work_type varchar(50),
    Applies int,
    Job_posting_url varchar(255),
    primary key (Job_id)
);

LOAD DATA LOCAL INFILE './archive/postings.csv'
INTO TABLE job_posting
CHARACTER SET latin1
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES;