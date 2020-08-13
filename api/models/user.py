"""
DB operations for Users
"""

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from config import get_config

from api.models.base import DBModel


class UserDB(DBModel):
    '''DBModel for the users table'''

    tablename = 'users'

    @classmethod
    async def get_user(cls, username):
        '''Get the user from DB using the username'''
        where = [('username', '=', username)]
        return await cls.select_one(*where)

    @staticmethod
    def get_token_data(username, token):
        '''If the token exists, check if it's valid'''
        app_config = get_config()
        serializer = Serializer(
            app_config['security']['secret_key'],
            expires_in=app_config['security']['token_expires_in'])
        return serializer.loads(token)

    @staticmethod
    def generate_auth_token(username):
        '''Generate a new token'''
        app_config = get_config()
        serializer = Serializer(
            app_config['security']['secret_key'],
            expires_in=app_config['security']['token_expires_in'])
        return serializer.dumps({'user': username})

    @staticmethod
    def password_hash(password):
        '''Generate and return a hashed password'''
        return pwd_context.encrypt(password)

    @classmethod
    async def verify_identity(cls, username, password):
        '''Verify if the password `pwd` is valid'''
        user = await cls.get_user(username)
        if user is None:
            return False
        return pwd_context.verify(password, user['password'])

    @classmethod
    async def set_password(cls, username, password):
        '''Set a new password for the current user'''
        new_password = cls.password_hash(password)
        where = [('username', '=', username)]
        await cls.update('password', (new_password, ), *where)
