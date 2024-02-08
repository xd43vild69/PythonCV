import psycopg2
from psycopg2 import Error
from dbconfig import dbconfig

def dbConnect():
    connection = None
    params = dbconfig()
    print('db connection')
    connection = psycopg2.connect(**params) # use all internal parameters from this dictionary
    cursor = connection.cursor()
    cursor.execute("select * from tblT2I")
    record = cursor.fetchall()

    for row in record:
        print("r:", row, "\n")    

dbConnect()

"""
try:

     # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password="pCh4rc0l13.",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="aiSD")
    
    # Create a cursor to perform database operations
    cursor = connection.cursor()

    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    # Executing a SQL query
    cursor.execute("select * from tblT2I")

    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")    

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")    
"""