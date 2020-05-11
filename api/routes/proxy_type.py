"""
Routes for Proxy Type
"""

from api.handlers.proxy_type import get_handler
from api.handlers.proxy_type import post_handler
from api.handlers.proxy_type import put_handler
from api.handlers.proxy_type import delete_handler


def init_proxy_type_routes(app):
    '''Init routes for proxy type'''
    app.router.add_route('GET', r'/proxy_type/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/proxy_type', get_handler)
    app.router.add_route('POST', r'/proxy_type', post_handler)
    app.router.add_route('PUT', r'/proxy_type/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/proxy_type/{id:\d+}', delete_handler)
