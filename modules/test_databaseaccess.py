import unittest
import os

from modules import databaseaccess

db_file = "../db/testdb.db"


class TestDBActions(unittest.TestCase):

    def test_create_db(self):
        global db_file

        does_db_exist = os.path.exists(db_file)
        if does_db_exist:
            os.remove(db_file)
        conn = None
        try:
            # create connection and test DB if not exist
            conn = databaseaccess.create_db_if_needed_and_get_connection(db_file)
            self.assertTrue(os.path.exists(db_file))
        finally:
            cleanup(conn)

    def test_write_to_db(self):
        global db_file

        does_db_exist = os.path.exists(db_file)
        if does_db_exist:
            os.remove(db_file)
        conn = None
        try:
            # create connection and test DB if not exist
            conn = databaseaccess.create_db_if_needed_and_get_connection(db_file)
            databaseaccess.create_schema(conn, db_file)
            databaseaccess.load_inner_queries()

            count_before = databaseaccess\
                .execute_query(conn, "SELECT COUNT(*) FROM tweets")\
                .fetchone()[0]

            # insert fake tweet
            test_tweet = [1136432762729222144,
                          20210220223527,
                          'USERNAME',
                          1,
                          0,
                          'MESSAGE',
                          '']
            databaseaccess.insert_tweet(conn, test_tweet)

            count_after = databaseaccess\
                .execute_query(conn, "SELECT COUNT(*) FROM tweets")\
                .fetchone()[0]

            self.assertEquals(count_before, 0)
            self.assertEquals(count_after, 1)
        finally:
            cleanup(conn)

    def test_retrieve_from_db(self):
        global db_file

        does_db_exist = os.path.exists(db_file)
        if does_db_exist:
            os.remove(db_file)
        conn = None
        try:
            # create connection and test DB if not exist
            conn = databaseaccess.create_db_if_needed_and_get_connection(db_file)
            databaseaccess.create_schema(conn, db_file)
            databaseaccess.load_inner_queries()

            # insert fake tweet
            test_tweet = [1136432762729222144,
                          20210220223527,
                          'USERNAME',
                          1,
                          0,
                          'MESSAGE',
                          '']
            databaseaccess.insert_tweet(conn, test_tweet)

            result = databaseaccess.retrieve_tweet(conn, ["1"])
            result = list(result.fetchone())
            self.assertTrue((len(result)-1) == len(test_tweet))
            unittest.TestCase.assertListEqual(self,
                                              list1=result[1:],
                                              list2=test_tweet)
        finally:
            cleanup(conn)


def cleanup(conn):
    global db_file
    if conn:
        conn.close()
    os.remove(db_file)


if __name__ == '__main__':
    unittest.main()
