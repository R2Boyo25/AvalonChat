import asyncio
import websockets, time

async def hello():
    uri = "ws://localhost:8090"
    async with websockets.connect(uri) as websocket:

        await websocket.send('{"type":"auth", "token":"abcd1234"}')

        #time.sleep(10)

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

        while True:
            print(await websocket.recv())

asyncio.run(hello())