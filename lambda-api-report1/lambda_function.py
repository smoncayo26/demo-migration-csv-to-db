import json
import os
import sys
import pymysql


# data to connect to DB, previously loaded in the lambda's environment variables
user_name = os.environ["user_name"]
password = os.environ["password"]
rds_host = os.environ["rds_host"]
db_name = os.environ["db_name"]

try:
    conn = pymysql.connect(
        host=rds_host, user=user_name, passwd=password, db=db_name, connect_timeout=5
    )
except pymysql.MySQLError as e:
    print("ERROR: Unexpected error: Could not connect to MySQL instance.")
    print(e)
    sys.exit()

print("SUCCESS: Connection to RDS MySQL instance succeeded")

query = 'SELECT (select department from departments where id=department_id) "department", (select job from jobs where id=job_id) "job", SUM(CASE WHEN Q = "1" THEN 1 ELSE 0 END) Q1, SUM(CASE WHEN Q = "2" THEN 1 ELSE 0 END) Q2, SUM(CASE WHEN Q = "3" THEN 1 ELSE 0 END) Q3, SUM(CASE WHEN Q = "4" THEN 1 ELSE 0 END) Q4 FROM (SELECT * from (SELECT *,EXTRACT(YEAR FROM datetime) AS year, QUARTER( DATETIME) AS "Q" FROM hired_employees) t) bt WHERE bt.year=2021 GROUP BY department_id, job_id ORDER BY department, job'


def lambda_handler(event, context):
    cur = conn.cursor()
    cur.execute(query)
    query_results = cur.fetchall()
    print(query_results)
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(query_results, default=str),
    }
    return response
