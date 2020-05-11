"""
This is the main AIOHTTP server for the Proxy Service API
"""

import asyncio
import argparse
from aiohttp import web
from api import init_app


DESCRIPTION = 'Proxy Service API: aiohttp server'


def parse_arguments():
    '''Parse the command line arguments'''
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--path')
    parser.add_argument('--port')
    return parser.parse_args()


def run_server():
    '''Run the main aiohttp server'''
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(loop))
    args = parse_arguments()
    web.run_app(app, path=args.path, port=args.port)


if __name__ == '__main__':
    run_server()
