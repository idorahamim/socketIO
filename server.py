import asyncio
from datetime import datetime

import socketio
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()

sio.attach(app)

connected_clients = set()


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('message')
async def do_nothing(sid, numbers):
    print("Socket ID: ", sid)
    for number in numbers:
        await asyncio.sleep(number)
        await sio.emit('message', number)
        print(number)

    await sio.emit('message', str(numbers) + ' done')


@sio.on('time')
async def send_time(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await sio.emit('time', current_time)


def print_connected_users():
    print("connected users: " + str(len(connected_clients)))
    print("users: " + str(connected_clients))


@sio.event
def disconnect(sid):
    connected_clients.remove(sid)
    print_connected_users()
    print('disconnect ', sid)


@sio.event
async def connect(sid, environ):
    connected_clients.add(sid)
    print_connected_users()
    print('connect ', sid)
    await sio.emit('message', 'ido connected to socket  io ' + str(sid))
    await send_time("time")
    return sid


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
