import asyncio, asyncssh, sys

class MySSHTCPSession(asyncssh.SSHTCPSession):
    def connection_made(self, chan):
        self._chan = chan

    def data_received(self, data, datatype):
        self._chan.write(data)

def connection_requested(orig_host, orig_port):
    print('Connection received from %s, port %s' % (orig_host, orig_port))
    return MySSHTCPSession()

async def run_client():
    async with asyncssh.connect('meba.xyz',port=1985,username="sshforward", password='sshforward') as conn:
       # server = await conn.create_server(connection_requested, '', 44403,
       #                                   encoding='utf-8')

       # if server:
       #     await server.wait_closed()
       # else:
       #     print('Listener couldn''t be opened.', file=sys.stderr)
        listener = await conn.forward_remote_port(listen_host='meba.xyz', listen_port=44403, dest_host='192.168.100.254', dest_port=8123)
        print('Listening on port %s...' % listener.get_port())
        await listener.wait_closed()


try:
    asyncio.get_event_loop().run_until_complete(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))