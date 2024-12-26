set global local_infile = true;

create database final_project;
use final_project;

source ./create_table_file/CT_company.sql;
source ./create_table_file/CT_job.sql;
source ./create_table_file/CT_mapping.sql;
source ./create_table_file/CT_posting.sql;
source ./create_table_file/Account.sql;
source ./create_table_file/Queries.sql;
source ./create_table_file/manager.sql;
source ./create_table_file/Shopping_cart.sql;