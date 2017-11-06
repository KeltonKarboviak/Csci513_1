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

    # Get the asin and developers
    asin = form.getvalue('asin', '')
    title = form.getvalue('title', '')
    price = float(form.getvalue('price', '0'))
    devs = zip(form.getlist('dev_ids[]'), form.getlist('dev_names[]'))

    status = 'error'

    connection, cursor = None, None
    try:
        with Oracle.connect(**credentials) as connection:
            cursor = connection.cursor()

            dev_table_type = connection.gettype('DEVELOPERS_TABLE')
            dev_table_obj = dev_table_type.newobject()

            dev_type = connection.gettype('DEV_T')

            sql = """\
                UPDATE games2
                SET title = :title,
                    price = :price,
                    developers = :developers
                WHERE asin = :asin
            """

            for d in devs:
                dev_obj = dev_type.newobject()
                dev_obj.ID, dev_obj.NAME = d[0], d[1]
                dev_table_obj.append(dev_obj)

            cursor.execute(sql, asin=asin, title=title, price=price, developers=dev_table_obj)

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
