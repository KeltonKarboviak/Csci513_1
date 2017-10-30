#!/usr/bin/env python

import cgi
import json
import os
from dotenv import load_dotenv, find_dotenv


def main():
    correct_password = os.environ.get('ADMIN_PASSWORD')

    form = cgi.FieldStorage()

    # Get the password passed in by the user
    passed_password = form.getvalue('admin_password', '')

    # Check to see if the password submitted by the user matches ADMIN_PASSWORD
    # stored in the .env file
    status = 'success' if correct_password == passed_password else 'error'

    print json.dumps({'status': status})
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
