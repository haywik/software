from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

from fastapi.responses import StreamingResponse

from contextlib import asynccontextmanager

import asyncio
import datetime
import json
import uuid
import random







#----Varibles----

boot_time = datetime.datetime.now()

queue=[]

online={}

active_connections: set[WebSocket] = set()      #adds websocket as a hint, causes less errors and easier linking


#----Varibles End----


@asynccontextmanager        #Boot behaviour
async def lifespan(app:FastAPI):
    yield

    for connection in active_connections:
        try:
            await connection.close(code=1001,reason="Server Shutdown")
        except:
            pass
    active_connections.clear()


app = FastAPI(lifespan=lifespan)


async def sort():

    while True:
        if queue >= 2:
            try:
                client = queue[0]
                partner = queue[random.randint(1,len(queue)-1)]

                online[client]["partner"] = partner
                online[partner]["partner"] = client

                websocket = online[client]["websocket"]
                websocket.send_text("room")

                websocket = online[partner]["websocket"]
                websocket.send_text("room")
            except:
                pass
        else:
            print("INFO in sort(): Insufficent clients in queue")
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

            print("Websocket Dissconnect called in join()")

            try:websocket.close()
            except:pass

            if Cid in online:

                if online[Cid]["partner"] == "null":online[Cid]["partner"] = "null"

                else:online.update({online[online[Cid]["partner"]]["partner"]:"null"})

            return

        except RuntimeError as e:
            print("\nRunTimeError: Websocket disconnect",e)
            return

        except Exception as e:

            print("\nMajor exepetion 1 in join()",e)

            return




async def msg_manager(websocket : WebSocket,Cid,incoming):

    try:
        if not Cid or Cid=="":
            return


        incoming = json.loads(incoming)

        time_log = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        outcoming = {
            "server": {
                "type": "websocket.send",
                "request": "null",
                "msg": "null",
                "time": time_log
            }
        }

        #print(f"\n\n\nINFO msg_manager(), {websocket},{Cid},{incoming} \n\n\n")

        if incoming["client"]["request"] == "alive":
            time_log = outcoming["server"]["time"]
            print(f"\nAlive Ping {time_log} IP: {websocket.client.host}")                    #Here on clean up---------
            outcoming["server"]["request"] = "response"
            outcoming["server"]["msg"] = "alive ping recived"
            await websocket.send_json(outcoming)
        elif incoming["client"]["request"] == "message":
            try:
                print(incoming["client"]["request"])
                websocket1 = online[online[Cid]["partner"]]["websocket"]

                print("sending message")

                outcoming["server"]["request"] = "message"
                outcoming["server"]["msg"] = incoming["request"]["msg"]

                print("incoming message", incoming["request"]["msg"])

                await websocket1.send(json.dumps(outcoming))
            except Exception as e:
                print("\nEREROR exeption in msg_manager()",e)
        else:
            print("Unexpected incoming",incoming)


    except RuntimeError:
        try:
            await websocket.close()

        except:
            pass

        finally: return

    except WebSocketDisconnect:
        try:
            await websocket.close()
        except:
            pass
        finally:
            print("msg_manager websoket dissconnect")
            return



    except Exception as e:
        print("Exception in msg_manager()",e)

    return





