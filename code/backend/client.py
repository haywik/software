import asyncio
import websockets




async def connect():
    uri = "ws://localhost:8011/join"

    async with websockets.connect(uri) as websocket:
        msg = await websocket.recv()
        print(msg)

        while True:
            try:
                msg = await websocket.recv()
                print("msg recived",msg)
            except:
                print("msg disconnected")
                break

async def chat(client_msg):
    url = "ws://localhost:8011/chat"




asyncio.run(connect())