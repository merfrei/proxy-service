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

Some targets may not have have permission to use some proxy types or providers
"""

from aiohttp import web


async def get_handler(request):
    '''Main get handler'''
    target_id = request.match_info.get('tid')
    return web.json_response({'message': 'All OK',
                              'data': {'target_id': target_id},
                              'total': 0,
                              'status': 'success'}, status=200)
