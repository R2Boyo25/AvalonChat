import asyncio
import websockets, time, json
import threading, os
from aioconsole import ainput, aprint

os.system('clear')

websockett = 0

async def main2(websocket):
    #global websockett
    
    #   websockett = websocket

    await websocket.send('{"type":"auth", "token":"abcd1235"}')

    while True:
        await websocket.send(json.dumps({'type':'message', 'message':await ainput(">>> ")}))

        

async def receiveData(websocket):
    while True:
        aprint(await websocket.recv())
        await asyncio.sleep(0.5)

async def main(loop):
    await asyncio.sleep(0)
    uri = "ws://2.tcp.ngrok.io:12104"
    async with websockets.connect(uri) as websocket:
        await main2(websocket)
        t1 = asyncio.create_task(receiveData(websocket))
        await t1

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()

asyncio.run(hello())
