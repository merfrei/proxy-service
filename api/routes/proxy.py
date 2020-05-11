"""
Routes for Proxy
"""

from api.handlers.proxy import get_handler
from api.handlers.proxy import post_handler
from api.handlers.proxy import put_handler
from api.handlers.proxy import delete_handler


def init_proxy_routes(app):
    '''Init routes for proxy'''
    app.router.add_route('GET', r'/proxy/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/proxy', get_handler)
    app.router.add_route('POST', r'/proxy', post_handler)
    app.router.add_route('PUT', r'/proxy/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/proxy/{id:\d+}', delete_handler)
