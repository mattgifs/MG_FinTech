DROP TABLE if exists zillow_data;


CREATE TABLE zillow_data(
	indicator_id VARCHAR,
	region_id VARCHAR,
	date VARCHAR,
	value VARCHAR
);
----------
--remove header that was imported through the import tool (forgot to toggle Options>Header>On)
DELETE FROM zillow_data
WHERE indicator_id='indicator_id'

--add new column for unique id per row
ALTER TABLE zillow_data
ADD COLUMN index_id SERIAL;

--set new column (index_id) as the PK
ALTER TABLE zillow_data
Add PRIMARY KEY (index_id)

----------
SELECT * FROM zillow_data
LIMIT 1000

----------



--Seemingly correct way to import file using query tool, but did not work
--COPY zillow_data(indicator_id, region_id, date, value)
--FROM 'C:\Users\giffo\Desktop\FinTech\MG_Fintech\ZILLOW_DATA_962c837a6ccefddddf190101e0bafdaf.csv'
--DELIMITER ','
--CSV HEADER;


--ZILLOW_DATA_962c837a6ccefddddf190101e0bafdaf.csv