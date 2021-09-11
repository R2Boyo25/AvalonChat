import asyncio
import websockets, time, json
import threading, os
os.system('clear')

websockett = 0

async def hello():
    global websockett
    uri = "ws://localhost:8090"
    async with websockets.connect(uri) as websocket:
        websockett = websocket

        await websocket.send('{"type":"auth", "token":"abcd1234"}')

        while True:
            await websocket.send(json.dumps({'type':'message', 'message':input('> ')}))

        

async def receiveData(websocket):
    print('running')
    while True:
        print('receiving')
        print(await websocket.recv())
        await asyncio.sleep(0.5)

async def main(loop):
    await asyncio.sleep(0)
    await hello()
    t1 = asyncio.create_task(await receiveData(websockett))
    await t1

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()

asyncio.run(hello())