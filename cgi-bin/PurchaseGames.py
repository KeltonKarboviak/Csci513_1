#!/usr/bin/python

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
            sql_fetch_if_game_in_account = """\
                SELECT a.*, g.price
                FROM customers c, TABLE(c.account) a
                RIGHT JOIN games g
                  ON a.asin = g.asin
                WHERE c.id = :cid
                  AND g.asin = :asin
            """

            sql_update_if_game_exists = """\
                UPDATE TABLE(
                    SELECT c.account FROM customers c WHERE c.id = :cid
                )
                SET quantity = quantity + :add_qty,
                    total = total + (:add_qty * :price)
                WHERE asin = :asin
            """

            sql_insert_if_new_game = """\
                INSERT INTO TABLE(
                    SELECT c.account FROM customers c WHERE c.id = :cid
                )
                VALUES (:asin, :qty, :total)
            """

            # Loop through each asin/quantity pair
            for asin, qty in zip(asins, qtys):
                # First check to see if game exists in customer's account
                cursor.execute(
                    sql_fetch_if_game_in_account,
                    cid=customer_id,
                    asin=asin
                )

                result = cursor.fetchone()

                price = result[3]  # We'll always get the price

                if result[0]:  # Check to see if returned ASIN is not None
                    # Game exists in customer's account already, so we need to
                    # the quantity and total
                    cursor.execute(
                        sql_update_if_game_exists,
                        cid=customer_id,
                        add_qty=qty,
                        price=price,
                        asin=asin
                    )
                else:
                    # Game does not exist in customer's account yet, so we need to
                    # insert it
                    cursor.execute(
                        sql_insert_if_new_game,
                        cid=customer_id,
                        asin=asin,
                        qty=qty,
                        total=qty * price
                    )

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
