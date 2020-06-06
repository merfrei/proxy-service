"""
API

Main app
"""

import asyncpg
from aiohttp import web
import aioredis
from api.routes import init_routes
from api.auth import apikey_middleware


def load_api_keys(app, config):
    '''Load the API Keys from config'''
    # Main API Key
    app['api_key'] = config['api']['api_key']
    # Methods API Keys
    for method in ('get', 'post', 'put', 'delete'):
        api_key_k = '{}_api_key'.format(method)
        if api_key_k in config['api']:
            app[api_key_k] = config['api'][api_key_k]


async def init_app(loop, config):
    '''Init aiohttp app'''
    app = web.Application(middlewares=[apikey_middleware])
    app['config'] = config
    load_api_keys(app, config)

    # Create a database connection pool
    app['pool'] = await asyncpg.create_pool(
        config['database']['postgres']['uri'],
        min_size=config['database']['postgres']['pool_min'],
        max_size=config['database']['postgres']['pool_max'])
    app['redis'] = await aioredis.create_redis_pool(
        config['database']['redis']['uri'],
        minsize=config['database']['redis']['pool_min'],
        maxsize=config['database']['redis']['pool_max'],
        loop=loop)

    init_routes(app)

    return app
