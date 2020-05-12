"""
API

Main app
"""

import aioredis
import asyncpg
from aiohttp import web
from api.routes import init_routes


async def init_app(loop, config):
    '''Init aiohttp app'''
    app = web.Application()
    app['config'] = config

    # Create a database connection pool
    app['pool'] = await asyncpg.create_pool(config['database']['postgres']['uri'])
    app['redis'] = await aioredis.create_redis_pool(
        config['database']['redis']['uri'],
        minsize=config['database']['redis']['pool_min'],
        maxsize=config['database']['redis']['pool_max'],
        loop=loop)

    init_routes(app)

    return app
