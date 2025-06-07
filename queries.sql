-- -- create empty tables with primary keys
-- CREATE TABLE dim_clients (
--   client_id VARCHAR(128),
--   company_id SERIAL,
--   people_id SERIAL,
--   sales_rep_id SERIAL,
--   PRIMARY KEY (client_id)
-- );
-- CREATE TABLE dim_people (
-- 	people_id SERIAL,
-- 	first_name VARCHAR(128),
-- 	last_name VARCHAR(128),
-- 	email VARCHAR(128),
-- 	address VARCHAR(128),
-- 	phone char(12),
-- 	PRIMARY KEY (people_id)
-- );

-- CREATE TABLE dim_client_contact_status (
-- 	status_id SERIAL,
--  name varchar(128),
-- 	client_id VARCHAR(128),
-- 	people_id VARCHAR(128),
-- 	can_call BOOLEAN,
-- 	can_email BOOLEAN,
-- 	PRIMARY KEY (status_id)
-- );
-- CREATE TABLE dim_company (
-- 	company_id SERIAL,
-- 	company_name VARCHAR(128),
-- 	PRIMARY KEY (company_id)
-- );
	
-- CREATE TABLE dim_sales_rep (
-- 	sales_rep_id SERIAL,
--  name varchar(128),
-- 	people_id VARCHAR(128),-- only 2 have id
-- 	PRIMARY KEY (sales_rep_id)
-- );

-- Insert unique company names from the clients table into dim_company
INSERT INTO dim_company (company_name)
SELECT DISTINCT company
FROM clients;

select * from dim_company;

--  dim_people has all the columns from people and a serial people_id
INSERT INTO dim_people (first_name, last_name, email, address)
SELECT DISTINCT first_name, last_name, email, address
FROM people;

select * from dim_people;

-- sales_rep is a column in clients TABLE
-- sales_rep has full names
-- people table has first and last name
-- are sales_rep in people?

SELECT DISTINCT c.sales_rep
FROM clients c
LEFT JOIN dim_people p
    ON CONCAT(p.first_name, ' ', p.last_name) = c.sales_rep -- join on matching name
WHERE p.people_id IS not NULL; -- look for no matches

--  98 sales_rep are not in dim_people
--  only two are
-- Heather Johnson
-- Amanda Morris

-- populate dim_sales_rep from clients

insert into dim_sales_rep (name, people_id)
SELECT distinct
    c.sales_rep AS name,
    p.people_id as people_id
FROM clients c
LEFT JOIN dim_people p
    ON CONCAT(p.first_name, ' ', p.last_name) = c.sales_rep

select * from dim_sales_rep;



-- dim_client_contact_status
-- first make boolean

ALTER TABLE client_contact_status
ADD COLUMN can_email_boolean BOOLEAN,
ADD COLUMN can_call_boolean BOOLEAN;

UPDATE client_contact_status
SET can_email_boolean = CASE 
    WHEN can_email = 1 THEN TRUE
    WHEN can_email = 0 THEN FALSE
    else NULL
end;

update client_contact_status
set can_call_boolean = case
    when can_call = 1 then TRUE
    when can_call =0 then FALSE
    else NULL
end;


-- now insert into dim_client_contact_status

insert into dim_client_contact_status(
    client_id, name, people_id, can_email, can_call
)
select DISTINCT
    cc.id as client_id,
    cc.name as name,
    p.people_id as people_id,
    cc.can_email_boolean::boolean as can_email,
    cc.can_call_boolean::boolean as can_call
from client_contact_status as cc
left join dim_people p
    on concat(p.first_name, ' ', p.last_name) = cc.name

-- check
select * from dim_client_contact_status;
-- None of the people in client_contact_status are people !!
-- maybe keep the names



