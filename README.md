# demo-migration-csv-to-db
Demo repository in the context of a DB migration with 3 different tables (departments, jobs, employees) , create
a local REST API that must:
1. Receive historical data from CSV files
2. Upload these files to the new DB, also create table if not exists.
3. Be able to insert batch transactions (1 up to 1000 rows) with one request.

Then, for exploring the data that was inserted in the previous section. You should create an end-point for two requirements.

Report 1. Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.

Report 2. List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).

The designed architecture is backed in AWS infraestructure using:
1. API Gateway as API REST service.
2. Three Lambda's with python code as backend.
3. RDS with MySQL as database engine.

Additionally, for this demo the API request to get report-1 and report-2 was testing with Postman. And the upload of .csv files is contemplated using Postman with each file in the body request and header: "Content-type": "multipart/form-data".


![alt text](https://github.com/smoncayo26/demo-migration-csv-to-db/blob/main/architecture.jpg?raw=true)

