-- create empty tables with primary keys

drop table if EXISTS dim_clients;
CREATE TABLE dim_clients (
  client_id VARCHAR(128),
  company_id integer,
  name varchar(128),
  people_id integer,
  sales_rep_id integer,
  PRIMARY KEY (client_id)
);

drop table if exists dim_people;
CREATE TABLE dim_people (
	people_id SERIAL,
	first_name VARCHAR(128),
	last_name VARCHAR(128),
	email VARCHAR(128),
	address VARCHAR(128),
	phone char(12),
	PRIMARY KEY (people_id)
);

drop table if exists dim_client_contact_status;
CREATE TABLE dim_client_contact_status (
	status_id SERIAL,
 name varchar(128),
	client_id VARCHAR(128),
	people_id integer,
	can_call BOOLEAN,
	can_email BOOLEAN,
	PRIMARY KEY (status_id)
);

drop table if exists dim_company;
CREATE TABLE dim_company (
	company_id SERIAL,
	company_name VARCHAR(128),
	PRIMARY KEY (company_id)
);
	
drop table if exists dim_sales_rep;
CREATE TABLE dim_sales_rep (
	sales_rep_id SERIAL,
 name varchar(128),
	people_id integer,-- only 2 have id
	PRIMARY KEY (sales_rep_id)
);

-- Insert unique company names from the clients table 
--              into dim_company
INSERT INTO dim_company (company_name)
SELECT DISTINCT company
FROM clients;


--  dim_people has all the columns from people and a serial people_id
INSERT INTO dim_people (first_name, last_name, email, address)
SELECT DISTINCT first_name, last_name, email, address
FROM people;


-- sales_rep is a column in clients TABLE
-- sales_rep has full names
-- people table has first and last name
-- are sales_rep in people?
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
    ON CONCAT(p.first_name, ' ', p.last_name) = c.sales_rep;


-- dim_client_contact_status
-- first make boolean

-- ALTER TABLE client_contact_status
-- ADD COLUMN can_email_boolean BOOLEAN,
-- ADD COLUMN can_call_boolean BOOLEAN;

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
    on concat(p.first_name, ' ', p.last_name) = cc.name;


-- None of the people in client_contact_status are people !!
-- maybe keep the names
-- how many of clients are in people?
-- None

insert into dim_clients(
    client_id, company_id, name, people_id, sales_rep_id
)
select DISTINCT
    c.id as client_id,
    cp.company_id as company_id,
    c.name as name,
    p.people_id as people_id,
    dsr.sales_rep_id as sales_rep_id
from clients c
left join dim_people p
    on concat(p.first_name, ' ', p.last_name) = c.name
left join dim_company cp
    on cp.company_name = c.company
left join dim_sales_rep dsr
    on dsr.name = c.sales_rep;


-- No that we have the tables populated
-- We need to assign foreign keys

-- Add foreign keys to dim_clients
ALTER TABLE dim_clients
ADD CONSTRAINT fk_clients_company
    FOREIGN KEY (company_id) REFERENCES dim_company(company_id),
ADD CONSTRAINT fk_clients_people
    FOREIGN KEY (people_id) REFERENCES dim_people(people_id),
ADD CONSTRAINT fk_clients_sales_rep
    FOREIGN KEY (sales_rep_id) REFERENCES dim_sales_rep(sales_rep_id);

-- Add foreign keys to dim_client_contact_status
ALTER TABLE dim_client_contact_status
ADD CONSTRAINT fk_contact_status_client
    FOREIGN KEY (client_id) REFERENCES dim_clients(client_id),
ADD CONSTRAINT fk_contact_status_people
    FOREIGN KEY (people_id) REFERENCES dim_people(people_id);

-- Add foreign key to dim_sales_rep
ALTER TABLE dim_sales_rep
ADD CONSTRAINT fk_sales_rep_people
    FOREIGN KEY (people_id) REFERENCES dim_people(people_id);

-- lets try a join
select dsr.name as sales_rep_name, c.name as client_name, cc.can_call, cc.can_email
from dim_clients c
inner join dim_client_contact_status cc
on cc.client_id = c.client_id
inner join dim_sales_rep dsr
on dsr.sales_rep_id = c.sales_rep_id;


select * from dim_clients;
select * from clients;
select * from dim_client_contact_status;
select * from people;

-- DROP ORIGINAL TABLES
-- drop table if exists clients;
-- drop table if exists people;
-- drop table if exists client_contact_status;





