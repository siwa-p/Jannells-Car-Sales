-- *TABLE OVERVIEW*

-- Creates tables with primary/composite keys that are pepared for data insertion
CALL CreateTables();
-- Inserts raw data from 'client_contact_status', 'clients', and 'people' into newly created tables
CALL InsertDataFromSources();
-- Performs any neccessary data cleaning/transformation before constructing final view
CALL PerformDataCleaning();

-- Resulting view to query from for CSV
SELECT * FROM client_contact_status_view;
-- Clients who can be called:
SELECT client_name, company_name, sales_rep_name, client_email_permission, client_email
FROM client_contact_status_view 
WHERE client_email_permission = FALSE;

SELECT * 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN (
	'dim_clients', 
	'dim_client_contact_status', 
	'dim_company',
	'dim_people',
	'dim_sales_rep'
)
ORDER BY table_name DESC;