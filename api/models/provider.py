"""
DB operations for Providers
"""

from api.model.base import DBModel


class ProviderDB(DBModel):
    '''DBModel for the providers table'''

    tablename = 'providers'
