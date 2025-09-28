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



waiting = {}
order=[]

chatting = []

async def sort():
    while True:
        try:
            if len(order)>=2:
                client1 = order[0]
                client2 = order[random.randint(1,len(order)-1)]

                ws1 = waiting(client1)
                ws2 = waiting(client2)

                if ws1 and ws2:
                    order.remove(client1)
                    order.remove(client2)

                    chatting[client1] = client1
                    chatting[client2] = client2

                    await ws1.send_text(f"Partner found")
                    await ws2.send_text(f"Partner found")
            await asyncio.sleep(1)
        except:
            await asyncio.sleep(0.1)


@app.websocket("/chat")
async def chat(websocket: WebSocket,client1,client2):
    await websocket.accept()







@app.websocket("/join")
async def join(websocket: WebSocket):
    await websocket.accept()

    Cid = str(uuid.uuid4())
    waiting[Cid] = websocket
    order.append(Cid)

    position = len(order)
    await websocket.send_text(f"{Cid}:{position}")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if Cid in waiting:
            del waiting[Cid]
            order.remove(Cid)












