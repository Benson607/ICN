#!/usr/bin/env python

import json
import asyncio
from websockets.asyncio.server import serve

async def handler(websocket):
    async for msg in websocket:
        msg_deconde = json.loads(msg)
        if msg_deconde["type"] == "msg":
            event = {
                "response": "get"
            }
            await websocket.send(json.dumps(event))

async def main():
    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())