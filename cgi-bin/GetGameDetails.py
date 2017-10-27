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

    DEV_TABLE_TYPE_NAME = 'DEVELOPERS_TABLE'

    form = cgi.FieldStorage()

    # Get the customer's id
    asin = form.getvalue('asin', '')

    status = 'error'

    # Initialize the result values with None's and an empty list for developers
    # since it represents the nested developers_table
    title, price, devs = None, None, []

    connection, cursor = None, None
    try:
        with Oracle.connect(**credentials) as connection:
            cursor = connection.cursor()

            sql = """\
                SELECT *
                FROM games_developer g_devs
                JOIN games g
                  ON g_devs.asin = g.asin
                JOIN developers d
                  ON g_devs.developer_id = d.id
                WHERE g.asin = :asin
            """

            sql = """\
                SELECT title, price, developers
                FROM games2
                WHERE asin = :asin
            """

            cursor.execute(sql, asin=asin)

            result = cursor.fetchone()

            # Check to see if result is not None
            if result:
                # Set devs as the nested table object as a list for
                # when we create the JSON result within the finally block
                title, price, devs = result
                devs = devs.aslist()

        status = 'success'
    except Oracle.DatabaseError as e:
        print e
    finally:
        if cursor is not None:
            cursor.close()

        print json.dumps(
            {
                'status': status,
                'asin': asin,
                'title': title,
                'price': price,
                'developers': [{'id': d.ID, 'name': d.NAME} for d in devs]
            }
        )
    # end finally
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
