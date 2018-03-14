"""aiohttp-based client to retrieve web pages."""

import time
import asyncio
import aiohttp


async def fetch_page(session, host, port=8000, wait=0):
    """Get one page."""
    url = '{}:{}/{}'.format(host, port, wait)
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            assert response.status == 200
            text = await response.text()
            return text.strip('\n')


async def get_multiple_pages(host, waits, port=8000, show_time=True):
    """Get multiple pages."""
    start = time.perf_counter()
    with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, host, port, wait) for wait in waits]
        pages = await asyncio.gather(*tasks)
    duration = time.perf_counter() - start
    sum_waits = sum(waits)
    if show_time:
        msg = 'It took {:4.2f} seconds for a total waiting time of {:4.2f}.'
        print(msg.format(duration, sum_waits))
    return pages


async def main():
    """Test it."""
    pages = await get_multiple_pages(
        host='http://localhost', port='8000', waits=[1, 5, 3, 2])
    for page in pages:
        print(page)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
