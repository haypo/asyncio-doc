import asyncio


async def run_command(*args):
    # Create subprocess
    process = await asyncio.create_subprocess_exec(
        *args,
        # stdout must be piped to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE)

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    # Return stdout
    return stdout.decode().strip()


async def main():
    # Gather uname and date commands
    commands = asyncio.gather(run_command('uname'), run_command('date'))

    # Wait for the results
    uname, date = await commands

    # Print a report
    print('uname: {}, date: {}'.format(uname, date))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
