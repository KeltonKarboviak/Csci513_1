#!/usr/bin/env python

import cgi
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

    form = cgi.FieldStorage()

    # Get the game's ASIN. If fetchAll == 1, then this value is ignored.
    asin = form.getvalue('asin', '')

    # Get whether we are fetching details for one game or for all games.
    # This should be converted to an int as it will be later used as a bool
    fetch_all = int(form.getvalue('fetchAll', '1'))

    status = 'error'

    details = []

    # Initialize sql query params as empty for base case of wanting to fetch all game details
    query_params = {}

    connection, cursor = None, None
    try:
        with Oracle.connect(**credentials) as connection:
            cursor = connection.cursor()

            sql = """\
                SELECT asin, title, price, developers
                FROM games2
            """

            if not bool(fetch_all):
                # If we don't want to fetch all of the games, then add a WHERE
                # clause to the sql query and add the desired ASIN to the dict
                # of query params
                sql += 'WHERE asin = :asin'
                query_params['asin'] = asin

            cursor.execute(sql, query_params)

            results = cursor.fetchall()

            details = [
                {
                    'asin': g[0],
                    'title': g[1],
                    'price': '%.2f' % g[2],
                    'devs': [{'id': d.ID, 'name': d.NAME} for d in g[3].aslist()]
                } for g in results
            ]

        status = 'success'
    except Oracle.DatabaseError as e:
        print e
    finally:
        if cursor is not None:
            cursor.close()

        print json.dumps({'status': status, 'details': details})
    # end finally
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
