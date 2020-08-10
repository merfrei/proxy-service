"""
API authentication

- API Key
- Basic-Auth & Token
"""

from itsdangerous import SignatureExpired
from itsdangerous import BadSignature

from aiohttp import web
from aiohttp import hdrs
from aiohttp import BasicAuth

from api.models.user import UserDB


FORBIDDEN_MESSAGE = 'forbidden'


async def get_403_response(message=FORBIDDEN_MESSAGE):
    '''GET 403 Unauthorized response'''
    return web.json_response({'message': message,
                              'data': {},
                              'status': 'forbidden'}, status=403)


def parse_auth_header(request):
    '''Basic-Auth helper to get the authorization header'''
    auth_header = request.headers.get(hdrs.AUTHORIZATION)
    if not auth_header:
        return None
    try:
        auth = BasicAuth.decode(auth_header=auth_header)
    except ValueError:
        auth = None
    return auth


@web.middleware
async def apikey_middleware(request, handler):
    '''API api-key authentication aiohttp middleware'''
    api_key = request.query.get('api_key', None)
    api_key_method = '{}_api_key'.format(request.method.lower())
    app_api_key = request.app.get(api_key_method, request.app['api_key'])
    if api_key is None or api_key != app_api_key:
        return await get_403_response()
    return await handler(request)


@web.middleware
async def basicauth_token_middleware(request, handler):
    '''BasicAuth middleware to use when API-Key is not provided
    - It is usually used for public web dashboards or public clients'''
    auth_h = parse_auth_header(request)

    if auth_h is None:
        return await get_403_response()

    authenticated = False
    message = FORBIDDEN_MESSAGE

    try:
        token_data = UserDB.get_token_data(auth_h.login, auth_h.password)
        authenticated = token_data['user'] == auth_h.login
    except SignatureExpired:
        message = 'Token expired'
    except BadSignature:
        authenticated = await UserDB.verify_identity(auth_h.login, auth_h.password)

    if not authenticated:
        return await get_403_response(message)

    return await handler(request)
