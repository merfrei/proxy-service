"""
Routes for Target / Provider relations
"""

from api.handlers.target_provider import get_handler
from api.handlers.target_provider import post_handler
from api.handlers.target_provider import put_handler
from api.handlers.target_provider import delete_handler


def init_target_provider_routes(app):
    '''Init routes for target_provider'''
    app.router.add_route('GET', r'/target_provider/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/target_provider', get_handler)
    app.router.add_route('POST', r'/target_provider', post_handler)
    app.router.add_route('PUT', r'/target_provider/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/target_provider/{id:\d+}', delete_handler)
