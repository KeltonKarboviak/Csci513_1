#!/usr/bin/env python

import json
import os
from dotenv import load_dotenv, find_dotenv
from subprocess import Popen, PIPE


def main():
    credentials = {
        'user': os.environ.get('ORACLE_USER'),
        'password': os.environ.get('ORACLE_PASSWORD'),
        'dsn': os.environ.get('ORACLE_HOST'),
    }

    status = 'error'

    cmd = Popen(['sqlplus', '-S', '%(user)s/%(password)s@//%(dsn)s' % credentials], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    cmd.stdin.write('@../database/fresh.sql')
    result = cmd.communicate()

    if 'error' not in ''.join(result):
        status = 'success'

    print json.dumps({'status': status})
    # end finally
# end def main()


if __name__ == '__main__':
    # Load in environment variables
    load_dotenv(find_dotenv())

    main()
