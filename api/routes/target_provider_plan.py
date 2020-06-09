"""
Routes for Target / Provider Plan relations
"""

from api.handlers.target_provider_plan import get_handler
from api.handlers.target_provider_plan import post_handler
from api.handlers.target_provider_plan import put_handler
from api.handlers.target_provider_plan import delete_handler


def init_target_provider_plan_routes(app):
    '''Init routes for target_provider_plan'''
    app.router.add_route('GET', r'/target_provider_plan/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/target_provider_plan', get_handler)
    app.router.add_route('POST', r'/target_provider_plan', post_handler)
    app.router.add_route('PUT', r'/target_provider_plan/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/target_provider_plan/{id:\d+}', delete_handler)
