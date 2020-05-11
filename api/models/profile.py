"""
DB operations for Profiles
"""

from api.model.base import DBModel


class ProfileDB(DBModel):
    '''DBModel for the profiles table'''

    tablename = 'profiles'
