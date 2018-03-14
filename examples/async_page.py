"""Get a web page asynchronously."""

import asyncio

ENCODING = 'ISO-8859-1'


def get_encoding(header):
    """Find out encoding."""
    for line in header:
        if line.lstrip().startswith('Content-type'):
            for entry in line.split(';'):
                if entry.strip().startswith('charset'):
                    return entry.split('=')[1].strip()
    return ENCODING


async def get_page(host, port, wait=0):
    """Get a web page asynchronously."""
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(b'\r\n'.join([
        'GET /{} HTTP/1.0'.format(wait).encode(ENCODING),
        b'Host: %b' % host.encode(ENCODING),
        b'Connection: close',
        b'', b''
    ]))
    header = []
    msg_lines = []
    async for raw_line in reader:
        line = raw_line.decode(ENCODING).strip()
        if not line.strip():
            break
        header.append(line)
    encoding = get_encoding(header)
    async for raw_line in reader:
        line = raw_line.decode(encoding).strip()
        msg_lines.append(line)
    writer.close()
    return '\n'.join(msg_lines)
