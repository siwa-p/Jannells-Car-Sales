-- *TABLE OVERVIEW*

-- Creates tables with primary/composite keys that are pepared for data insertion
CALL CreateTables();
-- Inserts raw data from 'client_contact_status', 'clients', and 'people' into newly created tables
CALL InsertDataFromSources();
-- Performs any neccessary data cleaning/transformation before constructing final view
CALL PerformDataCleaning();


-- All tables joined with relevant fields for business objectives to query from
CREATE OR REPLACE VIEW client_contact_status_view AS (
	SELECT 
		CONCAT(dp.first_name, ' ', dp.last_name) AS Client_Name,
		dc.company_name AS Company_Name,
		CONCAT(dsr.first_name, ' ', dsr.last_name) AS Sales_Rep_Name,
		dccs.can_call AS Client_Phone_Permission,
		dp.phone AS Client_Phone,
		dccs.can_email AS Client_Email_Permission,
		dp.email AS Client_Email
		FROM fact_clients fc
		LEFT JOIN dim_people dp ON fc.people_id = dp.people_id
		LEFT JOIN dim_company dc ON fc.company_id = dc.company_id
		LEFT JOIN dim_sales_rep dsr ON fc.sales_rep_id = dsr.sales_rep_id
		LEFT JOIN dim_client_contact_status dccs ON fc.client_id = dccs.client_id
);

-- Resulting view to query from for CSV
-- SELECT * FROM client_contact_status_view;

-- Clients who can be called:
-- SELECT client_name, company_name, sales_rep_name, client_email_permission, client_email
-- FROM client_contact_status_view 
-- WHERE client_email_permission = FALSE;

-- SELECT * 
-- FROM INFORMATION_SCHEMA.COLUMNS
-- WHERE TABLE_NAME IN (
-- 	'dim_clients', 
-- 	'dim_client_contact_status', 
-- 	'dim_company',
-- 	'dim_people',
-- 	'dim_sales_rep'
-- )
-- ORDER BY table_name DESC;


DROP VIEW IF EXISTS original_clients;
CREATE OR REPLACE VIEW original_clients AS (
	SELECT
		fc.client_id AS id,
		dc.company_name AS company,
		CONCAT(dp.first_name, ' ', dp.last_name) AS name,
		dp.address AS address,
		dp.email AS email,
		dp.phone AS phone,
		CONCAT(dsr.first_name, ' ', dsr.last_name) AS sales_rep
		FROM fact_clients fc
		LEFT JOIN dim_people dp ON fc.people_id = dp.people_id
		LEFT JOIN dim_company dc ON fc.company_id = dc.company_id
		LEFT JOIN dim_sales_rep dsr ON fc.sales_rep_id = dsr.sales_rep_id
		LEFT JOIN dim_client_contact_status dccs ON fc.client_id = dccs.client_id
);

-- select * from original_clients;
-- select * from clients;
