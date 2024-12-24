CREATE TABLE industries (
    Industry_id VARCHAR(10) NOT NULL,
    Industry_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (Industry_id)
);

CREATE TABLE skills (
    Skill_addr VARCHAR(10) NOT NULL,
    Skill_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (Skill_addr)
);

LOAD DATA LOCAL INFILE './archive/mappings/industries.csv'
INTO TABLE industries
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './archive/mappings/skills.csv'
INTO TABLE skills
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES;