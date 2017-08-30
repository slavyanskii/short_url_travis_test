import asyncio
import logging

import asyncpg
import short_url as short_url_maker

from settings import DB_CONFIG


class DBAsyncClient:
    DSN = 'postgres://{user}:{password}@{host}:{port}/{database}'

    def __init__(self):
        self._db_pool = None
        self.log = logging.getLogger()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.ensure_future(self._init_db()))

    async def _init_db(self):
        self._db_pool = await asyncpg.create_pool(self.DSN.format(**DB_CONFIG))

    async def create_short_url(self, full_url):
        async with self._db_pool.acquire() as connection:
            async with connection.transaction():
                last_row_id = await connection.fetchval('''INSERT INTO url_web (full_url) VALUES ($1) RETURNING id''',
                                                        full_url)
                short_url = short_url_maker.encode_url(last_row_id)
                await connection.execute('''UPDATE url_web SET short_url = $1 WHERE id = $2''', short_url, last_row_id)
        return short_url

    async def get_full_url(self, url_id):
        async with self._db_pool.acquire() as connection:
            full_url = await connection.fetchval('''SELECT full_url FROM url_web WHERE id = $1''', url_id)
        return full_url
