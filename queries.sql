-- create empty tables with primary keys
CREATE TABLE dim_clients (
  client_id VARCHAR,
  company_id SERIAL,
  people_id SERIAL,
  sales_rep_id SERIAL,
  PRIMARY KEY (client_id)
);
CREATE TABLE dim_people (
	people_id SERIAL,
	first_name VARCHAR,
	last_name VARCHAR,
	email VARCHAR,
	address VARCHAR,
	phone VARCHAR,
	PRIMARY KEY (people_id)
);
CREATE TABLE dim_client_contact_status (
	status_id SERIAL,
	client_id VARCHAR,
	people_id VARCHAR,
	can_call BOOLEAN,
	can_email BOOLEAN,
	PRIMARY KEY (status_id)
);
CREATE TABLE dim_company (
	company_id SERIAL,
	company_name VARCHAR,
	PRIMARY KEY (company_id)
);
	
CREATE TABLE dim_sales_rep (
	sales_rep_id SERIAL,
	people_id VARCHAR,
	PRIMARY KEY (sales_rep_id)
);