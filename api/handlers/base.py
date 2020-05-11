"""
Base Handler for the API operations
GET: get_handler
POST: post_handler
PUT: put_handler
DELETE: delete_handler
"""

import json
import datetime
from aiohttp import web


DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_datetime(content):
    '''Parse a date or datetime object and return a string'''
    if isinstance(content, datetime.datetime):
        return content.strftime(DEFAULT_DATETIME_FORMAT)
    if isinstance(content, datetime.date):
        return content.strftime(DEFAULT_DATE_FORMAT)
    return content


def custom_dumps(content):
    '''Custom JSON dumps including a parse date/datetime function'''
    return json.dumps(content, default=parse_datetime)


def get_404_response():
    '''Default 404 response'''
    return web.json_response({'message': 'Not found',
                              'data': {},
                              'status': 'unknown'}, status=404)


def get_value(key, value):
    """It detects if it's a special key (ie: date or time)
    In that case it converts the value to the proper type
    It returns the value without previous formating in other case"""
    if value is not None:
        if field_is_a_date(key):
            return datetime.datetime.strptime(value, DEFAULT_DATE_FORMAT).date()
        if field_is_a_datetime(key):
            return datetime.datetime.strptime(value, DEFAULT_DATETIME_FORMAT)
    return value


def field_is_a_date(field):
    '''Return true if field is a date'''
    return (
        field == 'date' or
        field.startswith('date_') or
                field.endswith('_date'))


def field_is_a_datetime(field):
    '''Return true if field is a datetime'''
    return (
        field == 'time' or
        field == 'timestamp' or
        field == 'datetime' or
        field.startswith('time_') or
                field.endswith('_time'))


def get_base_get(db_model, *where, extra=None):
    '''Return a default handler for GET requests'''
    async def get_handler(request):
        model_id = request.match_info.get('id')
        model_db = db_model(request.app)
        total = 1
        paging_query = []
        if 'offset' in request.query:
            offset = int(request.query['offset'])
            paging_query.append('OFFSET {}'.format(offset))
        if 'limit' in request.query:
            limit = int(request.query['limit'])
            paging_query.append('LIMIT {}'.format(limit))
        where_query = list(where)
        extra_query = []
        if extra is not None:
            extra_query.append(extra)
        extra_query += paging_query
        if model_id is not None:
            model_id = int(model_id)
            where_query += [('id', '=', model_id), ]
            row = await model_db.select_one(*where_query,
                                            extra=' '.join(extra_query))
            result = dict(row) if row is not None else {}
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
                                  'status': 'success'}, status=200,
                                 dumps=custom_dumps)
    return get_handler


def get_base_post(db_model):
    '''Return a default handler for POST requests'''
    async def post_handler(request):
        model_db = db_model(request.app)
        params = await request.json()
        if params:
            columns = []
            values = []
            for key, value in params.items():
                columns.append(key)
                try:
                    values.append(get_value(key, value))
                except ValueError as err:
                    return web.json_response({'message': str(err),
                                              'data': None,
                                              'status': 'client error'}, status=400)
            result = await model_db.insert(','.join(columns), *[tuple(values)])
            return web.json_response({'message': 'All OK',
                                      'data': {'id': result},
                                      'status': 'success'}, status=201,
                                     dumps=custom_dumps)
        return get_404_response()
    return post_handler


def get_base_put(db_model):
    '''Return a default handler for PUT requests'''
    async def put_handler(request):
        model_id = request.match_info.get('id')
        if model_id is not None:
            model_db = db_model(request.app)
            params = await request.json()
            if params:
                columns = []
                values = []
                for key, value in params.items():
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
                return web.json_response({'message': 'All OK',
                                          'data': dict(result),
                                          'status': 'success'}, status=200,
                                         dumps=custom_dumps)
        return get_404_response()
    return put_handler


def get_base_delete(db_model):
    '''Return a default handler for DELETE requests'''
    async def delete_handler(request):
        model_id = request.match_info.get('id')
        if model_id is not None:
            model_db = db_model(request.app)
            where_query = [('id', '=', int(model_id)), ]
            result = await model_db.delete(*where_query)
            return web.json_response({'message': 'All OK',
                                      'data': dict(result),
                                      'status': 'success'}, status=200,
                                     dumps=custom_dumps)
        return get_404_response()
    return delete_handler
