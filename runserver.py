#!/usr/bin/env python3
"""module for running the server"""

#-----------------------------------------------------------------------
# runserver.py
# Author: Ekow Bentsi-Enchill
#-----------------------------------------------------------------------

from sys import exit, stderr
from app import app
import argparse

def get_port():
    """gets port from user input"""
    parser = argparse.ArgumentParser(description='The logic application')
    parser.add_argument('port', type=int, help='the port at which the server should listen')
    args = parser.parse_args()

    try:
        return int(args.port)
    except ValueError:
        parser.print_help()
        exit(1)

def main():
    """runs the server"""
    try:
        port = int(get_port())
    except OverflowError:
        print('Port must be an integer.', file=stderr)
        exit(1)



    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except OSError as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
