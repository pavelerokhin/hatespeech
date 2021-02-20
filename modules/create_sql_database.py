import os
import sqlite3
from sqlite3 import Error

INSERT_MESSAGE_QUERY = ""


def orchestrate_db_connection(conf):
    db_file = conf.get('dbPath')
    if not db_file:
        raise InsufficientConfigurationError("no DB filepath available")

    db_exists = os.path.exists(db_file)

    # create connection and DB if not exist
    conn = create_connection(db_file)

    if not db_exists:
        # TODO: control if schema has been installed
        create_schema(conn, db_file)

    load_queries()  # TODO: make it without global vars

    return conn


def create_connection(db_file):
    """
    create connection to SQLite database
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        raise SQLiteConnectionError(e)

    return conn


def execute_query(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
    except Error as e:
        raise QueryExecutionError("error while executing query", e)


def create_schema(conn, db_file):
    if conn:
        with open("db/dbschema/hatespeech_tweets.sql", "r") as schema_file:
            create_table_sql = schema_file.read().replace("\n", " ")
        execute_query(conn, create_table_sql)


def load_queries():
    global INSERT_MESSAGE_QUERY
    with open('db/queries/insert_tweet.sql') as q:
        INSERT_MESSAGE_QUERY = q.read().replace("\n", "")


def create_table(conn, create_table_sql):
    """
    create table from the create_table_sql
    """
    execute_query(create_table_sql)


def insert_tweet(conn, values):
    global INSERT_MESSAGE_QUERY
    populated_query = INSERT_MESSAGE_QUERY.format(*values)
    execute_query(conn, populated_query)


# Exceptions

class InsufficientConfigurationError(Exception):
    def __init__(self, message, err):
        self.message = message
        self.err = err


class SQLiteConnectionError(Error):
    def __init__(self, message, err):
        self.message = message
        self.err = err


class QueryExecutionError(Error):
    def __init__(self, message, err):
        self.message = message
        self.err = err


