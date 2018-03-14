import asyncio
import random


async def produce(queue, n):
    # produce n items
    for x in range(1, n+1):

        # produce an item (simulate i/o operation using sleep)
        print('producing {}/{}'.format(x, n))
        item = await asyncio.sleep(random.random(), result=x)

        # put the item in the queue
        await queue.put(item)

    # indicate the producer is done
    await queue.put(None)


async def consume(queue):
    while True:
        # wait for an item from the producer
        item = await queue.get()

        # the producer emits None to indicate that it is done
        if item is None:
            break

        # process the item (simulate i/o operation using sleep)
        print('consuming item {}...'.format(item))
        await asyncio.sleep(random.random())


async def main():
    queue = asyncio.Queue()
    producer_coro = produce(queue, 10)
    consumer_coro = consume(queue)
    await asyncio.gather(producer_coro, consumer_coro)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
