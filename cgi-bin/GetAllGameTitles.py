#!/usr/bin/env python

import cx_Oracle as Oracle
import json
import os
from dotenv import load_dotenv, find_dotenv


def main():
    credentials = {
        'user': os.environ.get('ORACLE_USER'),
        'password': os.environ.get('ORACLE_PASSWORD'),
        'dsn': os.environ.get('ORACLE_HOST'),
    }

    games = []

    status = 'error'

    connection, cursor = None, None
    try:
        with Oracle.connect(**credentials) as connection:
            cursor = connection.cursor()

            sql = """\
                SELECT asin, title, price
                FROM games2
                ORDER BY title ASC
            """

            cursor.execute(sql)

            games = [
                {
                    'asin': g[0],
                    'title': g[1],
                    'price': '%.2f' % g[2],
                } for g in cursor
            ]

        status = 'success'
    except Oracle.DatabaseError as e:
        print e
    finally:
        if cursor is not None:
            cursor.close()

        print json.dumps({'status': status, 'games': games})
    # end finally
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
