import asyncio


async def say(what, when):
    await asyncio.sleep(when)
    print(what)


async def stop_after(when):
    await asyncio.sleep(when)
    asyncio.get_event_loop().stop()


async def schedule():
    asyncio.ensure_future(say('first hello', 2))
    asyncio.ensure_future(say('second hello', 1))
    asyncio.ensure_future(say('third hello', 4))
    asyncio.ensure_future(stop_after(3))


loop = asyncio.get_event_loop()
loop.run_until_complete(schedule())
loop.run_forever()
loop.close()
