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