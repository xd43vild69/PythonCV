import psycopg2
from psycopg2 import Error
from configparser import ConfigParser

def dbconfig(filename="database.ini", section="postgresql"):
    parser= ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section not find into the config")
    return db
dbconfig()