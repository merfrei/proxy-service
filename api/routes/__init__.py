"""
API Routes
"""

from api.routes.target import init_target_routes
from api.routes.proxy import init_proxy_routes
from api.routes.proxy_type import init_proxy_type_routes
from api.routes.proxy_location import init_proxy_location_routes
from api.routes.provider import init_provider_routes
from api.routes.provider_plan import init_provider_plan_routes
from api.routes.target_provider import init_target_provider_routes
from api.routes.target_provider_plan import init_target_provider_plan_routes
from api.routes.proxy_list import init_proxy_list_routes
from api.routes.token import init_token_routes


def init_routes(app):
    '''Init all API routes
    Add your init routes methods here
    ie:
    def init_routes(app) {
        app.router.add_route('GET', r'/myroute', handler)
    }'''
    init_target_routes(app)
    init_proxy_routes(app)
    init_proxy_type_routes(app)
    init_proxy_location_routes(app)
    init_provider_routes(app)
    init_provider_plan_routes(app)
    init_target_provider_routes(app)
    init_target_provider_plan_routes(app)
    init_proxy_list_routes(app)
    init_token_routes(app)
