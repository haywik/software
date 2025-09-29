import asyncio
import websockets
import json

from starlette.websockets import WebSocketDisconnect

'''
msg = {
    "client":{
        "alive":True,
        "request":"null",
        "msg":"null"
    }
}
'''

async def connect():
    uri = "ws://localhost:8011/join"

    try:
        async with websockets.connect(uri) as websocket:
            serv = await websocket.recv()
            print(f"INFO websocket.connect(uri): {serv}")

            while True: #
                outcoming = {   #outcoming for clinet, incoming for client
                    "client": {
                        "type": "websocket.send",

                        "alive": True,
                        "request": "alive",
                        "msg": "null"
                    }
                }


                await websocket.send(json.dumps(outcoming))


                incoming =  json.loads(await websocket.recv())

                if incoming["server"]["request"] == "message":
                    temp = incoming['server']['msg']
                    print("INFO websocket.connect(uri) MESSAGE RECEIVED: {incoming['client']['msg']}")
                elif incoming["server"]["request"] == "response":
                    print("INFO websocket.connect(uri) SERVER RESPONSE:",incoming['server']['msg'])

                await asyncio.sleep(1)


    except:
        print("client error in connect()")
        await websocket.close()
        await asyncio.sleep(2)

        #new room logic?



async def run_relay():
    await asyncio.sleep(2)
    await connect()

while True:

    try:
        asyncio.run(run_relay())
    except Exception as e:

        print("ERROR core run", e)



