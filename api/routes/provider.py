"""
Routes for Provider
"""

from api.handlers.provider import get_handler
from api.handlers.provider import post_handler
from api.handlers.provider import put_handler
from api.handlers.provider import delete_handler


def init_provider_routes(app):
    '''Init routes for provider'''
    app.router.add_route('GET', r'/provider/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/provider', get_handler)
    app.router.add_route('POST', r'/provider', post_handler)
    app.router.add_route('PUT', r'/provider/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/provider/{id:\d+}', delete_handler)
