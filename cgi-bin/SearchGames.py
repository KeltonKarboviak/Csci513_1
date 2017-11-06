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

    # Grab the string of names passed in through CGI (give empty string if
    # nothing was passed in), then convert string to lowercase, then split it on
    # all whitespaces to get a list. We want the names in lowercase for
    # case-insensitive comparison
    names = form.getvalue('search_keywords', '').strip().lower().split()
    num_names = len(names)
    sorted_games = []
    status = 'error'

    connection, cursor = None, None
    try:
        connection = Oracle.connect(**credentials)
        cursor = connection.cursor()

        # Initialize SQL statement with no WHERE so that we'll retrieve data
        # for all games
        sql = """\
            SELECT g.asin, g.title, d.name
            FROM games2 g, TABLE(g.developers) d
        """

        # Build the WHERE clause here. If names is empty, it'll just be an
        # empty string, otherwise it'll add a LIKE comparison for each name
        # we have
        where_clause = '' \
            if num_names == 0 \
            else 'WHERE ' + ' OR '.join( ["LOWER(d.name) LIKE '%' || :{} || '%'"] * num_names ).format( *range(num_names) )

        sql += where_clause

        cursor.execute(sql, names)
        results = cursor.fetchall()

        # This dict will be used for storing ASINs and their corresponding
        # number of keyword hits
        games = {}

        for asin, title, dev_name in results:
            # Use lowercase for case-insensitive comparison
            dev_name = dev_name.lower()

            # Check if ASIN doesn't exist in our resulting games dict
            if asin not in games:
                games[asin] = {'title': title, 'hits': 0}

            # Add number of hits for this developer to running total for ASIN
            games[asin]['hits'] += reduce(
                lambda hits, name: hits + 1 if name in dev_name else hits,
                names,
                0
            )
        # end for

        # We want the games sorted by number of hits descending first, then by
        # title asc when there's a tie for hits. We have to perform the sorts
        # in opposite order due to logic of sorting.
        sorted_games = sorted(games.items(), key=lambda (k, v): v['title'])
        sorted_games.sort(key=lambda (k, v): v['hits'], reverse=True)

        # Restructure games to be in format: [{'asin': 'XXX', 'title': 'YYY'}, ...]
        sorted_games = map(lambda (k, v): {'asin': k, 'title': v['title']}, sorted_games)

        status = 'success'
    except Oracle.DatabaseError as e:
        print e
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

        print json.dumps({'status': status, 'games': sorted_games})
    # end finally
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
