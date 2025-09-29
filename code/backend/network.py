from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

from fastapi.responses import StreamingResponse

from contextlib import asynccontextmanager

import asyncio
import json
import time
import subprocess
import datetime
import sys
import json
import uuid
import random


boot_time = datetime.datetime.now()




#----Varibles----

online={
    "clientID":{
        "websocket":"websocket value",
        "partner":"partner value",
        "joined":"base"
    }
}


queue=["clientID","NextClientID"]  #when a client requests a room, they are placed into queue, parternet is set to null, then moved onto someone random, must update partner one and two
#contains everyone with a active websocket,if null then sort() will give them a partner once it is their turn in the list

active_connections: set[WebSocket] = set()

#----Varibles End----


#app startup and shutdown behaviour
@asynccontextmanager
async def lifespan(app:FastAPI):
    yield



    print("Server Shutdown")
    for connection in active_connections:
        try:
            await connection.close(code=1001,reason="Server Shutdown")
        except:
            pass
    active_connections.clear()


app = FastAPI(lifespan=lifespan)


async def sort():
    while True:
        await asyncio.sleep(0.01)
        if queue >= 2:
            client = queue[0]
            partner = queue[random.randint(1,len(queue)-1)]

            online[client]["partner"] = partner
            online[partner]["partner"] = client

            websocket = online[client]["websocket"]
            websocket.send_text("room")

            websocket = online[partner]["websocket"]
            websocket.send_text("room")
        else:
            print("insufficent clients")
            await asyncio.sleep(0.01)



@app.websocket("/join")
async def join(websocket: WebSocket):

    await websocket.accept()

    Cid = str(uuid.uuid4())



    online.update({
        Cid:{
            "websocket":websocket,
            "partner":"null",
            "joined":datetime.datetime.now()
        }
    })


    queue.append(Cid)

    position = len(queue)+1

    await websocket.send_text(f"{Cid}:{position}")

    while True:
        try:              #keeps alive, manages if user goes offline
            incoming = await websocket.receive_text()
            asyncio.create_task(msg_manager(websocket,Cid,incoming))
        except WebSocketDisconnect:
            try:
                await websocket.close()
            except:
                pass
            print("websocket disconnect")
            if Cid in online:
                if online[Cid]["partner"] == "null":
                    del online[Cid]
                    queue.remove(Cid)

                else:

                    online.update({online[online[Cid]["partner"]]["partner"]:"null"})
        except RuntimeError:
            try:
                await websocket.close()
                await asyncio.sleep(5)
            except:
                pass
            print("run time error in join")
            print("websocket disconnect")
            if Cid in online:
                if online[Cid]["partner"] == "null":
                    del online[Cid]
                    queue.remove(Cid)

                else:

                    online.update({online[online[Cid]["partner"]]["partner"]: "null"})
        except Exception:
            try:
                await websocket.close()
            except:
                pass
            print("some not good in join, finnally called")




async def msg_manager(websocket : WebSocket,Cid,incoming):
    try:
        if not Cid or Cid=="":
            return

        incoming = json.loads(incoming)
        time_log = str(datetime.datetime.now())
        outcoming = {
            "server": {
                "type": "websocket.send",

                "request": "null",
                "msg": "null",
                "time": time_log
            }
        }
        #print(f"\n\n\nINFO msg_manager(), {websocket},{Cid},{incoming} \n\n\n")

        if incoming["client"]["alive"]:
            print("client send alive ping")
            outcoming["server"]["request"] = "response"
            outcoming["server"]["msg"] = "alive ping recived"
            #print(outcoming)
            await websocket.send_json(outcoming)
            return

        websocket1 = online[online[Cid]["partner"]]["websocket"]

        print("sending message")

        outcoming["server"]["request"] = "message"
        outcoming["server"]["msg"] = incoming["request"]["msg"]

        await websocket1.send(json.dumps(outcoming))
    except RuntimeError:
        try:
            await websocket.close()

        except:
            pass
        print("discconet msg already recived")
    except WebSocketDisconnect:
        try:
            await websocket.close()
        except:
            pass
        print("Websocket disconnect")



    except Exception:
        try:
            await websocket.close()
        except:
            pass
        print("something else wen wrong in msg_manager, finally called")


        pass

    return





