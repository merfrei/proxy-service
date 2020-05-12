"""
DB operations for Provider Plans
"""

from api.model.base import DBModel


class ProviderPlanDB(DBModel):
    '''DBModel for the provider_plans table'''

    tablename = 'provider_plans'
