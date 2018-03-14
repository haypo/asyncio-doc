import asyncio
import aiohttp


async def fetch_page(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            assert response.status == 200
            return await response.read()


async def main():
    with aiohttp.ClientSession() as session:
        content = await fetch_page(session, 'http://python.org')
        print(content.decode())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
