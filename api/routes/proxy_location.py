"""
Routes for Proxy Location
"""

from api.handlers.proxy_location import get_handler
from api.handlers.proxy_location import post_handler
from api.handlers.proxy_location import put_handler
from api.handlers.proxy_location import delete_handler


def init_proxy_location_routes(app):
    '''Init routes for proxy location'''
    app.router.add_route('GET', r'/proxy_location/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/proxy_location', get_handler)
    app.router.add_route('POST', r'/proxy_location', post_handler)
    app.router.add_route('PUT', r'/proxy_location/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/proxy_location/{id:\d+}', delete_handler)
