CREATE OR REPLACE PROCEDURE PerformDataCleaning()
LANGUAGE plpgsql 
AS $$
BEGIN

	-- Converting 'dim_client_contact_status' can_email/call fields from 1s and 0s (double precision) to boolean
	-- - Have to cast to boolean for this to work
	ALTER TABLE dim_client_contact_status
	ALTER COLUMN can_email TYPE BOOLEAN USING (
		CASE 
			WHEN can_email = 1.0 THEN TRUE
			WHEN can_email = 0.0 THEN FALSE
			ELSE NULL
		END);

	ALTER TABLE dim_client_contact_status
	ALTER COLUMN can_call TYPE BOOLEAN USING (
		CASE
			WHEN can_call = 1.0 THEN TRUE
			WHEN can_call = 0.0 THEN FALSE
			ELSE NULL
		END);

	
	-- Splitting the 'name' column in 'fact_clients' into 'first_name' and 'last_name', and inserting them into the 'people' table
	-- - Adding a first name & last name column to clients
	ALTER TABLE fact_clients
	ADD first_name varchar(255),
	ADD last_name varchar(255);
	
	-- - Selecting the substring of name before the space (' ') to get the first name
	UPDATE fact_clients
	SET first_name = (SELECT SUBSTRING(name, 1, STRPOS(name, ' ') - 1));
	
	-- - Selecting the substring of name after the space (' ') to get the last name
	UPDATE fact_clients
	SET last_name = (SELECT SUBSTRING(name, STRPOS(name, ' ') + 1));
	
	--  - Removing the original name column from clients, redundant
	ALTER TABLE fact_clients
	DROP COLUMN name;
	
	--  - Now that the name column is split, insert all clients into the people table
	INSERT INTO dim_people (first_name, last_name)
	SELECT DISTINCT first_name, last_name
	FROM fact_clients;

	--  - Setting the people_id of CLIENTS equal to the people_id of PEOPLE that was generated after the insert via SERIAL
	UPDATE fact_clients AS fc
	SET people_id = dp.people_id
	FROM dim_people as dp
	WHERE dp.first_name = fc.first_name
	AND dp.last_name = fc.last_name;

	-- - Dropping the first and last names from clients, will retrieve from people
	ALTER TABLE fact_clients
	DROP first_name, 
	DROP last_name;
		
	-- Repeating the same process for sales reps
	-- - Adding a first name & last name column to 'dim_sales_reps'
	ALTER TABLE dim_sales_rep
	ADD first_name varchar(255),
	ADD last_name varchar(255);
	
	-- - Selecting the substring of name before the space (' ') to get the first name
	UPDATE dim_sales_rep
	SET first_name = (SELECT SUBSTRING(name, 1, STRPOS(name, ' ') - 1));
	
	-- - Selecting the substring of name after the space (' ') to get the last name
	UPDATE dim_sales_rep
	SET last_name = (SELECT SUBSTRING(name, STRPOS(name, ' ') + 1));
	
	--  - Removing the original name column from clients, redundant
	ALTER TABLE dim_sales_rep
	DROP COLUMN name;
	
	--  - Now that the name column is split, insert all clients into the people table
	INSERT INTO dim_people (first_name, last_name)
	SELECT DISTINCT first_name, last_name
	FROM dim_sales_rep;
	
	--  - Setting the people_id of CLIENTS equal to the people_id of PEOPLE that were generated after the insert via SERIAL
	UPDATE dim_sales_rep AS sr
	SET people_id = dp.people_id
	FROM dim_people as dp
	WHERE dp.first_name = sr.first_name
	AND dp.last_name = sr.last_name;

	-- - Setting the people_id of CLIENT_CONTACT_STATUS equal to the people_id of PEOPLE that were generated after insert via SERIAL
	-- - - Because we added people_id to this table (since all appear in people), needed to fill in their people id as well
	UPDATE dim_client_contact_status AS ccs
	SET people_id = dp.people_id
	FROM dim_people as dp
	WHERE CONCAT(dp.first_name, ' ', dp.last_name) = ccs.name;

	-- Last thing to do is add the address, email, and phones of clients to the people table
	UPDATE dim_people AS dp
	SET 
		address = c.address,
		email = c.email,
		phone = c.phone
	FROM clients as c
	WHERE CONCAT(dp.first_name, ' ', dp.last_name) = c.name;

	-- Fixing phone number formatting in dim_people
	-- UPDATE dim_people
	-- SET phone = LEFT(phone, STRPOS('x', phone) - 1);
	
	UPDATE dim_people
	SET phone = REPLACE(phone, '.', '');
	
END
$$;
