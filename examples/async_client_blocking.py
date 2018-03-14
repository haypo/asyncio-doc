"""Get web pages.

Waiting until one pages is download before getting the next.
"""

import time
import asyncio
from async_page import get_page


async def get_multiple_pages(host, port, waits, show_time=True):
    """Get multiple pages."""
    start = time.perf_counter()
    pages = []
    for wait in waits:
        pages.append(await get_page(host, port, wait))
    duration = time.perf_counter() - start
    sum_waits = sum(waits)
    if show_time:
        msg = 'It took {:4.2f} seconds for a total waiting time of {:4.2f}.'
        print(msg.format(duration, sum_waits))
    return pages


async def main():
    """Test it."""
    pages = await get_multiple_pages(
        host='localhost', port='8000', waits=[1, 5, 3, 2])
    for page in pages:
        print(page)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
