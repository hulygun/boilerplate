import aiohttp_rpc
from aiohttp import web

from rpc_methods import send_message

aiohttp_rpc.rpc_server.add_methods([
    send_message
])

async def web_app():
    app = web.Application()
    app.router.add_routes([
        web.post('/', aiohttp_rpc.rpc_server.handle_http_request),
    ])
    return app