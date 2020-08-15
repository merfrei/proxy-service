"""
Handler for targets
"""

from aiohttp import web
from api.handlers.base import get_value
from api.handlers.base import get_404_response
from api.models.target import TargetDB
from api.models.target_provider import TargetProviderDB
from api.models.target_provider_plan import TargetProviderPlanDB


async def get_handler(request):
    '''GET one or more targets'''
    model_id = request.match_info.get('id')
    model_db = TargetDB(request.app)
    total = 1
    paging_query = []
    if 'offset' in request.query:
        offset = int(request.query['offset'])
        paging_query.append('OFFSET {}'.format(offset))
    if 'limit' in request.query:
        limit = int(request.query['limit'])
        paging_query.append('LIMIT {}'.format(limit))
    where_query = []
    extra_query = []
    extra_query += paging_query
    if model_id is not None:
        model_id = int(model_id)
        where_query += [('id', '=', model_id), ]
        row = await model_db.select_one(*where_query,
                                        extra=' '.join(extra_query))
        result = dict(row) if row is not None else {}
        provider_db = TargetProviderDB(request.app)
        plan_db = TargetProviderPlanDB(request.app)
        result['providers'] = [prov['provider_id'] for prov in
                               await provider_db.select(*[('target_id', '=', model_id)])]
        result['plans'] = [plan['provider_plan_id'] for plan in
                           await plan_db.select(*[('target_id', '=', model_id)])]
        if not result:
            return get_404_response()
    else:
        rows = await model_db.select(*where_query,
                                     extra=' '.join(extra_query))
        result = [dict(r) for r in rows]
        total_c = await model_db.count(*where_query)
        total = total_c['count']
    return web.json_response({'message': 'All OK',
                              'data': result,
                              'total': total,
                              'status': 'success'}, status=200)


async def post_handler(request):
    '''POST a new target'''
    model_db = TargetDB(request.app)
    params = await request.json()
    if params:
        columns = []
        values = []
        for key, value in params.items():
            if key in ('providers', 'plans'):
                continue
            columns.append(key)
            try:
                values.append(get_value(key, value))
            except ValueError as err:
                return web.json_response({'message': str(err),
                                          'data': None,
                                          'status': 'client error'}, status=400)
        result = await model_db.insert(','.join(columns), *[tuple(values)])
        providers_db = TargetProviderDB(request.app)
        plans_db = TargetProviderPlanDB(request.app)
        if params['providers']:
            await providers_db.insert('target_id,provider_id',
                                    *[(result, int(tid)) for tid in params['providers']])
        if params['plans']:
            await plans_db.insert('target_id,provider_plan_id',
                                *[(result, int(pid)) for pid in params['plans']])
        return web.json_response({'message': 'All OK',
                                  'data': {'id': result},
                                  'status': 'success'}, status=201)
    return get_404_response()


async def put_handler(request):
    '''PUT update a target'''
    model_id = request.match_info.get('id')
    if model_id is not None:
        model_db = TargetDB(request.app)
        params = await request.json()
        if params:
            columns = []
            values = []
            for key, value in params.items():
                if key in ('providers', 'plans'):
                    continue
                columns.append(key)
                try:
                    values.append(get_value(key, value))
                except ValueError as err:
                    return web.json_response({'message': str(err),
                                              'data': None,
                                              'status': 'client error'}, status=400)
            where_query = [('id', '=', int(model_id)), ]
            result = await model_db.update(','.join(columns),
                                           tuple(values),
                                           *where_query)
            providers_db = TargetProviderDB(request.app)
            plans_db = TargetProviderPlanDB(request.app)
            await providers_db.delete(*[('target_id', '=', int(model_id))])
            if params['providers']:
                await providers_db.insert('target_id,provider_id',
                                        *[(int(model_id), int(tid)) for tid in params['providers']])
            await plans_db.delete(*[('target_id', '=', int(model_id))])
            if params['plans']:
                await plans_db.insert('target_id,provider_plan_id',
                                    *[(int(model_id), int(pid)) for pid in params['plans']])
            return web.json_response({'message': 'All OK',
                                      'data': dict(result),
                                      'status': 'success'}, status=200)
    return get_404_response()


async def delete_handler(request):
    '''DELETE remove a target'''
    model_id = request.match_info.get('id')
    if model_id is not None:
        model_db = TargetDB(request.app)
        where_query = [('id', '=', int(model_id)), ]
        await model_db.delete(*where_query)
        return web.json_response({'message': 'All OK',
                                  'data': {},
                                  'status': 'success'}, status=200)
    return get_404_response()
