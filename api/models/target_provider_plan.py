"""
DB operations for Target Provider Plans relation
"""

from api.models.base import DBModel


class TargetProviderPlanDB(DBModel):
    '''DBModel for the target_provider_plans table'''

    tablename = 'target_provider_plans'
