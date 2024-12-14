#!/usr/bin/env python

import ssl
import json
import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

client_list = {}

async def handler(websocket):
    async for msg in websocket:
        msg_deconde = json.loads(msg)
        if msg_deconde["type"] == "msg":
            event = {
                "response": "get"
            }
            print(msg_deconde["text"])
            await websocket.send(json.dumps(event))
        
        elif msg_deconde["type"] == "video":
            
            client_id = id(websocket)
            if (client_id not in client_list):
                print(client_list)
            client_list[client_id] = websocket

            for other_id, other_client in list(client_list.items()):
                if other_id != client_id:
                    try:
                        msg_deconde["id"] = client_id
                        await other_client.send(json.dumps(msg_deconde))
                    except ConnectionClosed:
                        print("del")
                        del client_list[client_id]

async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    async with serve(handler, "192.168.0.195", 8001, ssl=ssl_context):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
