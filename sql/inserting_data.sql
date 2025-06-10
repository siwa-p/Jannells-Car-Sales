-- *DATA INSERTION*
-- - Inserting data from original data sources extracted via Python: 'client_contact_status', 'clients', and 'people'

CREATE OR REPLACE PROCEDURE InsertDataFromSources()
LANGUAGE plpgsql
AS $$
BEGIN

	-- Inserting the distinct company names from original 'clients' table into new 'dim_company' table
	INSERT INTO dim_company (company_name)
	SELECT DISTINCT company
	FROM clients;
	
	-- Inserting descriptive attributes from original 'clients' table into new 'dim_people' table
	INSERT INTO dim_people (first_name, last_name, email, address)
	SELECT DISTINCT first_name, last_name, email, address
	FROM people;
	
	-- Inserting the sales rep's names from original 'clients' table into new 'dim_sales_rep' table
	INSERT INTO dim_sales_rep (name, people_id)
	SELECT DISTINCT
	    c.sales_rep AS name,
	    p.people_id AS people_id
	FROM clients c
	LEFT JOIN dim_people p
	    ON CONCAT(p.first_name, ' ', p.last_name) = c.sales_rep;
	
	-- Inserting data from original 'clients' table into new 'fact_clients' table
	-- - Joining people to populate the 'people_id' column if there are already clients in the 'dim_people' table
	INSERT INTO fact_clients (
	    client_id, company_id, name, people_id, sales_rep_id
	)
	SELECT DISTINCT
	    c.id AS client_id,
	    cp.company_id AS company_id,
	    c.name AS name,
	    p.people_id AS people_id,
	    dsr.sales_rep_id AS sales_rep_id
	FROM clients c
	LEFT JOIN dim_people p
	    ON concat(p.first_name, ' ', p.last_name) = c.name
	LEFT JOIN dim_company cp
	    ON cp.company_name = c.company
	LEFT JOIN dim_sales_rep dsr
	    ON dsr.name = c.sales_rep;
		
	-- Inserting data from original 'client_contact_status' into new 'dim_client_contact_status' table
	-- - Joining people to populate the 'people_id' if they already exist in the 'dim_people' table
	INSERT INTO dim_client_contact_status(
	    client_id, name, people_id, can_email, can_call
	)
	SELECT DISTINCT
	    cc.id AS client_id,
	    cc.name AS name,
	    p.people_id AS people_id,
	    cc.can_email AS can_email,
	    cc.can_call AS can_call
	FROM client_contact_status AS cc
	LEFT JOIN dim_people p
	    ON concat(p.first_name, ' ', p.last_name) = cc.name;

END
$$;