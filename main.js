const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo')
const peerConnectionConfig = {
    iceServers: [{urls: 'stun:stun.l.google.com:19302'}]
}
let localStream;
let peerConnection;
const socket = new WebSocket('wss://192.168.0.195:8001');

async function start() {
    // 獲取本地媒體流（視訊與音訊）
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    localVideo.srcObject = localStream
    // 創建 RTCPeerConnection 物件
    peerConnection = new RTCPeerConnection(peerConnectionConfig)
    // 在創建後設置 ICE candidate 事件處理器
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            // 當有新的 ICE candidate 時，發送到伺服器
            socket.send(JSON.stringify({ iceCandidate: event.candidate }));
        }
    }
    // 將本地媒體流的所有 track 加入 peerConnection
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream))
    // 當接收到遠端流時顯示
    peerConnection.ontrack = (event) => {
        remoteVideo.srcObject = event.streams[0];
    };
}

// WebSocket 連線與信令處理
socket.onopen = () => {
    console.log('WebSocket connection established');
}

socket.onmessage = (event) => {
    const message = JSON.parse(event.data)
    if (message.offer) {
        handleOffer(message.offer);
    } else if (message.answer) {
        handleAnswer(message.answer);
    } else if (message.iceCandidate) {
        handleNewICECandidate(message.iceCandidate);
    }
}

// 處理來自其他用戶的 offer 訊息
function handleOffer(offer) {
    peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
    peerConnection.createAnswer().then(answer => {
        peerConnection.setLocalDescription(answer);
        socket.send(JSON.stringify({ answer: answer })); // 發送 answer 回去
    });
}

// 處理來自其他用戶的 answer 訊息
function handleAnswer(answer) {
    peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
}

// 處理 ICE candidate
function handleNewICECandidate(candidate) {
    const iceCandidate = new RTCIceCandidate(candidate);
    peerConnection.addIceCandidate(iceCandidate);
}

// 發送 offer 訊息給伺服器
async function createOffer() {
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    socket.send(JSON.stringify({ offer: offer }));  // 發送 offer 訊息
}

window.onunload = () => {
	socket.send(JSON.stringify({type: "del"}));
}

// 這是開始連線的地方，呼叫此方法開始建立 WebRTC 連線
start().then(() => {
    // 一旦本地媒體流準備好，就可以創建 offer
    createOffer();
});