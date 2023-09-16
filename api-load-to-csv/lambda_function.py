import json
import base64
import sys
import os
import pymysql

# data to connect to DB, previously loaded in the lambda's environment variables
user_name = os.environ["user_name"]
password = os.environ["password"]
rds_host = os.environ["rds_host"]
db_name = os.environ["db_name"]

# code to connect to DB
try:
    conn = pymysql.connect(
        host=rds_host, user=user_name, passwd=password, db=db_name, connect_timeout=5
    )
except pymysql.MySQLError as e:
    print("ERROR: Unexpected error: Could not connect to MySQL instance.")
    print(e)
    sys.exit()

print("SUCCESS: Connection to RDS MySQL instance succeeded")


# function to create tables if not exist, load data, and drop 3 tables
def addData(output, table_name):
    i = 0
    data = output
    dict_tables = {
        "jobs": {
            "query": "CREATE TABLE if not exists jobs(id INT UNSIGNED NOT NULL AUTO_INCREMENT,job VARCHAR(63) NOT NULL,PRIMARY KEY (id))",
            "fields": ["id", "job"],
        },
        "departments": {
            "query": "CREATE TABLE if not exists departments(id INT UNSIGNED NOT NULL AUTO_INCREMENT,department VARCHAR(63) NOT NULL,PRIMARY KEY (id))",
            "fields": ["id", "department"],
        },
        "hired_employees": {
            "query": "CREATE TABLE if not exists hired_employees(id INT UNSIGNED NOT NULL AUTO_INCREMENT,name VARCHAR(63) NOT NULL, datetime VARCHAR(63) NOT NULL,department_id INT UNSIGNED NOT NULL,job_id INT UNSIGNED NOT NULL,PRIMARY KEY (id))",
            "fields": ["id", "name", "datetime", "department_id", "job_id"],
        },
        "drop_tables": {
            "query": "DROP TABLE if exists jobs;DROP TABLE if exists departments;DROP TABLE if exists hired_employees"
        },
    }
    with conn.cursor() as cur:
        i = 0
        first_query = dict_tables[table_name]["query"]
        for sub_query in first_query.split(";"):
            cur.execute(sub_query)
            print("query executed: " + sub_query)

        conn.commit()
        if data:
            n = len(data) - 2
            for row in data[4:n]:
                row = (row.split("\\n"))[1]
                i = i + 1
                data = row.split(",")
                if len(data) > 1:
                    fields = dict_tables[table_name]["fields"]
                    query = (
                        f'insert into {table_name} ({",".join(fields)}) values ('
                        + ",".join([f'"{item}"' for item in data])
                        + ")"
                    )
                    print("query executed: " + query)
                    cur.execute(query)
            conn.commit()
    return i


def lambda_handler(event, context):
    body = event.get("body", None)
    table_name = event["queryStringParameters"]["table"]
    # load data if body exists in event
    if body:
        file_content = str(base64.b64decode(body))
        output = file_content.split("\\r")
        x = addData(output, table_name)
        body_response = {"records_added": x, "on_table": table_name}
    # try to drop tables if body not exists in event
    else:
        output = None
        x = addData(output, table_name)
        body_response = {"action_ok": "drop_tables"}
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body_response),
    }
    return response
