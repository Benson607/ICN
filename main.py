import asyncio
import websockets
import ssl
import json

# 儲存所有用戶的 WebSocket 連接
connected_clients = {}

times = 0

async def signaling_handler(websocket, path):
    global times

    user_id = id(websocket)
    
    try:
        async for message in websocket:
            data = json.loads(message)
            times += 1

            if 'offer' in data:
                #print(times, "get offer")
                if data["id"] in connected_clients:
                    await connected_clients[data["id"]].send(json.dumps({'offer': data['offer'], "id": user_id}))
            
            elif 'answer' in data:
                #print(times, "get answer")
                if data["id"] in connected_clients:
                    await connected_clients[data["id"]].send(json.dumps({'answer': data['answer'], "id": user_id}))
            
            elif 'iceCandidate' in data:
                #print(times, "get ice")
                if data["id"] in connected_clients:
                    await connected_clients[data["id"]].send(json.dumps({'iceCandidate': data['iceCandidate'], "id": user_id}))
            
            elif data["type"] == "join":
                connected_clients[user_id] = websocket
                if len(list(connected_clients.keys())) > 1:
                    tmp = list(connected_clients.keys())
                    pos_now = tmp.index(user_id)
                    del tmp[pos_now]
                    await connected_clients[user_id].send(json.dumps({"create": 1, "ids": tmp}))

            elif data["type"] == "del":
                for client in connected_clients:
                    if client != user_id:
                        await connected_clients[client].send(json.dumps({'type': "del", "id": user_id}))

                if user_id in connected_clients:
                    del connected_clients[user_id]

    except websockets.exceptions.ConnectionClosed as e:
        print(e)

# WebSocket 伺服器地址與 SSL 配置
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# 啟動 WebSocket 伺服器，使用 wss
# ip位置寫自己電腦的ip
start_server = websockets.serve(signaling_handler, "192.168.0.147", 8001, ssl=ssl_context)

# 啟動事件循環來運行伺服器
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
