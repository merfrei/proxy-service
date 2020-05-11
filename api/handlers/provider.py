"""
Handler for providers
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.model.provider import ProviderDB


async def get_handler(request):
    '''GET one or more providers'''
    result = await get_base_get(ProviderDB)(request)
    return result


async def post_handler(request):
    '''POST a new provider'''
    result = await get_base_post(ProviderDB)(request)
    return result


async def put_handler(request):
    '''PUT update a provider'''
    result = await get_base_put(ProviderDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a provider'''
    result = await get_base_delete(ProviderDB)(request)
    return result
