"""
Routes for Proxy List
"""

from api.handlers.proxy_list import get_handler


def init_proxy_list_routes(app):
    '''Init routes for proxy list'''
    app.router.add_route('GET', r'/proxy_list/{tid}', get_handler)
