# demo-migration-csv-to-db
Demo repository in the context of a DB migration with 3 different tables (departments, jobs, employees) , create
a local REST API that must:
1. Receive historical data from CSV files
2. Upload these files to the new DB
3. Be able to insert batch transactions (1 up to 1000 rows) with one request.

The designed architecture is backed in AWS infraestructure using:
1. API Gateway as API service.
2. Lambda with python code as backend code.
3. RDS with MySQL as RDS engine
Additionally, the upload of .csv files is contemplated using Postman.
