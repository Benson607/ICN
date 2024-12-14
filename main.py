#!/usr/bin/env python

import json
import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

import base64
from PIL import Image
from io import BytesIO

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
                print("add")
            client_list[client_id] = websocket

            for other_id, other_client in list(client_list.items()):
                if other_id != client_id:
                    try:
                        msg_deconde["id"] = client_id
                        await other_client.send(json.dumps(msg_deconde))
                    except ConnectionClosed:
                        del client_list[client_id]

async def main():
    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())