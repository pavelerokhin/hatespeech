import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    create connection to SQLite database
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print("connection error:", e)
    finally:
        if conn:
            conn.close()


def create_schema(conn):
    if conn:
        with open("../dbschema/hatespeech_tweets.sql", "r") as schema_file:
            create_table_sql = schema_file.readlines()
        create_table(conn, create_table_sql)


def create_table(conn, create_table_sql):
    """
    create table from the create_table_sql
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print("error while creating table", e)

