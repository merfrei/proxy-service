"""
Handler for targets
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.models.target_provider_plan import TargetProviderPlanDB


async def get_handler(request):
    '''GET one or more target provider plan relations'''
    where_query = []
    if 'target_id' in request.query:
        where_query.append(
            ('target_id', '=', int(request.query['target_id'])))
    result = await get_base_get(TargetProviderPlanDB, *where_query)(request)
    return result


async def post_handler(request):
    '''POST a new target provider plan relation'''
    result = await get_base_post(TargetProviderPlanDB)(request)
    return result


async def put_handler(request):
    '''PUT update a target provider relation'''
    result = await get_base_put(TargetProviderPlanDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a target provider relation'''
    result = await get_base_delete(TargetProviderPlanDB)(request)
    return result
