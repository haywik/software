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


async def input_waiting():
    return await asyncio.to_thread(input,"Enter MSG:")

async def connect():
    uri = "ws://localhost:8011/join"

    try:
        async with websockets.connect(uri) as websocket:
            serv = await websocket.recv()
            print(f"INFO websocket.connect(uri): {serv}")
            user_term = asyncio.create_task(input_waiting())
            while True: #


                outcoming = {   #outcoming for client, incoming for client
                    "client": {
                        "type": "websocket.send",

                        "alive": True,
                        "request": "alive",
                        "msg": "null"
                    }
                }

                try:
                    if user_term.done():
                        user_term = user_term.result()
                        print("User has inputted",user_term)
                        outcoming["client"]["request"] = "message"
                        outcoming["client"]["msg"] = user_term

                        user_term = asyncio.create_task(input_waiting())

                except Exception as e:
                    print("user input error",e)

                #print(outcoming)
                await websocket.send(json.dumps(outcoming))


                incoming =  json.loads(await websocket.recv())

                if incoming["server"]["request"] == "message":
                    temp = incoming['server']['msg']
                    print("INFO websocket.connect(uri) MESSAGE RECEIVED: {incoming['client']['msg']}")
                elif incoming["server"]["request"] == "response":
                    #print("INFO websocket.connect(uri) SERVER RESPONSE:",incoming['server']['msg'])
                    pass

                await asyncio.sleep(1)

    except Exception as e:
        print("client error in connect()",e)
        await websocket.close()
        await asyncio.sleep(2)
        return
        #new room logic?



async def run_relay():
    try:
        await connect()
    except:
        asynno.run(run_relay())


try:
    asyncio.run(run_relay())

except Exception as e:

    print("ERROR core run", e)



