"""
Handler for targets
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.model.target import TargetDB


async def get_handler(request):
    '''GET one or more targets'''
    result = await get_base_get(TargetDB)(request)
    return result


async def post_handler(request):
    '''POST a new target'''
    result = await get_base_post(TargetDB)(request)
    return result


async def put_handler(request):
    '''PUT update a target'''
    result = await get_base_put(TargetDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a target'''
    result = await get_base_delete(TargetDB)(request)
    return result
