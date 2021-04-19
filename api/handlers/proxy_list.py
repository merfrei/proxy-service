"""
This is the main handler

Check some parameters and returns a proxy list

The parameters could be:

- Target ID
- Limit length
- Locations
- Providers
- Profile
- Proxy type (http, tor, backconnect, residential)

Some targets may not have permission to use some providers and plans
"""

from aiohttp import web
from api.models.target import TargetDB
from api.models.target_provider import TargetProviderDB
from api.models.target_provider_plan import TargetProviderPlanDB
from api.models.proxy import ProxyDB
from api.models.proxy_location import ProxyLocationDB
from api.models.proxy_type import ProxyTypeDB
from api.models.provider import ProviderDB
from api.models.provider_plan import ProviderPlanDB
from lib.proxies.pool import ProxyPool


async def get_target_id_from_identifier(request, identifier: str):
    '''Given a Target identifier it returns the value if the ID in the database'''
    target_db = TargetDB(request.app)
    target_id = await target_db.select_val(*[('identifier', '=', identifier)], columns='id')
    return target_id


async def get_db_element_id_from_code(request, model_db, code):
    '''Return an ID from a given code
    @param request: the aiohttp request
    @param model_db: a DBModel class
    @param code: a string with the unique element code
    @return: an integer with the element ID or None'''
    model_inst = model_db(request.app)
    elem_id = await model_inst.select_val(*[('code', '=', code)], columns='id')
    return elem_id


async def add_filter_if_not_none(request, model_db, filter_in, filter_out, where):
    '''If the ID exists in database the filter will be added to the where query
    The filter uses the `code` of the element. A unique "code" to use so it does not use the actual
    element ID. So, it needs to make a query to get the actual ID using that element code
    Then, the query is added to the where list to filter the proxy list by the related element ID
    @param request: the aiohttp request
    @param model_db: the DBModel class. Where to get the id from
    @param filter_in: string with the key in the request.query dict
    @param filter_out: string with the column name of the relationship in the `proxies` table
    @param where: reference to the where list with the queries'''
    elem_code = request.query.get(filter_in)
    if elem_code is not None:
        elem_id = await get_db_element_id_from_code(request, model_db, elem_code)
        if elem_id is not None:
            where.append((filter_out, '=', elem_id))


async def add_proxy_filter_to_where(request, where):
    '''Given a query it will complete the where query passed as reference
    Query:
    - loc: Location
    - type: Proxy Type
    - prov: Provider
    - plan: Provider Plan'''
    await add_filter_if_not_none(request, ProxyLocationDB, 'loc', 'proxy_location_id', where)
    await add_filter_if_not_none(request, ProxyTypeDB, 'type', 'proxy_type_id', where)
    await add_filter_if_not_none(request, ProviderDB, 'prov', 'provider_id', where)
    await add_filter_if_not_none(request, ProviderPlanDB, 'plan', 'provider_plan_id', where)


async def add_target_constraints_to_where(request, target_id, where):
    '''Add the providers and plans to the where query'''
    await add_target_restriction_to_where(request, target_id, where,
                                          column_name='provider_id',
                                          model_db=TargetProviderDB)
    await add_target_restriction_to_where(request, target_id, where,
                                          column_name='provider_plan_id',
                                          model_db=TargetProviderPlanDB)


async def add_target_restriction_to_where(request, target_id, where, column_name, model_db):
    '''Check if there are any restrictions for the Target given a model
    Add them to the where if any'''
    model_inst = model_db(request.app)
    results = await model_inst.select(*[('target_id', '=', int(target_id))], columns=column_name)
    if results:
        where.append((column_name, 'in', [row[column_name] for row in results]))


def get_blocked_proxy_ids(request):
    '''Read the request.query data and returns the blocked IDs presents there if any'''
    blocked_ids = []
    blocked_data_str = request.query.get('blocked')
    if blocked_data_str is not None:
        blocked_ids.extend([int(p_id.strip()) for p_id in blocked_data_str.split('|')])
    return blocked_ids


async def get_target_data(request, target_id: int):
    '''It returns the data in database for the Target with ID <target_id>'''
    target_db = TargetDB(request.app)
    target_data = await target_db.select_one(*[('id', '=', target_id)])
    return target_data


async def get_handler(request):
    '''Main get handler'''
    config = request.app['config']
    target_identifier = request.match_info.get('tid')
    target_id = await get_target_id_from_identifier(request, target_identifier)
    if target_id is None:
        return web.json_response({
            'message': 'Target "{}" does not exist'.format(target_identifier),
            'data': {},
            'status': 'not found'}, status=404)
    target_data = await get_target_data(request, target_id)  # Target DB data
    pool_length = int(request.query.get('len', config['pool']['length']))  # List length
    blocked_ids = get_blocked_proxy_ids(request) # Blocked proxies to be added
    where = [] # Where query to filter proxy results
    await add_proxy_filter_to_where(request, where) # Basic proxy filter
    await add_target_constraints_to_where(request, target_id, where) # Target constraints
    proxy_db = ProxyDB(request.app)
    # Get all proxies filtered by the user query and allowed for this target
    all_proxies = await proxy_db.select(*where)
    # Create a Proxy pool manager
    proxy_pool = ProxyPool(pool_id=str(target_id), pool_len=pool_length,
                           standby_mins=target_data['blocked_standby'],
                           redis=request.app['redis'])
    # Mark proxies as blocked if any
    if blocked_ids:
        await proxy_pool.set_as_blocked_list(*blocked_ids)
    await proxy_pool.load(*all_proxies) # Load the proxy pool passing the proxies as parameter
    return web.json_response({'message': 'All OK',
                              'data': {
                                  'target_id': target_id,
                                  'pool': proxy_pool.pool},
                              'total': proxy_pool.length,
                              'status': 'success'}, status=200)
