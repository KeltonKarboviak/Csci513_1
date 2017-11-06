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

    asin = form.getvalue('asin', '')

    status = 'error'

    connection, cursor = None, None
    try:
        with Oracle.connect(**credentials) as connection:
            cursor = connection.cursor()

            # First get game asin, title, & price
            sql = """\
                SELECT asin, title, price
                FROM games2
                WHERE asin = :asin
            """

            cursor.execute(sql, asin=asin)

            result = cursor.fetchone()

            if result:
                asin = result[0]
                title = result[1]
                price = result[2]

                # Now get all the developers, but give the developers that are
                # associated with this ASIN a flag so that they can be pre-selected
                # in the dropdown box
                sql = """\
                    SELECT id, name, fnc_DidDevelop(:asin, id) AS did_develop
                    FROM developers
                """

                cursor.execute(sql, asin=asin)

                devs = [{'id': d[0], 'name': d[1], 'selected': d[2] > 0} for d in cursor]

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
                'devs': devs
            }
        )
    # end finally
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
