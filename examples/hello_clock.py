import asyncio


async def print_every_second():
    while True:
        for i in range(60):
            print(i, 's')
            await asyncio.sleep(1)


async def print_every_minute():
    for i in range(1, 10):
        await asyncio.sleep(60)
        print(i, 'minute')


async def main():
    coro_second = print_every_second()
    coro_minute = print_every_minute()
    await asyncio.gather(coro_second, coro_minute)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
