import asyncio


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()


async def start_serving():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    return server


async def stop_serving(server):
    server.close()
    await server.wait_closed()


# Start the server
loop = asyncio.get_event_loop()
server = loop.run_until_complete(start_serving())

# Serve requests until Ctrl+C is pressed
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
loop.run_until_complete(stop_serving(server))
loop.close()
