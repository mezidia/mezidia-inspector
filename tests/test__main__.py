from aiohttp import web

from inspector import __main__ as main


async def test_ping(aiohttp_client):
    """Test launch the app"""
    app = web.Application()
    app.router.add_post('/', main.webhook)
    client = await aiohttp_client(app)
    headers = {'x-github-event': 'ping', 'x-github-delivery': '1234'}
    data = {'zen': 'testing is good'}
    response = await client.post('/', headers=headers, json=data)
    assert response.status == 200


async def test_success(aiohttp_client):
    """Test success action"""
    app = web.Application()
    app.router.add_post('/', main.webhook)
    client = await aiohttp_client(app)
    headers = {'x-github-event': 'ping', 'x-github-delivery': '1234'}
    data = {'action': 'created'}
    response = await client.post('/', headers=headers, json=data)
    assert response.status == 200


async def test_failure(aiohttp_client):
    """Test the app without headers"""
    app = web.Application()
    app.router.add_post('/', main.webhook)
    client = await aiohttp_client(app)
    response = await client.post('/', headers={})
    assert response.status == 500
