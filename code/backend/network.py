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

app = FastAPI()




online={
    "clientID":{
        "websocket":"websocket value",
        "partner":"partner value",
        "joined":"base"
    }
}

#contains everyone with a active websocket,if null then sort() will give them a partner once it is their turn in the list

queue=["clientID","NextClientID"]  #when a client requests a room, they are placed into queue, parternet is set to null, then moved onto someone random, must update partner one and two


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
            if Cid in online:
                if online[Cid]["partner"] == "null":
                    del online[Cid]
                    queue.remove(Cid)

                else:

                    online.update({online[online[Cid]["partner"]]["partner"]:"null"})




async def msg_manager(websocket : WebSocket,Cid,incoming):
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
    print(f"\n\n\nINFO msg_manager(), {websocket},{Cid},{incoming} \n\n\n")

    if incoming["client"]["alive"]:
        outcoming["server"]["request"] = "response"
        outcoming["server"]["msg"] = "alive ping recived"
        await websocket.send_json(outcoming)
        return

    websocket = online[online[Cid]["partner"]]["websocket"]

    outcoming["server"]["request"] = "message"
    outcoming["server"]["msg"] = incoming["request"]["msg"]

    await websocket.send_json(outcoming)

    return






