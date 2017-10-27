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

    # Get the customer's id
    customer_id = form.getvalue('id', '')

    # Grab the asins that were passed in and their corresponding quantities
    asins = form.getlist('asins[]')
    qtys = [int(q) for q in form.getlist('qtys[]')]

    status = 'error'

    connection, cursor = None, None
    try:
        with Oracle.connect(**credentials) as connection:
            cursor = connection.cursor()

            # In query we're doing a RIGHT JOIN because we always want to get
            # the price of the game whether it's in their account already
            # or not
            sql = "SELECT * FROM customers"

            cursor.execute(sql)

            results = cursor.fetchall()

        status = 'success'
    except Oracle.DatabaseError as e:
        print e
    finally:
        if cursor is not None:
            cursor.close()

        print json.dumps({'status': status})
    # end finally
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
