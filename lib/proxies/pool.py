"""
Proxies Pool Manager

It manages a pool of proxies
Stores already returned proxies in Redis
Also add a standby time value for some proxies. It can be used for blocked IPs
The goal is make fair use of proxies
Also the pool can be configured to give flexibility using proxies
"""

import random
from datetime import datetime
from datetime import timedelta


class ProxyPool:
    '''Proxy Pool'''

    used_key_frmt = '{pool_id}_used_list'
    blocked_key_frmt = '{pool_id}_blocked:{pid}'
    blocked_datetime_frmt = '%Y-%m-%d %H:%M'

    def __init__(self, pool_id: str, pool_len: int, standby_mins: int, redis: object):
        '''
        @param pool_id: the pool ID (ie: the domain or the target ID)
        @param pool_len: the min size of the pool or the min number of proxies to be returned
        @param standby_mins: how much time a blocked proxy should be excluded from the pool
        @redis: the redis connection pool'''
        self.pool_id = pool_id
        self.pool_len = pool_len
        self.standby_mins = standby_mins
        self.redis = redis
        self.pool = []

    @property
    def length(self):
        '''Return the pool length'''
        return len(self.pool)

    async def load(self, *proxies):
        '''Load N (self.pool_len) proxies in the pool if available
        The pool size is a minimum number of proxies.
        It will reuse proxies if necessary or use blocked proxies
        To load N number of proxies is a MUST for this method
        @param *proxies: a list of already filtered proxy objects (dict)'''
        blocked_ids = set()
        used_ids = await self.get_used_ids()
        proxy_map = {proxy['id']: dict(proxy) for proxy in proxies}
        all_ids = {int(proxy_id) for proxy_id in proxy_map}
        available_ids = all_ids
        if used_ids:
            available_ids = available_ids - used_ids
        for proxy_id in available_ids:
            proxy_blocked = await self.is_blocked(proxy_id)
            if proxy_blocked:
                blocked_ids.add(proxy_id)
        if blocked_ids:
            available_ids = available_ids - blocked_ids
        if len(available_ids) < self.pool_len:
            # First will try cleaning used proxies and adding some used proxies
            if used_ids:
                await self.clean_used_stack()
                _ = self.fill_pool_ids(available_ids, used_ids)
            # If the length is still low then it will try using blocked proxies
            if len(available_ids) < self.pool_len and blocked_ids:
                added_ids = self.fill_pool_ids(available_ids, blocked_ids)
                for blocked_id in added_ids:
                    await self.unblock_proxy(blocked_id)
        for proxy_id in available_ids:
            self.pool.append(proxy_map[proxy_id])
            await self.set_as_used(proxy_id)

    def fill_pool_ids(self, pool_set, ids_set):
        '''Given an input pool set and a second pool with optional proxy ids
        will try to add ids to the input pool until it's full (self.pool_len)'''
        # It uses random.shuffle to give some random choice of the proxy IDs to add
        added_ids = []
        ids_list = list(ids_set)
        random.shuffle(ids_list)
        for proxy_id in ids_list:
            if len(pool_set) >= self.pool_len:
                break
            pool_set.add(proxy_id)
            added_ids.append(proxy_id)
        return added_ids

    async def is_blocked(self, pid: int):
        '''Check if the proxy ID (pid) is blocked'''
        blocked_key = self.blocked_key_frmt.format(pool_id=self.pool_id, pid=pid)
        blocked_res = await self.redis.get(blocked_key)
        if blocked_res is not None:
            blocked_time = datetime.strptime(blocked_res.decode('utf-8'),
                                             self.blocked_datetime_frmt)
            blocked_range = datetime.now() - blocked_time
            if blocked_range < timedelta(minutes=self.standby_mins):
                return True
            # Remove register
            await self.redis.delete(blocked_key)
        return False

    async def get_used_ids(self):
        '''Get the already used proxy IDs
        @return: set of IDs (int)'''
        used_key = self.used_key_frmt.format(pool_id=self.pool_id)
        used_list = await self.redis.smembers(used_key)
        return {int(pid) for pid in used_list}

    async def clean_used_stack(self):
        '''Clean the used proxy IDs stack'''
        used_key = self.used_key_frmt.format(pool_id=self.pool_id)
        await self.redis.delete(used_key)

    async def set_as_used(self, pid: int):
        '''Set the proxy ID as used'''
        used_key = self.used_key_frmt.format(pool_id=self.pool_id)
        await self.redis.sadd(used_key, pid)

    async def set_as_used_list(self, *pids):
        '''Set as used a list of proxy IDS'''
        for pid in pids:
            await self.set_as_used(pid)

    async def set_as_blocked(self, pid: int):
        '''Set the proxy ID as blocked'''
        blocked_key = self.blocked_key_frmt.format(pool_id=self.pool_id, pid=pid)
        blocked_time_str = datetime.now().strftime(self.blocked_datetime_frmt)
        await self.redis.set(blocked_key, blocked_time_str)

    async def set_as_blocked_list(self, *pids):
        '''Set as blocked a lost of proxy IDs'''
        for pid in pids:
            await self.set_as_blocked(pid)

    async def unblock_proxy(self, pid: int):
        '''Force to unblock a proxy ID'''
        blocked_key = self.blocked_key_frmt.format(pool_id=self.pool_id, pid=pid)
        await self.redis.delete(blocked_key)
