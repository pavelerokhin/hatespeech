# main launcher

import yaml
import sys
from modules import twitterlistener as tl
from modules.create_sql_database import orchestrate_db_connection, SQLiteConnectionError, \
    InsufficientConfigurationError

if __name__ == "__main__":
    # get config
    conf = ""
    with open("conf.yml", "r") as conf_file:
        conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        if not conf:
            print("no configurations")
            sys.exit(1)
    # get twitter keys
    keys = ""
    with open("twitter_keys.yml", "r") as twitter_keys_file:
        keys = yaml.load(twitter_keys_file, Loader=yaml.FullLoader)
        if not keys:
            print("no Twitter keys")
            sys.exit(1)

    conn = None
    try:
        conn = orchestrate_db_connection(conf)
        tl.stream_go(conf, keys, conn)
    except (SQLiteConnectionError, InsufficientConfigurationError) as e:
        print(e.message)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

