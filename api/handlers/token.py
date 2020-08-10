"""
Handler to return a Token
"""

from aiohttp import web

from api.models.user import UserDB


async def post_handler(request):
    params = await request.json()
    if not 'username' in params:
        return web.json_response({'message': 'Not valid request',
                                  'data': {},
                                  'status': 'error'}, status=401)
    token = UserDB.generate_auth_token(params['username'])
    return web.json_response({'message': 'All OK',
                              'data': {'token': token},
                              'status': 'success'}, status=200)
