"""
Routes for Token
"""

from api.handlers.token import post_handler


def init_token_routes(app):
    '''Init the routes for token generation'''
    app.router.add_route('POST', r'/token', post_handler)
