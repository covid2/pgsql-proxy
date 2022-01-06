import argparse
import os
import psycopg2
import re
import sys
import time

parser = argparse.ArgumentParser(description='This script creates a simulated office employee data set in a PostgreSQL database.', add_help=False)
parser.add_argument("--help", action="help", help="Show this help message and exit.")
parser.add_argument("-h", "--host", help="Specify a host destination for the PostgreSQL instance. Defaults to localhost.", default="127.0.0.1")
parser.add_argument("-p", "--port", help="Specify a port for the PostgreSQL connection. Defaults to 5432.", default=5432)
parser.add_argument("-U", "--user", help="Specify a database user.")
parser.add_argument("-W", "--password", help="Specify the db user's password.")
parser.add_argument("-d", "--dbname", help="Specify a database name to use in your PostgreSQL instance.")
parser.add_argument("-l", "--locations", help="Specify number of locations for the fake employee data.", default=8)
parser.add_argument("-e", "--employees", help="Specify number of employees per location for the fake employee data.", default=8)
parser.add_argument("-a", "--auto", help="If the specified database name doesn't exist, passing this flag tells script to automatically create it.", action='store_true')
parser.add_argument("-n", "--dontclean", help="By default the script truncates the tables. Passing this flag means the tables will be left alone.", action='store_true')
parser.add_argument("-c", "--continuous", help="Instead of populating the db as fast as possible, this tells the script to stream instead up to the numbers specified.", action='store_true')
args = parser.parse_args()

# from config import SQL instance connection info, and 
# our database information to connect to the db
SQL_HOST = os.environ.get("SQL_HOST", args.host)
DB_PORT  = os.environ.get("DB_PORT", args.port)
DB_USER  = os.environ.get("DB_USER", args.user)
DB_PASS  = os.environ.get("DB_PASS", args.password)
DB_NAME  = os.environ.get("DB_NAME", args.dbname)

# configurable defaults for how many variations you want
LOCATIONS = 0
try:
    LOCATIONS = int(args.locations)
except:
    print("Locations count must be an integer.")
    sys.exit(1)
# Make sure that we have all the pieces we must have in order to connect to our db properly
if not DB_USER:
    print ("You have to specify a database user either by environment variable or pass one in with the -u flag.")
    sys.exit(2)
if not DB_PASS:
    print ("You have to specify a database password either by environment variable or pass one in with the -p flag.")
    sys.exit(2)
if not DB_NAME:
    print ("You have to specify a database name either by environment variable or pass one in with the -d flag.")
    sys.exit(2)
if not DB_PORT:
    print ("You have to specify a database port either by environment variable or pass one in with the -P flag.")
    sys.exit(2)


# Wait for our database connection
mydb = None
attempt_num = 0
wait_amount = 1
rowid = 0
# backoff_count is the static count for how many times we should try at one
# second increments before expanding the backoff time exponentially
# Once the wait time passes a minute, we'll give up and exit with an error
backoff_count = 5
def connect_database():
    global attempt_num
    global wait_amount
    global mydb
    
    try:
        mydb = psycopg2.connect(
            host=SQL_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME
        )
        cur = mydb.cursor()
        print("connected db",SQL_HOST)
        cur.execute("SELECT to_char(current_timestamp, 'dd/mm/yyyy  HH12:MI:SS');")
        result= cur.fetchone()
        cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(rowid, result))
        cur.execute("SELECT count (*) as cnt FROM test;")
        result1 = cur.fetchone()
        print ("total records : ",result,"executed at ", result1)
        mydb.commit()
        cur.close()
        mydb.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        sys.exit(1)
        
while 1 == 1:
    rowid  = rowid +1
    connect_database()

