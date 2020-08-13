"""
Manage users

- Add new user
- Update password
"""

import sys

import asyncio
import logging
import argparse

from asyncpg_connect.db import DBSession

from config import get_config
from api.models.user import UserDB


DESCRIPTION = 'Proxy Service - Users management'


def parse_arguments():
    '''Parse the command line arguments'''
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--add', type=str, dest='add_user',
                        help='Add a new user (CSV: username,password)')
    parser.add_argument('--update', type=str, dest='update_user',
                        help='Update the user password (CSV: username,password)')
    return parser.parse_args()


async def add_user(db_session: DBSession, username: str, password: str):
    '''Add a new user and set the password `password`'''
    hashed_password = UserDB.password_hash(password.strip())
    new_user = {
        'username': username.strip(),
        'password': hashed_password,
    }
    user_id = await db_session.insert_one('users', new_user, return_field='id')
    logging.debug('Added user with ID: %d', user_id)


async def set_password(db_session: DBSession, username: str, password: str):
    '''Set the password for the user with `username`'''
    hashed_password = UserDB.password_hash(password.strip())
    status = await db_session.connection.fetchval(
        'UPDATE users SET password = $1 WHERE username = $2', hashed_password, username.strip())
    logging.debug('Status: %r', status)


async def main():
    '''All happens here'''
    args = parse_arguments()

    log_format = '%(levelname)s: %(asctime)s %(filename)s: %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.NOTSET,
                        format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

    config = get_config()
    db_uri = config['database']['postgres']['uri']
    async with DBSession(db_uri) as db_session:
        if args.add_user:
            logging.info('Adding new user...')
            await add_user(db_session, *args.add_user.split(','))
        if args.update_user:
            logging.info('Updations user...')
            await set_password(db_session, *args.update_user.split(','))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
