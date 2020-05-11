"""
Handler for proxy locations
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.model.proxy import ProxyLocationDB


async def get_handler(request):
    '''GET one or more proxy locations'''
    result = await get_base_get(ProxyLocationDB)(request)
    return result


async def post_handler(request):
    '''POST a new location'''
    result = await get_base_post(ProxyLocationDB)(request)
    return result


async def put_handler(request):
    '''PUT update a location'''
    result = await get_base_put(ProxyLocationDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a location'''
    result = await get_base_delete(ProxyLocationDB)(request)
    return result
