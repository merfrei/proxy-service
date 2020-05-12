"""
Handler for targets
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.models.target_provider import TargetProviderDB


async def get_handler(request):
    '''GET one or more target provider relations'''
    result = await get_base_get(TargetProviderDB)(request)
    return result


async def post_handler(request):
    '''POST a new target provider relation'''
    result = await get_base_post(TargetProviderDB)(request)
    return result


async def put_handler(request):
    '''PUT update a target provider relation'''
    result = await get_base_put(TargetProviderDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a target provider relation'''
    result = await get_base_delete(TargetProviderDB)(request)
    return result
