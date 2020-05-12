"""
DB operations for Target Providers relation
"""

from api.model.base import DBModel


class TargetProviderDB(DBModel):
    '''DBModel for the target_providers table'''

    tablename = 'target_providers'
