import asyncio
import random


async def produce(queue, n):
    for x in range(n):
        # produce an item
        print('producing {}/{}'.format(x, n))
        # simulate i/o operation using sleep
        await asyncio.sleep(random.random())
        item = str(x)
        # put the item in the queue
        await queue.put(item)


async def consume(queue):
    while True:
        # wait for an item from the producer
        item = await queue.get()
        # process the item
        print('consuming {}...'.format(item))
        # simulate i/o operation using sleep
        await asyncio.sleep(random.random())
        # Notify the queue that the item has been processed
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    # schedule the consumer
    consumer = asyncio.ensure_future(consume(queue))
    # run the producer and wait for completion
    await produce(queue, 10)
    # wait until the consumer has processed all items
    await queue.join()
    # the consumer is still awaiting for an item, cancel it
    consumer.cancel()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
