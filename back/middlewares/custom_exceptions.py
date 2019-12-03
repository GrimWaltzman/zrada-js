import aiohttp_jinja2
from aiohttp import web


def error_html(template, request, context={}, status_code=200):
    return aiohttp_jinja2.render_template(template, request, context, status=status_code)


def error_json(message, status_code=200):
    return web.json_response({"error": True,"message": message}, status=status_code)


def error_factory(templates: dict):
    templates = templates

    async def error_middleware(app, handler):
        async def middleware_handler(request):
            if request.path.startswith('/api/'):
                try:
                    response = await handler(request)
                    return response
                except web.HTTPException as ex:
                    return error_json(ex.reason , status_code=ex.status_code)

            if not request.path.startswith('/api/'):
                try:
                    response = await handler(request)
                    if response.status in templates:
                        return error_html(templates[response.status], request, status_code=response.status_code)
                    return response
                except web.HTTPException as ex:
                    if ex.status in templates:
                        return error_html(templates[ex.status], request, status_code=ex.status_code)
                    raise

            response = await handler(request)
            return response

        return middleware_handler
    return error_middleware