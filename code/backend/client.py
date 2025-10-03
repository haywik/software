from starlette.websockets import WebSocketDisconnect

import asyncio
import websockets
import json
import datetime



async def input_waiting():
    return await asyncio.to_thread(input,"Enter MSG:")


async def connect():

    #uri = "ws://app.haywik.com/backend"

    uri = "ws://localhost:8011/join"   #for testing, change to host ip for tsting over lan

    try:
        async with websockets.connect(uri) as websocket:
            await websocket.recv()

            user_term = asyncio.create_task(input_waiting())        #acceptes user input

            loop_count = 0
            while True:

                print("loop_count",loop_count)   #! test code

                loop_count += 1

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
                        outcoming["client"]["request"] = "message"
                        outcoming["client"]["msg"] = user_term

                        user_term = asyncio.create_task(input_waiting())

                        await websocket.send(json.dumps(outcoming))

                        print("MSG sent",outcoming["client"]["msg"])

                    else:
                        if int(loop_count / 5) == loop_count / 5:
                            await websocket.send(json.dumps(outcoming))

                except Exception as e:
                    print("user input error",e)



                incoming =  json.loads(await websocket.recv())

                if incoming["server"]["request"] == "message":
                    temp = incoming['server']['msg']
                    print(f"msg>{incoming['server']['msg']}")

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
    while True:
        try:
            await connect()
        except Exception as e:
            print("MAJOR ERROR, relay crashed\n",e)
            await asyncio.sleep(2)


asyncio.run(run_relay())





