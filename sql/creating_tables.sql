-- *TABLE CREATION*
-- - Creating the necessary tables to fulill our desired ERD
-- - Assigning primary and foreign keys
-- - Template of tables to begin inserting data from original 'client_contact_status', 'people', and 'clients' data
-- - Bundled into stored procedure, 'CreateTables', call with: 'CALL CreateTables()'

CREATE OR REPLACE PROCEDURE CreateTables()
LANGUAGE plpgsql
AS $$
BEGIN
	-- If any of these new tables already exist, drop them
	-- - This will allow for easier updates to our ERD
	DROP TABLE IF EXISTS dim_people CASCADE;
	DROP TABLE IF EXISTS dim_company CASCADE;
	DROP TABLE IF EXISTS dim_sales_rep CASCADE;
	DROP TABLE IF EXISTS fact_clients CASCADE;
	DROP TABLE IF EXISTS dim_client_contact_status CASCADE;

	-- Creating the 'dim_people' table:
	-- - Moving descriptive attributes about people, sales reps, and clients into this table
	CREATE TABLE dim_people (
		people_id SERIAL PRIMARY KEY,
		first_name VARCHAR(128),
		last_name VARCHAR(128),
		email VARCHAR(128),
		address VARCHAR(128),
		phone char(30)
	);
	
	-- Creating the 'dim_company' table
	-- - To achieve 3NF, needed to move company data into it's own table from 'clients'
	CREATE TABLE dim_company (
		company_id SERIAL PRIMARY KEY,
		company_name VARCHAR(128)
	);
	
	-- Creating the 'dim_sales_rep' table
	-- - Adding 'people_id' to this table for later joins
	CREATE TABLE dim_sales_rep (
		sales_rep_id SERIAL PRIMARY KEY,
	    name varchar(128),
		people_id integer,
		FOREIGN KEY (people_id) REFERENCES dim_people(people_id)
	);
	
	-- Creating the 'fact_clients' table: 
	-- - Moving attributes like address, email, phone to 'people' table
	-- - Adding 'people_id', 'company_id', 'sales_rep_id'; this will be our main snowflake table
	CREATE TABLE fact_clients (
	  client_id VARCHAR(128) PRIMARY KEY,
	  company_id integer,
	  name varchar(128),
	  people_id integer,
	  sales_rep_id integer,
	  FOREIGN KEY (company_id) REFERENCES dim_company(company_id),
	  FOREIGN KEY (people_id) REFERENCES dim_people(people_id),
	  FOREIGN KEY (sales_rep_id) REFERENCES dim_sales_rep(sales_rep_id)
	);
	
	-- Creating the 'dim_client_contact_status' table
	-- - Adding a 'status_id' column as the primary key and 'client_id' and 'people_id' for later joins
	-- - The type that 'can_email' and 'can_call' is double precision, maintaining this for now and will switch too boolean in cleaning script
	CREATE TABLE dim_client_contact_status (
		status_id SERIAL PRIMARY KEY,
	 	name varchar(128),
		client_id VARCHAR(128),
		people_id integer,
		can_call double precision,
		can_email double precision,
		FOREIGN KEY (people_id) REFERENCES dim_people(people_id),
		FOREIGN KEY (client_id) REFERENCES fact_clients(client_id)
	);
	
END
$$;