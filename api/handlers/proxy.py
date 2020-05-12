"""
Handler for proxies
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.models.proxy import ProxyDB


async def get_handler(request):
    '''GET one or more proxies'''
    result = await get_base_get(ProxyDB)(request)
    return result


async def post_handler(request):
    '''POST a new proxy'''
    result = await get_base_post(ProxyDB)(request)
    return result


async def put_handler(request):
    '''PUT update a proxy'''
    result = await get_base_put(ProxyDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a proxy'''
    result = await get_base_delete(ProxyDB)(request)
    return result
