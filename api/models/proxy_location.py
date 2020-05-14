"""
DB operations for Proxy Locations
"""

from api.models.base import DBModel


class ProxyLocationDB(DBModel):
    '''DBModel for the proxy_locations table'''

    tablename = 'proxy_locations'
