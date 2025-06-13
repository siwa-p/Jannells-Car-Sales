drop table if exists clients;
drop table if exists client_contact_status;

select * from clients;
select * from client_contact_status;

-- Show data types for columns in 'clients' table
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'clients';

-- Show data types for columns in 'client_contact_status' table
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'client_contact_status';