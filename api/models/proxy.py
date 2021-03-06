"""
DB operations for Proxies
"""

from api.models.base import DBModel


class ProxyDB(DBModel):
    '''DBModel for the proxies table'''

    tablename = 'proxies'


class ProxyView(DBModel):
    '''List proxies view'''

    tablename = 'proxies_view'
