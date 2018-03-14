import asyncio


async def say(what, when):
    await asyncio.sleep(when)
    print(what)


async def schedule():
    asyncio.ensure_future(say('first hello', 2))
    asyncio.ensure_future(say('second hello', 1))


loop = asyncio.get_event_loop()
loop.run_until_complete(schedule())
loop.run_forever()
loop.close()
