import json
import socket
import struct

# 配置接收端地址和端口
host = "127.0.0.1"
port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

client_list = []
frame_buffer = {}
max_packet_size = 1200
current_frame_id = 0

try:
    while True:
        packet, addr = sock.recvfrom(65535)
  
        # read header
        header = packet[:struct.calcsize("IHBB")]
        frame_id, fragment_id, is_last, data_type = struct.unpack("IHBB", header)
        fragment_data = packet[struct.calcsize("IHBB"):]
        frame_size = len(fragment_data)

        if data_type == 0:
            for i in client_list:
                for j in range(0, frame_size, max_packet_size):
                    fragment = fragment_data[j:j + max_packet_size]
                    header = struct.pack("IHBQ", frame_id, fragment_id, is_last, client_list.index(addr))
                    sock.sendto(header + fragment, i)
        elif data_type == 1:
            pass
        elif data_type == 2:
            # check if is new packet
            if frame_id != current_frame_id:
                frame_buffer = {}
                current_frame_id = frame_id

            frame_buffer[fragment_id] = fragment_data

            if is_last:
                full_data = b"".join(frame_buffer[i] for i in sorted(frame_buffer.keys()))
                json_obj = json.loads(full_data.decode('utf-8'))

                if json_obj["type"] == "join":
                    client_list.append(addr)
                    print(f"{addr} join")

except Exception as e:
    print(e)    
finally:
    sock.close()
