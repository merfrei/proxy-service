"""
Handler for proxy types
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.model.proxy import ProxyTypeDB


async def get_handler(request):
    '''GET one or more proxy types'''
    result = await get_base_get(ProxyTypeDB)(request)
    return result


async def post_handler(request):
    '''POST a new type'''
    result = await get_base_post(ProxyTypeDB)(request)
    return result


async def put_handler(request):
    '''PUT update a type'''
    result = await get_base_put(ProxyTypeDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a type'''
    result = await get_base_delete(ProxyTypeDB)(request)
    return result
