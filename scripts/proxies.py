"""
Manage Proxies

- Add Providers and Plans
- Add types and locations
- Add proxy TXT lists
"""

import sys
import os
import re

import asyncio
import logging
import argparse

from asyncpg_connect.db import DBSession

from config import get_config


URL_RE = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


DESCRIPTION = 'Proxy Service - Proxy data management'


def parse_arguments():
    '''Parse the command line arguments'''
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--provider', type=str, dest='provider',
                        help='Add a new provider (CSV: code,name,url)')
    parser.add_argument('--plan', type=str, dest='plan',
                        help='Add a new plan (CSV: provider_code,plan_code,name)')
    parser.add_argument('--proxy_type', type=str, dest='proxy_type',
                        help='Add a new proxy type (CSV: code,name)')
    parser.add_argument('--proxy_loc', type=str, dest='proxy_loc',
                        help='Add a new proxy location (CSV: code,name)')
    parser.add_argument('--proxy_txt', type=str, dest='proxy_txt',
                        help='Add a list of proxies')
    parser.add_argument('--proxy_txt_plan', type=str, dest='proxy_txt_plan',
                        help='Proxy list plan (Plan code)')
    parser.add_argument('--proxy_txt_type', type=str, dest='proxy_txt_type',
                        help='Proxy list type (Type code)')
    parser.add_argument('--proxy_txt_location', type=str, dest='proxy_txt_loc',
                        help='Proxy list location (Location code)')
    return parser.parse_args()


async def add_new_provider(db_session: DBSession, code: str, name: str, url: str):
    '''Add a new provider'''
    provider_row = {
        'code': code.strip(),
        'name': name.strip(),
        'url': url.strip(),
    }
    provider_id = await db_session.find_or_create('providers', provider_row, return_field='id')
    logging.debug('Added provider with ID: %d', provider_id)


async def add_new_plan(db_session: DBSession, provider: str, code: str, name: str):
    '''Add a new provider plan'''
    provider_code = provider.strip()
    provider_id = await db_session.connection.fetchval(
        'SELECT id FROM providers WHERE code = $1', provider_code)
    if provider_id is None:
        logging.error('Provider %s does not exist', provider_code)
        return
    plan_row = {
        'provider_id': provider_id,
        'name': name.strip(),
        'code': code,
    }
    plan_id = await db_session.find_or_create('provider_plans', plan_row, return_field='id')
    logging.debug('Added provider plan with ID: %d', plan_id)


async def add_new_type(db_session: DBSession, code: str, name: str):
    '''Add a new proxy type'''
    type_row = {
        'code': code.strip(),
        'name': name.strip(),
    }
    type_id = await db_session.find_or_create('proxy_types', type_row, return_field='id')
    logging.debug('Added proxy type with ID: %d', type_id)


async def add_new_location(db_session: DBSession, code: str, name: str):
    '''Add a new proxy type'''
    loc_row = {
        'code': code.strip(),
        'name': name.strip(),
    }
    loc_id = await db_session.find_or_create('proxy_locations', loc_row, return_field='id')
    logging.debug('Added proxy location with ID: %d', loc_id)


async def import_proxy_list_txt(  # pylint: disable=too-many-locals
        db_session: DBSession, txt_file: str, proxy_type: str,
        proxy_plan: str = None, proxy_location: str = None):
    '''Import a TXT file with proxies'''
    proxy_type_code = proxy_type.strip()
    proxy_type_id = await db_session.connection.fetchval(
        'SELECT id FROM proxy_types WHERE code = $1', proxy_type_code)
    if proxy_type_id is None:
        logging.error('Not valid proxy type: %s', proxy_type_code)
        return
    if proxy_plan is not None:
        proxy_plan_code = proxy_plan.strip()
        proxy_plan = await db_session.connection.fetchrow(
            'SELECT * FROM provider_plans WHERE code = $1', proxy_plan_code)
        if proxy_plan is None:
            logging.error('Not valid provider plan: %s', proxy_plan_code)
            return
        proxy_provider_id = proxy_plan['provider_id']
        proxy_plan_id = proxy_plan['id']
    else:
        proxy_provider_id = None
        proxy_plan_id = None
    if proxy_location is not None:
        proxy_location_code = proxy_location.strip()
        proxy_location_id = await db_session.connection.fetchval(
            'SELECT id FROM proxy_locations WHERE code = $1', proxy_location_code)
        if proxy_location_id is None:
            logging.error('Not valid location: %s', proxy_location_code)
            return
    else:
        proxy_location_id = None

    if not os.path.exists(txt_file):
        logging.error('File does not exist in current directory: %s', txt_file)
        return

    with open(txt_file) as f_txt:
        for line in f_txt:
            proxy_url = line.strip()
            if not proxy_url:
                continue
            if not URL_RE.match(proxy_url):
                logging.warning('Ignoring not valid proxy URL: %s', proxy_url)
                continue
            proxy_row = {
                'url': proxy_url,
                'proxy_type_id': proxy_type_id,
                'proxy_location_id': proxy_location_id,
                'provider_id': proxy_provider_id,
                'provider_plan_id': proxy_plan_id,
            }
            proxy_id = await db_session.find_or_create('proxies', proxy_row, return_field='id')
            logging.debug('Added proxy with ID: %d', proxy_id)


async def main():
    '''All happens here'''
    args = parse_arguments()

    log_format = '%(levelname)s: %(asctime)s %(filename)s: %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.NOTSET,
                        format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

    config = get_config()
    db_uri = config['database']['postgres']['uri']
    async with DBSession(db_uri) as db_session:
        if args.provider:
            logging.info('Adding provider: %s', args.provider)
            await add_new_provider(db_session, *args.provider.split(','))
        if args.plan:
            logging.info('Adding plan: %s', args.plan)
            await add_new_plan(db_session, *args.plan.split(','))
        if args.proxy_type:
            logging.info('Adding proxy type: %s', args.proxy_type)
            await add_new_type(db_session, *args.proxy_type.split(','))
        if args.proxy_loc:
            logging.info('Adding proxy location: %s', args.proxy_loc)
            await add_new_location(db_session, *args.proxy_loc.split(','))
        if args.proxy_txt:
            logging.info('Importing TXT file: %s', args.proxy_txt)
            await import_proxy_list_txt(db_session,
                                        args.proxy_txt, args.proxy_txt_type,
                                        args.proxy_txt_plan, args.proxy_txt_loc)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
