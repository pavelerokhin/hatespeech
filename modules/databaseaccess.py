import os
import yaml
import sqlite3
from sqlite3 import Error

QUERIES = {
    "INSERT_MESSAGE_QUERY": "",
    "RETRIEVE_TWEET_BY_ID": "",
    "RETRIEVE_TWEET_BY_WORDS_IN_TEXT": "",
    "RETRIEVE_TWEET_BY_WORDS_IN_QUOTE": "",
}

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def orchestrate_db_connection(conf):
    db_file = conf.get('dbPath')
    if not db_file:
        raise InsufficientConfigurationError("no DB filepath available")

    db_exists = os.path.exists(db_file)

    # create connection and DB if not exist
    conn = create_db_if_needed_and_get_connection(db_file)

    if not db_exists:
        # TODO: control if schema has been installed
        create_schema(conn, db_file)

    load_inner_queries()  # TODO: make it without global vars

    return conn


def create_db_if_needed_and_get_connection(db_file):
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
        result = c.execute(query)
        conn.commit()
        return result
    except Error as e:
        raise QueryExecutionError("error while executing query", e)


def create_schema(conn, db_file):
    if conn:
        schema_path = SCRIPT_PATH+"/../db/dbschema/"
        schema_scripts = [schema_path + script_name for script_name in os.listdir(schema_path)]

        for ss in schema_scripts:
            with open(ss, "r") as schema_file:
                schema_script = schema_file.read().replace("\n", " ")
            execute_query(conn, schema_script)


def load_inner_queries():
    with open(SCRIPT_PATH+"/../db/queries/queries.yml", "r") as qc:
        query_files = yaml.load(qc, Loader=yaml.FullLoader)

        for query_name in query_files.keys():
            with open(SCRIPT_PATH+"/../db/queries/" + query_files.get(query_name)) as q:
                QUERIES[query_name] = q.read().replace("\n", "")


def insert_tweet(conn, values):
    populated_query = QUERIES["INSERT_MESSAGE_QUERY"].format(*values)
    execute_query(conn, populated_query)


def retrieve_tweet_by_id(conn, values):
    populated_query = QUERIES["RETRIEVE_TWEET_BY_ID"].format(*values)
    return execute_query(conn, populated_query)


def retrieve_tweet_by_tweet_text(conn, values):
    populated_query = QUERIES["RETRIEVE_TWEET_BY_WORDS_IN_TEXT"].format(*values)
    return execute_query(conn, populated_query)


def retrieve_tweet_by_quote_text(conn, values):
    populated_query = QUERIES["RETRIEVE_TWEET_BY_WORDS_IN_QUOTE"].format(*values)
    return execute_query(conn, populated_query)


# Exceptions
class InsufficientConfigurationError(Error):
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
