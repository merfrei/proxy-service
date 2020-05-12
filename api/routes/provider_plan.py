"""
Routes for Provider Plan
"""

from api.handlers.provider_plan import get_handler
from api.handlers.provider_plan import post_handler
from api.handlers.provider_plan import put_handler
from api.handlers.provider_plan import delete_handler


def init_provider_plan_routes(app):
    '''Init routes for provider_plan'''
    app.router.add_route('GET', r'/provider_plan/{id:\d+}', get_handler)
    app.router.add_route('GET', r'/provider_plan', get_handler)
    app.router.add_route('POST', r'/provider_plan', post_handler)
    app.router.add_route('PUT', r'/provider_plan/{id:\d+}', put_handler)
    app.router.add_route('DELETE', r'/provider_plan/{id:\d+}', delete_handler)
