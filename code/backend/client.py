import asyncio
import websockets
import json
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

    async with websockets.connect(uri) as websocket:
        serv = await websocket.recv()
        print(f"INFO websocket.connect(uri): {serv}")

        while True: # heyyyyyyyyyy
            outcoming = {   #outcoming for clinet, incoming for client
                "client": {
                    "type": "websocket.send",

                    "alive": True,
                    "request": "alive",
                    "msg": "null"
                }
            }


            await websocket.send(json.dumps(outcoming))


            incoming = await json.loads(websocket.recv())

            if incoming["server"]["request"] == "message":
                print("INFO websocket.connect(uri) MESSAGE RECEIVED: {serv['client']['msg']}")
            elif incoming["server"]["request"] == "response":
                print("INFO websocket.connect(uri) SERVER RESPONSE: {serv['client']['msg']}")

            await asyncio.sleep(1)

        #new room logic?


while True: #needs better error management, temporty fix
    try:
        asyncio.run(connect())
    except Exception as e:
        print("ERROR core run",e)