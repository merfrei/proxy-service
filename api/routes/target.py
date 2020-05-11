"""
Routes for Target
"""

from api.handlers.target import get_handler
from api.handlers.target import post_handler
from api.handlers.target import put_handler
from api.handlers.target import delete_handler


def init_target_routes(app):
    '''Init routes for target'''
    app.router.add_route('GET', r'/target/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/target', get_handler)
    app.router.add_route('POST', r'/target', post_handler)
    app.router.add_route('PUT', r'/target/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/target/{id:\d+}', delete_handler)
