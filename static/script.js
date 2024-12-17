let currentUsername = ""; // 用於儲存使用者名稱
let currentRoomId = ""; // 用於儲存房間號

const socket = io('https://192.168.0.173:5000'); //這裡改為自己電腦的ip

const chat = document.getElementById('chat');
const messageInput = document.getElementById('chat-input');
const usernameInput = document.getElementById("username");
const roomInput = document.getElementById("room-id"); // 獲取房間號輸入框

// 進入會議室的功能
document.getElementById("enter-room-btn").addEventListener("click", function () {
  const username = usernameInput.value.trim();
  const room = roomInput.value.trim();

  if (username && room) {
    socket.emit('join', { username, room });
    currentUsername = username; // 儲存使用者名稱
    currentRoomId = room; // 儲存房間號
    // 切換到會議室畫面
    document.getElementById("username-screen").classList.remove("active");
    document.getElementById("meeting-screen").classList.add("active");

    // 在聊天訊息區顯示歡迎訊息
    const chatMessages = document.querySelector(".chat-messages");
    const welcomeMessage = document.createElement("p");
    welcomeMessage.innerHTML = `<strong>系統:</strong> 歡迎 ${currentUsername} 加入房間 ${currentRoomId}！`;
    chatMessages.appendChild(welcomeMessage);
  } else {
    alert("請輸入您的名稱和房間號！");
  }
});

// 聊天輸入框的 Enter 鍵功能
document.getElementById("chat-input").addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault(); // 防止換行
    const username = usernameInput.value.trim();;
    const room = roomInput.value.trim();;
    const message = messageInput.value.trim();;
    if (username && room && message) {
        socket.emit('send_message', { username, room, message });
        messageInput.value = ''; // 清空輸入框
    }
  }
});

// 離開通話按鈕功能
document.getElementById("leave-call-btn").addEventListener("click", function () {
  const username = usernameInput.value.trim();;
  const room = roomInput.value.trim();;

  if (username && room) {
    socket.emit('leave', { username, room });
  }

  // 清空聊天區訊息
  const chatMessages = document.querySelector(".chat-messages");
  chatMessages.innerHTML = "";

  // 返回到用戶名輸入畫面
  document.getElementById("meeting-screen").classList.remove("active");
  document.getElementById("username-screen").classList.add("active");

  // 清空當前用戶名
  currentUsername = "";
});

function sendMessage() {
  const username = usernameInput.value.trim();;
  const room = roomInput.value.trim();;
  const message = messageInput.value.trim();;

  if (username && room && message) {
      socket.emit('send_message', { username, room, message });
      messageInput.value = ''; // 清空輸入框
  }
}

 // 接收訊息
socket.on('message', (data) => {
  const msgElement = document.createElement('p');
  msgElement.textContent = data.msg;
  chat.appendChild(msgElement);
  chat.scrollTop = chat.scrollHeight; // 自動滾動到底部
});