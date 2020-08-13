"""
Handler for provider plans
"""

from api.handlers.base import get_base_get
from api.handlers.base import get_base_post
from api.handlers.base import get_base_put
from api.handlers.base import get_base_delete
from api.models.provider_plan import ProviderPlanDB
from api.models.provider_plan import ProviderPlanView


async def get_handler(request):
    '''GET one or more providers'''
    result = await get_base_get(ProviderPlanView)(request)
    return result


async def post_handler(request):
    '''POST a new provider'''
    result = await get_base_post(ProviderPlanDB)(request)
    return result


async def put_handler(request):
    '''PUT update a provider'''
    result = await get_base_put(ProviderPlanDB)(request)
    return result


async def delete_handler(request):
    '''DELETE remove a provider'''
    result = await get_base_delete(ProviderPlanDB)(request)
    return result
