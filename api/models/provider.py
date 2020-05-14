"""
DB operations for Providers
"""

from api.models.base import DBModel


class ProviderDB(DBModel):
    '''DBModel for the providers table'''

    tablename = 'providers'
