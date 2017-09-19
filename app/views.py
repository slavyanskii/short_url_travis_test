import asyncio

from aiohttp import web, hdrs
from marshmallow import Schema
from urllib.parse import urlunsplit
import short_url as short_url_maker

from app.exceptions import APIException
from app.serailizers import UrlSerializer

from settings import SCHEME, DOMAIN


class BaseView(web.View):
    serializer = Schema()

    async def pre_process_request(self):
        if self.request._method in {hdrs.METH_POST, hdrs.METH_PUT, hdrs.METH_PATCH, hdrs.METH_DELETE}:
            data = await self.request.json()
        else:
            data = self.request.query
        result = self.serializer.load(data)
        if result.errors:
            raise APIException(result.errors, 400)
        self.validated_data = result.data

    @asyncio.coroutine
    def __iter__(self):
        if self.request._method not in hdrs.METH_ALL:
            self._raise_allowed_methods()
        method = getattr(self, self.request._method.lower(), None)
        if method is None:
            self._raise_allowed_methods()
        try:
            yield from self.pre_process_request()
            resp = yield from method()
        except APIException as e:
            return e.response
        return resp


class UrlView(BaseView):
    serializer = UrlSerializer()

    async def post(self):
        result = self.validated_data
        short_url = await self.request['db'].create_short_url(result['full_url'])
        result['short_url'] = urlunsplit((SCHEME, DOMAIN, short_url, None, None))
        return web.json_response(result)


class UrlRedirectView(BaseView):

    async def get(self):
        try:
            url_id = short_url_maker.decode_url(self.request.match_info['url'])
        except ValueError:
            return web.FileResponse('static/not_found.html')
        full_url = await self.request['db'].get_full_url(url_id)
        if full_url:
            return web.HTTPFound(full_url)
        else:
            return web.FileResponse('static/not_found.html')
