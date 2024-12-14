let currentUsername = ""; // 用於儲存使用者名稱

// 進入會議室的功能
document.getElementById("enter-room-btn").addEventListener("click", function () {
  const usernameInput = document.getElementById("username");
  const username = usernameInput.value.trim();

  if (username) {
    currentUsername = username; // 儲存使用者名稱
    // 切換到會議室畫面
    document.getElementById("username-screen").classList.remove("active");
    document.getElementById("meeting-screen").classList.add("active");

    // 在聊天訊息區顯示歡迎訊息
    const chatMessages = document.querySelector(".chat-messages");
    const welcomeMessage = document.createElement("p");
    welcomeMessage.innerHTML = `<strong>系統:</strong> 歡迎 ${currentUsername} 加入會議！`;
    chatMessages.appendChild(welcomeMessage);
  } else {
    alert("請輸入您的名稱！");
  }
});

// 新增訊息的函式
function addMessage(message, sender) {
  if (message) {
    // 在聊天訊息區新增用戶訊息
    const chatMessages = document.querySelector(".chat-messages");
    const userMessage = document.createElement("p");
    userMessage.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatMessages.appendChild(userMessage);

    // 自動滾動到最新訊息
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

// 聊天訊息送出按鈕的功能
document.querySelector(".chat-input button").addEventListener("click", function () {
  const chatInput = document.getElementById("chat-input");
  const message = chatInput.value.trim();
  addMessage(message, currentUsername);
  chatInput.value = ""; // 清空輸入框
});

// 聊天輸入框的 Enter 鍵功能
document.getElementById("chat-input").addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault(); // 防止換行
    const chatInput = event.target;
    const message = chatInput.value.trim();
    addMessage(message, currentUsername);
    chatInput.value = ""; // 清空輸入框
  }
});
