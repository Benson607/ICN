from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'  # 替換為你的密鑰
socketio = SocketIO(app)

# 路由處理
@app.route('/')
def index():
    return render_template('index.html')

# 監聽用戶加入聊天室
@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'msg': f"{username} 加入了聊天室！"}, to=room)

# 監聽用戶離開聊天室
@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f"{username} 離開了聊天室！"}, to=room)

# 廣播訊息到聊天室
@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    message = f"{data['username']}: {data['message']}"
    emit('message', {'msg': message}, to=room)

# 啟動伺服器
if __name__ == '__main__':
    ssl_context = ('server.crt', 'server.key')
    # ip位置寫自己電腦的ip
    socketio.run(app, host='192.168.0.147', port=5000, ssl_context=ssl_context,debug=True)