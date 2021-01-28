import aiohttp_rpc
from aiohttp import web


def echo(*args, **kwargs):
    return {
        'args': args,
        'kwargs': kwargs,
    }

async def ping(rpc_request):
    return 'pong'

if __name__ == '__main__':
    aiohttp_rpc.rpc_server.add_methods([
        ping,
        echo,
    ])

    app = web.Application()
    app.router.add_routes([
        web.post('/', aiohttp_rpc.rpc_server.handle_http_request),
    ])

    web.run_app(app, host='0.0.0.0', port=8080)