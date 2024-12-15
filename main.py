import asyncio
import websockets
import ssl
import json

# 儲存所有用戶的 WebSocket 連接
connected_clients = set()

async def signaling_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)

            # 處理信令訊息：轉發 offer、answer 和 ICE candidates
            if 'offer' in data:
                for client in connected_clients:
                    if client != websocket:
                        await client.send(json.dumps({'offer': data['offer']}))
            elif 'answer' in data:
                for client in connected_clients:
                    if client != websocket:
                        await client.send(json.dumps({'answer': data['answer']}))
            elif 'iceCandidate' in data:
                for client in connected_clients:
                    if client != websocket:
                        await client.send(json.dumps({'iceCandidate': data['iceCandidate']}))
            elif data["type"] == "del":
                connected_clients.remove(websocket)

    except websockets.exceptions.ConnectionClosed as e:
        print(e)

# WebSocket 伺服器地址與 SSL 配置
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# 啟動 WebSocket 伺服器，使用 wss
start_server = websockets.serve(signaling_handler, "192.168.0.195", 8001, ssl=ssl_context)

# 啟動事件循環來運行伺服器
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
