"""
Utilities for MPP
"""

import sys
import logging

import asyncio

import requests

from asyncpg_connect.db import DBSession

from config import get_config


COUNTRY_LOCATIONS = {
    'USA': 'US',
    'UK': 'UK',
    'NL': 'NL',
    'DE': 'DE',
    'France': 'FR',
    'Sweden': 'SE',
    'Luxembourg': 'LU',
}


logging.basicConfig(stream=sys.stdout, level=logging.NOTSET)


async def update_mpp_list(api_url, plan_code, db_session):
    # Get plan
    plan = await db_session.connection.fecthrow(
        'SELECT * FROM provider_plans WHERE code = $1', plan_code)
    if plan is None:
        logging.error('Plan "%s" does not exist', plan_code)
        return
    # Inactive old proxies
    await db_session.connection.fetchval(
        'UPDATE proxies SET active = false WHERE provider_plan_id = $1', plan['id'])
    # Useful data for relations
    proxy_type_id = await db_session.connection.fetchval(
        'SELECT id FROM proxy_types WHERE code = $1', 'PRV')  # Get proxy type ID
    location_id_map = {}  # Map Location CODE => Location ID
    # Fetch and add proxies
    resp = requests.get(api_url)
    data = resp.json()
    for proxy in data:
        proxy_url = f"http://{proxy['proxy_ip']}:{proxy['proxy_port']}"
        if proxy['proxy_country'] not in COUNTRY_LOCATIONS:
            logging.warning('Unable to detect location for country %s', proxy['proxy_country'])
            continue
        location_code = COUNTRY_LOCATIONS[proxy['proxy_country']]
        if location_code not in location_id_map:
            location_id = await db_session.connection.fetchval(
                'SELECT id FROM proxy_locations WHERE code = $1', location_code)
            if location_id is None:
                logging.error('Location CODE does not exist: %s', location_code)
                continue
            location_id_map[location_code] = location_id

        proxy_row = {
            'url': proxy_url,
            'proxy_type_id': proxy_type_id,
            'proxy_location_id': location_id_map[location_code],
            'provider_id': plan['provider_id'],
            'provider_plan_id': plan['id'],
        }

        proxy_id = await db_session.find_or_create('proxies', proxy_row, return_field='id')
        logging.debug('Proxy with ID: %d', proxy_id)


async def main():
    config = get_config()
    db_uri = config['database']['postgres']['uri']
    api_url = config['mpp']['api_url']
    plan_code = config['mpp']['plan_code']
    async with DBSession(db_uri) as db_session:
        await update_mpp_list(api_url, plan_code, db_session)

if __name__ == '__main__':
    asyncio.run(main())
