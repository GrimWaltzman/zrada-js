import asyncio
import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web
import random


def error_html(template, request, context={}):
    return aiohttp_jinja2.render_template(template, request, context)





def error_factory(templates: dict):
    templates = templates
    async def error_middleware(app, handler):
        async def middleware_handler(request):
            try:
                response = await handler(request)
                if response.status in templates:
                    return error_html(templates[response.status], request)
                return response
            except web.HTTPException as ex:
                if ex.status in templates:
                    return error_html(templates[ex.status], request)
                raise

        return middleware_handler
    return error_middleware