const websocket = new WebSocket("ws://localhost:8001/");

window.addEventListener("DOMContentLoaded", () => {
  	document.getElementById("submit_button").addEventListener("click", function() {
		var msg = {
			type: "msg",
			text: document.getElementById("input_text").value
		}
		send(websocket, msg)
  	});
	websocket.addEventListener("message", ({ data }) => {
		const response = JSON.parse(data);
		console.log(response);
	});
});

function send(socket, msg) {
	socket.send(JSON.stringify(msg));
}

window.addEventListener('beforeunload', () => {
	if (websocket === WebSocket.OPEN) {
		websocket.close();
	}
});