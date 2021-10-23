"""
Test all proxies
"""

import sys
import os
import re

import asyncio
import logging
import argparse
import requests

from requests.exceptions import RequestException

from asyncpg_connect.db import DBSession

from config import get_config


TARGET_URL = 'https://api.myip.com/'
CONCURRENT_REQUESTS = 64
TIMEOUT_SEC = 10

DESCRIPTION = 'Proxy Service - Test Proxies'


def parse_arguments():
    '''Parse the command line arguments'''
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--provider', type=str, dest='provider',
                        help='Filter by provider code')
    parser.add_argument('--proxy_type', type=str, dest='proxy_type',
                        help='Filter by proxy type code')
    parser.add_argument('--location', type=str, dest='location',
                        help='Filter by location code')
    return parser.parse_args()


async def test_proxy(proxy: dict):
    logging.info('TESTING PROXY: %s', proxy['url'])
    try:
        res = requests.get(TARGET_URL,
                           proxies={'http': proxy['url'],
                                    'https': proxy['url']},
                           timeout=TIMEOUT_SEC)
    except RequestException as exp:
        logging.error('Proxy failed with error: %r -> %s', proxy, exp)
        return

    if res.status_code != 200:
        logging.error('Proxy returned no 200 code: %d', res.status_code)


async def test_proxy_list(proxy_list: list):
    futures = []
    while proxy_list:
        proxy = proxy_list.pop(0)
        futures.append(test_proxy(proxy))
        if len(futures) == CONCURRENT_REQUESTS or not proxy_list:
            await asyncio.gather(*futures)
            futures = []


async def get_proxy_list(db_session: DBSession, provider_code: str, location_code: str, type_code: str) -> list:
    query = '''SELECT
        prx.url as "url",
        prv.name as "provider",
        loc.name as "location",
        pty.name as "type"
        FROM
        proxies prx
        LEFT JOIN providers prv ON (prx.provider_id = prv.id)
        LEFT JOIN proxy_locations loc ON (prx.proxy_location_id = loc.id)
        LEFT JOIN proxy_types pty ON (prx.proxy_type_id = pty.id)'''
    where = ['prx.active = $1']
    args = [True]
    if provider_code:
        args.append(provider_code)
        where.append(f'prv.code = ${len(args)+1}')
    if location_code:
        args.append(location_code)
        where.append(f'loc.code = ${len(args)+1}')
    if type_code:
        args.append(type_code)
        where.append(f'pty.code = ${len(args)+1}')

    if where:
        where_str = ' AND '.join(where)
        query += f' WHERE {where_str}'

    proxies = await db_session.connection.fetch(query, *args)

    return [dict(res) for res in proxies]

async def main():
    '''All happens here'''
    args = parse_arguments()

    log_format = '%(levelname)s: %(asctime)s %(filename)s: %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.NOTSET,
                        format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

    config = get_config()
    db_uri = config['database']['postgres']['uri']
    async with DBSession(db_uri) as db_session:
        logging.info('Testing proxies: %r', args)
        proxy_list = await get_proxy_list(db_session, args.provider, args.location, args.proxy_type)

    logging.info('%d PROXIES LOADED', len(proxy_list))

    await test_proxy_list(proxy_list)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
