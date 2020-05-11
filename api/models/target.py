"""
DB operations for Targets
"""

from api.model.base import DBModel


class TargetDB(DBModel):
    '''DBModel for the targets table'''

    tablename = 'targets'
