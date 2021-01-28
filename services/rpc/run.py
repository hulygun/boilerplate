import aiohttp_rpc
from aiohttp import web

def echo(*args, **kwargs):
    return {
        'args': args,
        'kwargs': kwargs,
    }

async def ping(rpc_request):
    return 'pong'

aiohttp_rpc.rpc_server.add_methods([
    ping,
    echo,
])

async def web_app():
    app = web.Application()
    app.router.add_routes([
        web.post('/', aiohttp_rpc.rpc_server.handle_http_request),
    ])
    return app