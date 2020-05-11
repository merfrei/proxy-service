"""
Routes for Profile
"""

from api.handlers.profile import get_handler
from api.handlers.profile import post_handler
from api.handlers.profile import put_handler
from api.handlers.profile import delete_handler


def init_profile_routes(app):
    '''Init routes for profile'''
    app.router.add_route('GET', r'/profile/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/profile', get_handler)
    app.router.add_route('POST', r'/profile', post_handler)
    app.router.add_route('PUT', r'/profile/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/profile/{id:\d+}', delete_handler)
