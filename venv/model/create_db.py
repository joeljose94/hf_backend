import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


conn = psycopg2.connect(host='localhost', user='postgres', password='letmein123')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

create_db_sql = "CREATE DATABASE hf_db;" 
conn.cursor().execute(create_db_sql)
conn.close()

