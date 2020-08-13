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

    async def get_user(self, username):
        '''Get the user from DB using the username'''
        where = [('username', '=', username)]
        return await self.select_one(*where)

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

    async def verify_identity(self, username, password):
        '''Verify if the password `pwd` is valid'''
        user = await self.get_user(username)
        if user is None:
            return False
        return pwd_context.verify(password, user['password'])

    async def set_password(self, username, password):
        '''Set a new password for the current user'''
        new_password = self.password_hash(password)
        where = [('username', '=', username)]
        await self.update('password', (new_password, ), *where)
