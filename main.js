const localVideo = document.getElementById('localVideo');   // get screen that show you
const remoteVideo = document.getElementById('remoteVideo'); // get screen that show other people

const peerConnectionConfig = {
    iceServers: [{urls: 'stun:stun.l.google.com:19302'}]
};

let localStream;
let peerConnection;

let remote_list = {};

const socket = new WebSocket('wss://192.168.0.195:8001');

class My_peer_connection extends RTCPeerConnection {
    constructor(conf, id) {
        super(conf);
        this.id = id;
        this.video_item = document.createElement("video");
        this.video_item.id = id;
        this.video_item.autoplay = true;
        document.getElementById("video_area").appendChild(this.video_item);
    }
    
    set_callback() {
        this.onicecandidate = (event) => {
            if (event.candidate) {
                // when have new ice, send to server
                socket.send(JSON.stringify({ iceCandidate: event.candidate, id: this.id }));
            }
        };

        localStream.getTracks().forEach(track => this.addTrack(track, localStream));
        
        this.ontrack = (event) => {
            document.getElementById(this.id).srcObject = event.streams[0];
        };
    }
}

async function start() {
    // get local image from camera by stream format
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    
    // set your camera image to screen
    localVideo.srcObject = localStream;
}

socket.onopen = () => {
    //console.log('WebSocket open');
};

socket.onmessage = (event) => {
    const message = JSON.parse(event.data);

    if (message.create) {
        createOffer(message);
    }
    else if (message.offer) {
        handleOffer(message);
    }
    else if (message.answer) {
        handleAnswer(message);
    }
    else if (message.iceCandidate) {
        handleNewICECandidate(message);
    }
    else if (message.type == "del") {
        document.getElementById(message.id).remove();
        delete remote_list[message.id];
    }
}

// send image to other
function handleOffer(message) {
    //console.log("get offer");
    remote_list[message.id] = new My_peer_connection(peerConnectionConfig, message.id);
    remote_list[message.id].set_callback();
    remote_list[message.id].setRemoteDescription(new RTCSessionDescription(message.offer));
    remote_list[message.id].createAnswer().then(answer => {
        remote_list[message.id].setLocalDescription(answer);
        socket.send(JSON.stringify({answer: answer, id: message.id}));
    });
}

// set the image from other to screen
function handleAnswer(message) {
    remote_list[message.id].setRemoteDescription(new RTCSessionDescription(message.answer));
}

// 
function handleNewICECandidate(message) {
    //console.log("get ice");
    const iceCandidate = new RTCIceCandidate(message.iceCandidate);
    remote_list[message.id].addIceCandidate(iceCandidate);
    //peerConnection.addIceCandidate(iceCandidate);
}

// send "offer" messege to server
// tell server you want in
async function createOffer(message) {
    for (let i = 0; i < message.ids.length; i++) {
        remote_list[message.ids[i]] = new My_peer_connection(peerConnectionConfig, message.ids[i]);
        remote_list[message.ids[i]].set_callback();
        let offer = await remote_list[message.ids[i]].createOffer();
        remote_list[message.ids[i]].setLocalDescription(offer);
        socket.send(JSON.stringify({offer: offer, id: message.ids[i]}));
    }
}

window.addEventListener("beforeunload", () => {
    socket.send(JSON.stringify({ type: "del" }));
});

start().then(() => {
    socket.send(JSON.stringify({type: "join"}));
});
