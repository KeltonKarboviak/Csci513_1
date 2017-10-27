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

    status = 'error'
    purchases = []

    connection, cursor = None, None
    try:
        with Oracle.connect(**credentials) as connection:
            cursor = connection.cursor()

            sql = """\
                SELECT g.title, a.asin, a.quantity, a.total
                FROM customers c, TABLE(c.account) a
                JOIN games g
                  ON a.asin = g.asin
                WHERE c.id = :cid
                ORDER BY g.title ASC
            """

            cursor.execute(sql, cid=customer_id)

            results = cursor.fetchall()

            purchases = [
                {
                    'title': p[0],
                    'asin': p[1],
                    'quantity': p[2],
                    'total': '%.2f' % p[3],
                }
                for p in results
            ]

        status = 'success'
    except Oracle.DatabaseError as e:
        print e
    finally:
        if cursor is not None:
            cursor.close()

        print json.dumps({'status': status, 'purchases': purchases})
    # end finally
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
