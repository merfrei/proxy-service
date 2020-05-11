"""
Handler for profiles
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.model.profile import ProfileDB


async def get_handler(request):
    '''GET one or more profiles'''
    result = await get_base_get(ProfileDB)(request)
    return result


async def post_handler(request):
    '''POST a new profile'''
    result = await get_base_post(ProfileDB)(request)
    return result


async def put_handler(request):
    '''PUT update a profile'''
    result = await get_base_put(ProfileDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a profile'''
    result = await get_base_delete(ProfileDB)(request)
    return result
