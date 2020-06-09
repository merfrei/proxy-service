"""
Handler for target provider relations
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.models.target_provider import TargetProviderDB


async def get_handler(request):
    '''GET one or more target provider relations'''
    where_query = []
    if 'target_id' in request.query:
        where_query.append(
            ('target_id', '=', int(request.query['target_id'])))
    result = await get_base_get(TargetProviderDB, *where_query)(request)
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
