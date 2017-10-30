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

    # Get the developer's id
    dev_id = form.getvalue('id', '')

    details = {}

    status = 'error'

    connection, cursor = None, None
    try:
        with Oracle.connect(**credentials) as connection:
            cursor = connection.cursor()

            sql = """\
                SELECT d.id, d.name, g.asin, g.title, g.price
                FROM games2 g, TABLE(g.developers) d
                WHERE d.id = :id
            """

            cursor.execute(sql, id=dev_id)

            results = cursor.fetchall()

            # Check to see that we successully received something
            if results:
                details = {
                    'id': results[0][0],
                    'name': results[0][1],
                    'games': [
                        {
                            'asin': r[2], 'title': r[3], 'price': r[4]
                        } for r in results
                    ]
                }

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
