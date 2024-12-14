var websocket = new WebSocket("ws://localhost:8001/");
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');

var canvas_other = document.createElement('canvas');
var ctx_other = canvas_other.getContext("2d");

var video_id_list = [];

window.addEventListener("DOMContentLoaded", () => {
  	document.getElementById("submit_button").addEventListener("click", function() {
		var msg = {
			type: "msg",
			text: document.getElementById("input_text").value
		}
		send(msg);
  	});
	websocket.addEventListener("message", ({ data }) => {
		const response = JSON.parse(data);
		if (response["type"] == "video") {
			if (video_id_list.includes(response["id"]) === false) {
				console.log("append");
				video_id_list.push(response["id"]);
				const new_video = document.createElement("video");
				new_video.id = response["id"];
				new_video.autoplay = true;
				document.getElementById("video_area").appendChild(new_video);
			}
			
			const other_video = document.getElementById(response["id"]);
			
			const img = new Image();
    		
			img.onload = () => {
    		    canvas.width = img.width;
    		    canvas.height = img.height;
			
    		    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
			
    		    // 將 canvas 每幀轉為視頻數據模擬幀
    		    const stream = canvas.captureStream(30); // 每秒捕獲 30 幀
    		    other_video.srcObject = stream;
    		};
			img.src = "data:image/jpeg;base64," + response["data"];
		}
	});
});

function send(msg) {
	if (websocket.readyState === WebSocket.OPEN) {
		websocket.send(JSON.stringify(msg));
	}
}

window.addEventListener('beforeunload', () => {
	if (websocket === WebSocket.OPEN) {
		websocket.close();
	}
});

function send_video(video) {

	function captureFrame() {
		if (video.readyState >= 2) {

			// 設定 canvas 尺寸與 video 匹配
			canvas.width = video.videoWidth;
			canvas.height = video.videoHeight;
			
			// 在 canvas 上繪製 video 畫面
			ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

			// 將畫面轉換為 Base64
        	const base64String = canvas.toDataURL('image/jpeg', 0.8); // 0.8 為壓縮品質
			var msg = {
				type: "video",
				data: base64String.split(",")[1]
			}

			send(msg);
		}

		// 每秒捕獲 10 幀（可調整）
		setTimeout(captureFrame, 100);
	}

	captureFrame();
}