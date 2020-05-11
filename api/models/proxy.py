"""
DB operations for Proxies
"""

from api.model.base import DBModel


class ProxyDB(DBModel):
    '''DBModel for the proxies table'''

    tablename = 'proxies'
