import asyncio


async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')

    while True:
        data = await reader.read(100)
        message = data.decode()
        print(f'{addr!r} >> {message!r}')

        if message == 'exit':
            writer.close()
            print(f'{addr!r} -- DISCONNECTED')
            break

        message_new = f'{message!r} — back to you!'
        writer.write(message_new.encode())
        await writer.drain()
        print(f'{addr!r} << {message_new!r}')


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 9095)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
